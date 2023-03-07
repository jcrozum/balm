from __future__ import annotations

import random
from functools import reduce
from networkx import DiGraph # type:ignore
from pyeda.boolalg.bdd import expr2bdd # type:ignore
from pypint import InMemoryModel, Goal # type:ignore
from biodivine_aeon import BooleanNetwork # type: ignore

from nfvsmotifs.petri_net_translation import place_to_variable
from nfvsmotifs.pyeda_utils import aeon_to_pyeda
from nfvsmotifs.state_utils import state_to_bdd, state_list_to_bdd, function_eval, function_is_true

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyeda.boolalg.bdd import BinaryDecisionDiagram # type:ignore


"""
    A module responsible for detecting motif-avoidant attractors within terminal restriction space.
"""

def detect_motif_avoidant_attractors(
    network: BooleanNetwork,
    petri_net: DiGraph,
    candidates: list[dict[str, int]],
    terminal_restriction_space: BinaryDecisionDiagram,
    max_iterations: int,
    ensure_subspace: dict[str, int] = {}
) -> list[dict[str, int]]:
    """
        Compute a sub-list of `candidates` which correspond to motif-avoidant attractors.
        Other method inputs:
         - `network` and `petri_net` represent the model in which the property should be checked.
         - `terminal_restriction_space` is a symbolic set of states which contains all motif avoidant 
            attractors (i.e. if a candidate state can leave this set, the candidate cannot be an attractor).
         - `max_iterations` specifies how much time should be spent on the "simpler" preprocessing
            before applying a more complete method.
    """

    if len(candidates) == 0:
        return []
    
    candidates = _preprocess_candidates(network, candidates, terminal_restriction_space, max_iterations, ensure_subspace=ensure_subspace)

    if len(candidates) == 0:
        return []

    return _filter_candidates(petri_net, candidates, terminal_restriction_space)

def _preprocess_candidates(
    network: BooleanNetwork,
    candidates: list[dict[str, int]],
    terminal_restriction_space: BinaryDecisionDiagram,
    max_iterations: int,
    ensure_subspace: dict[str, int] = {}
) -> list[dict[str, int]]:
    """
        A fast but incomplete method for eliminating spurious attractor candidates. 

        The idea is to build the symbolic encoding of the given `network`, and then
        randomly simulate transitions for individual states, trying to reach a state
        outside of the `terminal_restriction_space`.

        TODO (1): There are multiple places where we build the symbolic encoding, and it
        will surely introduce extra overhead. We might want to just create the encoding
        once and then pass it around.

        TODO (2): We could probably make this algorithm slighlty less random by doing
        a limited version of symbolic reachability. I.e. instead of simulating just one
        state transition in each step, compute the whole successor BDD and then test 
        against that. Once the BDD becomes too large after several steps, we can just 
        pick a single state from it and start again. Sam: I'll add a version of this
        later, once we can actually benchmark how it performs :)
    """

    # First, build the symbolic encoding:
    variables = []
    update_functions = {}
    for var in network.variables():
        if var in ensure_subspace: # do not update constant nodes
            continue
        var_name = network.get_variable_name(var)
        variables.append(var_name)
        function_expression = network.get_update_function(var)
        function_bdd = expr2bdd(aeon_to_pyeda(function_expression))
        update_functions[var_name] = function_bdd

    symbolic_candidates = state_list_to_bdd(candidates)
    filtered_candidates = []
    for state in candidates:
        state_bdd = state_to_bdd(state)

        # Remove state from the symbolic set. If we can prove that is
        # is not an attractor, we will put it back.
        symbolic_candidates = symbolic_candidates & ~state_bdd

        simulation = state.copy()   # A copy of the state that we can overwrite.
        is_valid_candidate = True
        for _ in range(max_iterations):
            # Advance all variables by one step in random order.
            random.shuffle(variables)
            for var in variables:
                step = function_eval(update_functions[var], simulation)
                assert step is not None
                simulation[var] = step

            if function_is_true(symbolic_candidates, simulation):
                # The state can reach some other state in the candidate
                # set. This does not mean it cannot be an attractor, but
                # it means it is sufficient to keep considering the other
                # candidate.
                is_valid_candidate = False
                break

            if not function_is_true(terminal_restriction_space, simulation):
                # The state can reach some other state outside of the
                # terminal restriction space, which means it cannot be
                # a motif avoidant attractor in this subspace.
                is_valid_candidate = False
                break

        if is_valid_candidate:
            # If we cannot rule out the candidate, we can put it back
            # into candidate set.
            symbolic_candidates = symbolic_candidates | state_bdd
            filtered_candidates.append(state)
    
    return filtered_candidates
            

def _filter_candidates(
    petri_net: DiGraph,
    candidates: list[dict[str, int]],
    terminal_restriction_space: BinaryDecisionDiagram,
) -> list[dict[str, int]]:
    """
        Filter candidate states using reachability procedure in Pint.
    """

    avoid_states = ~terminal_restriction_space | state_list_to_bdd(candidates)
    filtered_candidates = []

    for state in candidates:
        state_bdd = state_to_bdd(state)

        # Remove state from the symbolic set. If we can prove that is
        # is not an attractor, we will put it back.
        avoid_states = avoid_states & ~state_bdd

        if _Pint_reachability(petri_net, state, avoid_states) == False:
            avoid_states = avoid_states | state_bdd
            filtered_candidates.append(state)

    return filtered_candidates

def _Pint_reachability(
    petri_net: DiGraph,
    initial_state: dict[str, int],
    target_states: BinaryDecisionDiagram
) -> bool:
    """
        Use Pint to check if a given `initial_state` can possibly reach some state
        in the `target_states` BDD.

        TODO: Here, if the result of static analysis is inconclusive, Pint falls back to `mole`
        model checker. However, in the future, we might also explore other methods, such as
        petri net reduction or symbolic reachability.
    """
    if target_states.is_zero():
        return False    # Cannot reach a stat in an empty set.

    # Build a Pint model through an automata network and copy
    # over the initial condition.
    pint_model = InMemoryModel(petri_net_as_automata_network(petri_net))
    for var, level in initial_state.items():
        pint_model.initial_state[var] = level

    goal = _Pint_build_symbolic_goal(target_states)

    return pint_model.reachability(goal=goal, fallback='mole')

def _Pint_build_symbolic_goal(states: BinaryDecisionDiagram) -> Goal:
    """
        A helper method which (very explicitly) converts a set of states
        represented through a BDD into a Pint `Goal`.
    """
    assert not states.is_zero()

    goals = []
    for clause in states.satisfy_all():
        goal_atoms = [ f"{var}={level}" for var, level in clause.items() ]
        goals.append(Goal(",".join(goal_atoms)))

    return reduce(lambda a, b: a | b, goals)

def petri_net_as_automata_network(petri_net: DiGraph) -> str:
    """
        Takes a Petri net which was created by implicant encoding from a Boolean network,
        and builds an automata network file (`.an`) compatible with the Pint tool.

        TODO: This is one of those things that would probably be better served by having
        an "explicit" `PetriNetEncoding` class.
    """
    auotmata_network = ""

    # Go through all PN places and save them as model variables.
    variable_set = set()
    for place, kind in petri_net.nodes(data="kind"):
        if kind != "place":
            continue
        variable_set.add(place_to_variable(place)[0])
    variables = sorted(variable_set)

    # Declare all variables with 0/1 domains.
    for var in variables:
        auotmata_network += f"\"{var}\" [0, 1]\n"

    for transition, kind in petri_net.nodes(data="kind"):
        if kind != "transition":
            continue
        
        predecessors = set(petri_net.predecessors(transition))
        successors = set(petri_net.successors(transition))

        # The value under modification is the only 
        # value that is different between successors and predecessors.
        source_place = next(iter(predecessors - successors))
        target_place = next(iter(successors - predecessors)) 
        
        (s_var, s_level) = place_to_variable(source_place)
        (t_var, t_level) = place_to_variable(target_place)
        assert s_var == t_var

        # The remaining places represent the necessary conditions.
        # Here, we transform them into a text format.
        conditions = sorted(predecessors.intersection(successors))
        conditions = [ place_to_variable(p) for p in conditions ]
        conditions = [ f"\"{var}\"={int(level)}" for var, level in conditions ]

        # A pint rule consists of a variable name, value transition,
        # and a list of necessary conditions for the change.
        rule = f"\"{s_var}\" {int(s_level)} -> {int(t_level)} when {' and '.join(conditions)}\n"
        auotmata_network += rule
    
    return auotmata_network


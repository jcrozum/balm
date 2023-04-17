from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from biodivine_aeon import BooleanNetwork # type: ignore    
    from pyeda.boolalg.bdd import BinaryDecisionDiagram, BDDVariable # type:ignore

from nfvsmotifs.trappist_core import trappist
from nfvsmotifs.space_utils import percolate_space, percolate_network
from nfvsmotifs.state_utils import state_list_to_bdd, state_to_bdd
from nfvsmotifs.drivers import find_single_node_LDOIs, find_single_drivers
from nfvsmotifs.pyeda_utils import aeon_to_pyeda
from pyeda.inter import Not, expr2bdd, bdd2expr # type: ignore

def get_self_neg_tr_trap_spaces(network: BooleanNetwork) -> list[dict[str, int]]:
    """
    Takes a Boolean network and gets its self-negating time-reversal trap spaces.
    To find time-reversal trap spaces in a specific trap space,
    percolated network should be given as input. 
    """
    tr_trap_spaces = trappist(network, problem="max", reverse_time=True)
    self_neg_tr_trap_spaces = []
    for tr_trap_space in tr_trap_spaces:
        result, conflicts = percolate_space(network, tr_trap_space)
        if conflicts:
            self_neg_tr_trap_spaces.append(tr_trap_space)

    return self_neg_tr_trap_spaces

def get_terminal_restriction_space (stable_motifs: list[dict[str, int]],
                                    network: BooleanNetwork | None = None,
                                    ensure_subspace: dict[str, int] | None = None,
                                    use_single_node_drivers = True, use_tr_trapspaces = True) -> BinaryDecisionDiagram:
    """
    Find the terminal restriction space.

    Construct the negation of the terminal restriction space and return the negation of the negation.
    ~terminal restriction space = stable motifs | ~R(X) | self negating time reversal trap spaces
    ~R(X) = single node drivers of stable motifs(delta) | F(delta) | ~LDOI(~delta)

    network and ensure subspace required for using delta and tr trapspaces.
    """

    # ~terminal restriction space includes stable motifs
    result_bdd = state_list_to_bdd(stable_motifs)

    # ~terminal restriction space includes ~R(X)
    if use_single_node_drivers:
        # Get the percolated Boolean Network
        if ensure_subspace != None:
            reduced_network = percolate_network(network, ensure_subspace)
        else:
            reduced_network = network
        LDOIs = find_single_node_LDOIs(reduced_network)

        for stable_motif in stable_motifs:
            # find delta
            single_node_drivers = find_single_drivers(stable_motif, reduced_network, LDOIs=LDOIs)
            # ~R(X) includes delta
            result_bdd = result_bdd | state_to_bdd(dict(single_node_drivers))

            for single_node_driver in single_node_drivers:
                # ~R(X) includes the F(delta)
                expression = aeon_to_pyeda(reduced_network.get_update_function(single_node_driver[0]))
                if single_node_driver[1] == 0:
                    expression = Not(expression)
                result_bdd = result_bdd | expr2bdd(expression)
            
                # get ~delta
                not_delta = tuple([single_node_driver[0],(single_node_driver[1]+1)%2])
                # ~R(X) includes ~LDOI(~delta)
                result_bdd = result_bdd | ~state_to_bdd(LDOIs[not_delta])

    if use_tr_trapspaces:
        pass

    return ~result_bdd
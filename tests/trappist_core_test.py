from biodivine_aeon import BooleanNetwork, SymbolicAsyncGraph, FixedPoints # type: ignore
from nfvsmotifs.trappist_core import trappist, compute_fixed_point_reduced_STG
from nfvsmotifs.aeon_utils import remove_static_constraints
from nfvsmotifs.space_utils import is_syntactic_trap_space
from nfvsmotifs.petri_net_translation import network_to_petrinet
import sys

# TODO: Right now, this is necessary to correctly parse some of the larger models
# using PyEDA. In the future, we should ideally use a parser that does not have this problem.
sys.setrecursionlimit(100_000)

def test_network_minimum_traps(network_file):
    bn = BooleanNetwork.from_file(network_file)
    bn = remove_static_constraints(bn)
    stg = SymbolicAsyncGraph(bn)

    min_max_traps = trappist(bn, problem="min") + trappist(bn, problem="max")

    pn = network_to_petrinet(bn)
    min_max_traps_pre_encoded = trappist(pn, problem="min") + trappist(pn, problem="max")

    assert min_max_traps == min_max_traps_pre_encoded

    # We have no way of knowing if a trap is minimal/maximal, but we can still
    # verify that it is indeed a trap.
    for trap in min_max_traps:
        # First a quick syntactic check which should work most of the time,
        # but is incomplete.
        if is_syntactic_trap_space(bn, trap):
            continue
        # Then a proper symbolic check that should be reliable every time.
        symbolic_space = stg.fix_subspace({ x: bool(int(trap[x])) for x in trap })
        if stg.is_trap_set(symbolic_space):
            continue
        raise Exception(f"Failed on {network_file}: {trap} is not a trap space.")

def test_network_fixed_points(network_file):
    # Verify that the fixed-points of the test models are the same
    # as when computing using BDDs.
    bn = BooleanNetwork.from_file(network_file)
    bn = remove_static_constraints(bn)
    stg = SymbolicAsyncGraph(bn)

    symbolic_fixed_points = FixedPoints.symbolic(stg)
    trappist_fixed_points = trappist(bn, problem="fix")
    for fixed_point in trappist_fixed_points:
        # Convert trappist result to a symbolic singleton set.
        vertex = stg.fix_subspace({ x: bool(int(fixed_point[x])) for x in fixed_point })
        # Check that the fixed-point has been found, and remove it.
        assert vertex.is_subset(symbolic_fixed_points), \
            f"Failed on {network_file}: {fixed_point} is not in symbolic fixed points."
        symbolic_fixed_points = symbolic_fixed_points.minus(vertex)
    # In the end, all fixed-points must have been found.
    assert symbolic_fixed_points.is_empty(), \
        f"Failed on {network_file}: Some symbolic fixed points not detected by trappist."

def test_network_fixed_point_reduced_STG():
    # Validate the function for computing fixed points of the reduced STG 
    # on a single small input.

    bn = BooleanNetwork.from_bnet("""
        x1, (x1 & x2) | (!x1 & !x2)
        x2, (x1 & x2) | (!x1 & !x2)
    """)

    petri_net = network_to_petrinet(bn)
    avoid_subspace_1 = {"x1" : 1, "x2" : 1}
    avoid_subspace_2 = {}
    avoid_subspace_3 = {"x2" : 1}

    ensure_subspace_1 = {}
    ensure_subspace_2 = {"x1" : 0, "x2" : 0}


    retained_set = {"x1" : 0, "x2" : 0}
    candidate_set = compute_fixed_point_reduced_STG(petri_net, retained_set)
    assert len(candidate_set) == 2 # candidate_set = {00, 11}

    candidate_set = compute_fixed_point_reduced_STG(petri_net, retained_set, ensure_subspace=ensure_subspace_1, avoid_subspaces=[avoid_subspace_1])
    assert len(candidate_set) == 1 # candidate_set = {00}

    candidate_set = compute_fixed_point_reduced_STG(petri_net, retained_set, ensure_subspace=ensure_subspace_1, avoid_subspaces=[avoid_subspace_2])
    assert len(candidate_set) == 0 # candidate_set = empty

    candidate_set = compute_fixed_point_reduced_STG(petri_net, retained_set, ensure_subspace=ensure_subspace_2)
    assert len(candidate_set) == 1 # candidate_set = {00}

    retained_set = {"x1" : 1, "x2" : 1}
    candidate_set = compute_fixed_point_reduced_STG(petri_net, retained_set)
    assert len(candidate_set) == 3 # candidate_set = {01, 10, 11}

    candidate_set = compute_fixed_point_reduced_STG(petri_net, retained_set, ensure_subspace=ensure_subspace_1, avoid_subspaces=[avoid_subspace_1])
    assert len(candidate_set) == 2 # candidate_set = {01, 10}

    candidate_set = compute_fixed_point_reduced_STG(petri_net, retained_set, ensure_subspace=ensure_subspace_1, avoid_subspaces=[avoid_subspace_2])
    assert len(candidate_set) == 0 # candidate_set = empty

    candidate_set = compute_fixed_point_reduced_STG(petri_net, retained_set, ensure_subspace=ensure_subspace_1, avoid_subspaces=[avoid_subspace_3])
    assert len(candidate_set) == 1 # candidate_set = {10}


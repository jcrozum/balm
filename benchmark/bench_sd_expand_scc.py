import sys
from biodivine_aeon import BooleanNetwork
from balm.SuccessionDiagram import SuccessionDiagram
from balm._sd_algorithms.expand_source_SCCs import expand_source_SCCs
import balm.SuccessionDiagram

# Print progress and succession diagram size.
balm.SuccessionDiagram.DEBUG = True

NODE_LIMIT = 1_000_000
DEPTH_LIMIT = 10_000

bn = BooleanNetwork.from_file(sys.argv[1])
bn = bn.infer_valid_graph()

# Compute the succession diagram.
sd = SuccessionDiagram(bn)
fully_expanded = expand_source_SCCs(sd, check_maa=False)
assert fully_expanded

print(f"Succession diagram size:", len(sd))
print(f"Minimal traps:", len(sd.minimal_trap_spaces()))

print("size, expanded, minimal")
print(f"{len(sd)}, {len(list(sd.expanded_ids()))}, {len(sd.minimal_trap_spaces())}")
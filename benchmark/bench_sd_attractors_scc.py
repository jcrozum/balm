import sys
sys.path.append(".")

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
fully_expanded = expand_source_SCCs(sd)
assert fully_expanded

attractor_count = 0
motif_avoidant_count = 0

for node in sd.node_ids():
    attr = sd.node_attractor_seeds(node, compute=True)
    attractor_count += len(attr)
    if not sd.node_is_minimal(node):
        motif_avoidant_count += len(attr)

print("nodes, attractors, motif-avoidant")
print(f"{len(sd)}, {attractor_count}, {motif_avoidant_count}")
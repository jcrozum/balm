from biodivine_aeon import BooleanNetwork, SymbolicAsyncGraph, find_attractors
import sys
import os
import time

# Experiment: AEON attractor detection
#
# This script computes the asynchronous attractors for a given
# network using AEON.py. The script outputs the name of the model,
# the runtime in ms and the total number of attractors.
# 
# Example usage:
# ```
# python3 attr-aeon.py network.bnet
# ```
#

model_path = sys.argv[1]
model_name = os.path.basename(model_path)

bn = BooleanNetwork.from_file(model_path)
# Ensures that the static constraints in the model are valid.
# Should be negligible compared to attractor finding.
bn = bn.infer_regulatory_graph()
bn = bn.inline_inputs()
stg = SymbolicAsyncGraph(bn)

start = time.perf_counter_ns()
attractors = find_attractors(stg)
elapsed_ns = time.perf_counter_ns() - start
elapsed_ms = int(elapsed_ns / 1000)
print(f"{model_name}\t{elapsed_ms}\t{len(attractors)}")
from __future__ import annotations

import networkx as nx # type: ignore

from biodivine_aeon import BooleanNetwork  # type: ignore
from nfvsmotifs.petri_net_translation import network_to_petrinet
from nfvsmotifs.interaction_graph_utils import find_minimum_NFVS, feedback_vertex_set
from nfvsmotifs.trappist_core import trappist, compute_fixed_point_reduced_STG
from nfvsmotifs.space_utils import percolate_network, percolate_space, is_syntactic_trap_space, intersect
from nfvsmotifs.motif_avoidant import detect_motif_avoidant_attractors
from nfvsmotifs.state_utils import state_list_to_bdd

DEBUG = True

class SuccessionDiagram():
    def __init__(self, network: BooleanNetwork):
        # Original Boolean network.
        self.network = network
        # A Petri net representation of the original Boolean network.
        self.petri_net = network_to_petrinet(network)
        # Negative feedback vertex set.
        self.nfvs = feedback_vertex_set(network, parity="negative")
        # A directed acyclic graph representing the succession diagram.
        self.G = nx.DiGraph()
        # A dictionary used for uniqueness checks on the nodes of the succession diagram.
        # See `SuccessionDiagram.ensure_node` for details.
        self.node_indices = {}
        # Set of diagram node IDs that have already been expanded (i.e. their successors 
        # are already known).
        self.expanded = set()
        # Set of diagram node IDs where attractor search has already been performed.    
        self.attr_expanded = set()
        # Maps node IDs to lists of attractor "seed" vertices. Note that even if attractor 
        # search was performed, the node ID may not be present if no attractors were found.
        self.attractors = {}        

        self.ensure_node(None, {})

    def root(self) -> int: 
        return 0

    def __len__(self) -> int:
        return self.G.number_of_nodes()

    def max_depth(self) -> int:
        d = 0
        for node in self.G.nodes():
            d = max(d, self.node_depth(node))
        return d

    def node_depth(self, node_id: int, depth: int | None = None) -> int:
        if depth:
            self.G.nodes[node_id]['depth'] = max(self.G.nodes[node_id]['depth'], depth)

        return self.G.nodes[node_id]['depth']
    
    def node_space(self, node_id: int) -> dict[str, int]:
        return self.G.nodes[node_id]['fixed_vars']

    def is_minimal(self, node_id: int) -> bool:
        # TODO: This is not very fast, but it does not appear in any performance critical code.
        return len(list(self.G.successors(node_id))) == 0

    def expand_node(self, node_id: int, depth_limit: int | None = 0, node_limit: int | None = None) -> int:
        """
        Expand the given node. 
        
        By default, the method only expands the given node. That is, if its successors are unknown, they
        are computed and nothing else happens. However, you can use `depth_limit` to instruct the method to 
        continue expanding the child nodes up to a certain depth and number of nodes (or to expand the whole
        subgraph by setting the limits to `None`).
        
        If a recursive expansion is requested, the method will continue expanding until it visits an unexpanded 
        node  (as long as the depth limit permits it). This means you can start the expansion from an already
        expanded node and just increase the depth/size limit to gradually grow the decision diagram (instead
        of always starting in the unexpanded leaf nodes). 

        The `node_limit` applies to the number of nodes that are expanded, i.e. the number of nodes for which
        successors have been computed. The method also returns this number (i.e. number of actually expanded
        nodes). Hence, when the result is smaller than the given `node_limit`, you know that the whole
        sub-graph is fully computed.

        The `depth_limit` is relative to the provided `node_id`. I.e. this is not the "absolute" depth of the
        node in the diagram, but rather the distance from the initial `node_id`.
        """            
        bfs_queue = [(node_id, depth_limit)]
        visited = set()        

        total_expanded = 0

        while len(bfs_queue) > 0:
            node, depth = bfs_queue.pop(0)

            # Due to BFS, a node is always first visited with its maximal
            # depth_limit, hence there is no need to re-explore nodes, even
            # if they are visited again with a different depth limit.
            if node in visited:
                continue
            visited.add(node)            
            # If the node isn't expanded, we can expand it:
            if node not in self.expanded:                
                self._expand_one(node)

                total_expanded += 1

                if DEBUG:
                    print(f"Total expanded: {total_expanded}/{self.G.number_of_nodes()}. Fixed vars {len(self.node_space(node))}/{self.network.num_vars()} at depth {self.node_depth(node)}.")

                if (node_limit is not None) and (total_expanded >= node_limit):                    
                    return total_expanded
            
            # If the node has sufficient depth limit, we can 
            # explore its successors (if they are not visited).

            if (depth is None) or (depth > 0):
                new_depth = (depth - 1) if (depth is not None) else None
                for s in self.G.successors(node):
                    if s not in visited:
                        bfs_queue.append((s, new_depth))

        return total_expanded

    def _expand_one(self, node_id: int):
        """
        An internal method to expand a single node of the succession diagram.

        This entails computing the maximal trap spaces within the node (stable motifs) 
        and creating a node for the result (if it does not exist).

        If the node is already expanded, the method does nothing.
        """
        if node_id in self.expanded:
            return
        
        # TODO: This method should use self.petri_net instead of self.network for optimal performance.

        current_space = self.node_space(node_id)

        if len(current_space) == self.network.num_vars():
            # This node is a fixed-point. Trappist would just
            # return this fixed-point again. No need to continue.
            if DEBUG:
                print(f"Found fixed-point: {current_space}")
            return

        if DEBUG:
            print(f"[{node_id}] Expanding: {len(self.node_space(node_id))} fixed vars.")
        
        sub_spaces = trappist(
            self.network, 
            problem="max", 
            ensure_subspace=current_space, 
            petri_net=self.petri_net
        )

        if len(sub_spaces) == 0:
            if DEBUG:
                print(f"Found minimum trap space: {current_space}")
            return

        if DEBUG:
            print(f"Sub-spaces: {len(sub_spaces)}")

        for sub_space in sub_spaces:    
            child_id = self.ensure_node(node_id, sub_space)
            
            #if DEBUG:
            #    print(f"[{node_id}] Found child {child_id}: {sub_space} => {self.node_space(child_id)}")

        
        # TODO: These are ideas for the "partial order reduction".
        #print(f"Found {len(sub_spaces)} sub-spaces.")
        #branch_on = sub_spaces[0]
        #child_id = self.ensure_node(node_id, branch_on)
        #print(f"[{node_id}] Found main child {child_id}: {len(branch_on)}")

        #for sub_space in sub_spaces[1:]:
        #    intersection = intersect(sub_space, branch_on)
        #    if intersection is None:
        #        child_id = self.ensure_node(node_id, sub_space)
        #        print(f"[{node_id}] Found conflict child {child_id}: {len(sub_space)}")


    def ensure_node(self, parent_id: int | None, stable_motif: dict[str, int]) -> int:
        """
        Ensure that the provided node is present in this succession diagram as a child of the given `parent_id`.
        The `stable_motif` is an "initial" trap space that is then percolated to compute the actual fixed
        variables for this node.

        The method also ensures the depth of the node is at least `depth[parent_id] + 1`.
        If the `parent_id` is not given, no edge is created and depth is considered to be zero.
        
        Note that this logic ensures that the depth of every node is always larger than the depth of its 
        predecessors.
        """

        fixed_vars, _ = percolate_space(self.network, stable_motif, strict_percolation=False)

        # Key is a binary encoding of the fixed_vars dictionary. Since Python has
        # arbitrary-precision integers, this should work for any network and be 
        # reasonably fast (we are not doing any copies or string manipulation).
        key = 0
        for (k, v) in fixed_vars.items():
            var_index = self.network.find_variable(k).as_index()
            # Each variable is encoded as two bits, so the total length
            # of the key is 2 * n and the offset of each variable is 2 * index.
            # 00 - unknown; 10 - zero; 11 - one                             
            key |= (v + 2) << (2 * var_index)

        depth = (self.node_depth(parent_id) + 1) if (parent_id is not None) else 0

        if key not in self.node_indices:
            new_id = self.G.number_of_nodes()
            self.G.add_node(new_id, fixed_vars=fixed_vars, depth=depth)
            self.node_indices[key] = new_id
            if parent_id is not None:
                self.G.add_edge(parent_id, new_id, motif=stable_motif)                        
            return new_id
        else:
            existing_id = self.node_indices[key]
            self.node_depth(existing_id, depth)
            if (parent_id is not None) and (not self.G.has_edge(parent_id, existing_id)):
                self.G.add_edge(parent_id, existing_id, notif=stable_motif)
            return existing_id
        
    def expand_attractors(self, node_id: int) -> list[dict[str, int]]:
        """
        Compute the list of attractor "seed" vertices associated with the given `node_id`. 
        If the attractors are already known, simply return the known result.

        Note that (at the moment), this method is not recursive. I.e. if does not return the 
        attractors of any successor nodes for the given `node_id`.
        """

        if node_id in self.attr_expanded:
            if node_id in self.attractors:
                return self.attractors[node_id]
            else:
                return []

        node_space = self.node_space(node_id)

        self.attr_expanded.add(node_id)

        if len(node_space) == self.network.num_vars():
            # This node is a fixed-point.
            self.attractors[node_id] = [node_space]
            return [node_space]

        # Fix everything in the NFVS to zero, as long as 
        # it isn't already fixed by our `node_space`.
        #
        # We add the whole node space to the retain set because we know
        # the space is a trap and this will remove the corresponding unnecessary
        # Petri net transitions.
        retained_set = node_space.copy()
        for x in self.nfvs:
            if x not in retained_set:
                retained_set[x] = 0

        if len(retained_set) == self.network.num_vars():
            # There is only a single attractor remaining here, 
            # and its "seed" is the retain set.            
            self.attractors[node_id] = [retained_set]
            return [retained_set]

        child_spaces = [self.node_space(child) for child in self.G.successors(node_id)]
        terminal_restriction_space = ~state_list_to_bdd(child_spaces)

        #print(f"Retained: {len(retained_set)}; Node space: {len(node_space)}")

        candidate_seeds = compute_fixed_point_reduced_STG(
            self.petri_net, 
            [self.network.get_variable_name(v) for v in self.network.variables()], 
            retained_set,
            ensure_subspace=node_space,
            avoid_subspaces=child_spaces
        )

        if DEBUG:
            print(f"[id={node_id};children={len(child_spaces)}] Candidates: {len(candidate_seeds)}")
        
        if len(candidate_seeds) == 1 and len(child_spaces) == 0:
            # If this is a pseudo-minimal trap and there is only one seed,
            # the seed must be valid.
            attractors = candidate_seeds
        else:
            attractors = detect_motif_avoidant_attractors(
                self.network, 
                self.petri_net, 
                candidate_seeds, 
                terminal_restriction_space, 
                max_iterations=1000
            )

        if len(attractors) > 0:
            self.attractors[node_id] = attractors
        
        return attractors

        
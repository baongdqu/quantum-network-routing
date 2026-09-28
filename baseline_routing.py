import numpy as np
from networkx import Graph, dijkstra_path, exception

from sequence.topology.router_net_topo import RouterNetTopo
from sequence.network_management.routing_static import StaticRoutingProtocol
from sequence.kernel.timeline import Timeline
from sequence.constants import SECOND

class HopCountNetTopo(RouterNetTopo):
    """
    Custom Network Topology that implements Hop-Count based baseline routing.
    Instead of using distance as the routing weight, it uses a constant weight of 1
    per link, thus computing the shortest path in terms of number of hops.
    """
    
    def _generate_forwarding_table(self, config: dict):
        """Override the default static routing table generation to use Hop Count."""
        
        # Build the graph representing the network
        graph = Graph()
        for node in config["nodes"]:
            if node["type"] == self.QUANTUM_ROUTER:
                graph.add_node(node["name"])

        # Map BSM (Bell State Measurement) nodes to their connecting routers
        # Here we assign a uniform cost of 1 for hop count routing, instead of distance.
        costs = {}
        for qc in self.qchannels:
            router, bsm = qc.sender.name, qc.receiver
            if bsm not in costs:
                # [router1, hop_count_cost]
                costs[bsm] = [router, 1]
            else:
                # [router1, router2, hop_count_cost]
                costs[bsm] = [router] + costs[bsm]
                costs[bsm][-1] += 1

        # Retrieve the routing protocol of the first router to check its type
        routing_protocol = None
        for q_router in self.nodes[self.QUANTUM_ROUTER]:
            routing_protocol = q_router.network_manager.get_routing_protocol()
            break

        if isinstance(routing_protocol, StaticRoutingProtocol):
            print("[Baseline Routing] Initializing Static Forwarding Tables based on Hop Count.")
            # Add edges with the uniform hop-count weight to the graph
            graph.add_weighted_edges_from(costs.values())
            
            # Compute shortest paths and install forwarding rules
            for src in self.nodes[self.QUANTUM_ROUTER]:
                for dst_name in graph.nodes:
                    if src.name == dst_name:
                        continue
                    try:
                        # Ensure deterministic tie-breaking by ordering src/dst names
                        if dst_name > src.name:
                            path = dijkstra_path(graph, src.name, dst_name)
                        else:
                            path = dijkstra_path(graph, dst_name, src.name)[::-1]
                        
                        next_hop = path[1]
                        # Install the rule in the router's forwarding table
                        routing_protocol = src.network_manager.get_routing_protocol()
                        routing_protocol.add_forwarding_rule(dst_name, next_hop)
                    except exception.NetworkXNoPath:
                        print(f"Warning: No path between {src.name} and {dst_name}")

if __name__ == "__main__":
    # Test the Hop Count Routing initialization
    print("Loading custom Hop Count topology...")
    network_config = "SeQUeNCe/example/demo_for_beginners/star_network.json"
    
    # This automatically invokes _generate_forwarding_table upon initialization
    topo = HopCountNetTopo(network_config)
    print("Baseline Hop-Count Routing tables successfully initialized!")

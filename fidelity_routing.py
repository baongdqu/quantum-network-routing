import numpy as np
from networkx import Graph, dijkstra_path, exception

from sequence.topology.router_net_topo import RouterNetTopo
from sequence.network_management.routing_static import StaticRoutingProtocol

class FidelityAwareNetTopo(RouterNetTopo):
    """
    Custom Network Topology that implements Fidelity-Aware routing.
    Instead of using just distance or hop-count, it uses a metric that 
    estimates the fidelity degradation.
    
    In optical fiber, fidelity loss is roughly proportional to the total attenuation.
    Therefore, minimizing (distance * attenuation_rate) effectively maximizes 
    the end-to-end fidelity of the path.
    """
    
    def _generate_forwarding_table(self, config: dict):
        """Override the default static routing table generation to be Fidelity-Aware."""
        
        # Build the graph representing the network
        graph = Graph()
        for node in config["nodes"]:
            if node["type"] == self.QUANTUM_ROUTER:
                graph.add_node(node["name"])

        # Map BSM nodes to their connecting routers using fidelity-aware weights
        costs = {}
        for qc in self.qchannels:
            router, bsm = qc.sender.name, qc.receiver
            
            # The fidelity penalty metric: distance * attenuation
            # By minimizing this, Dijkstra finds the path with the highest remaining fidelity
            fidelity_penalty = qc.distance * qc.attenuation
            
            if bsm not in costs:
                # [router1, fidelity_penalty]
                costs[bsm] = [router, fidelity_penalty]
            else:
                # [router1, router2, total_fidelity_penalty_across_both_halves]
                costs[bsm] = [router] + costs[bsm]
                costs[bsm][-1] += fidelity_penalty

        routing_protocol = None
        for q_router in self.nodes[self.QUANTUM_ROUTER]:
            routing_protocol = q_router.network_manager.get_routing_protocol()
            break

        if isinstance(routing_protocol, StaticRoutingProtocol):
            print("[Fidelity Routing] Initializing Static Forwarding Tables based on expected Fidelity.")
            # Add edges with the fidelity penalty weight to the graph
            graph.add_weighted_edges_from(costs.values())
            
            # Compute optimal fidelity paths and install forwarding rules
            for src in self.nodes[self.QUANTUM_ROUTER]:
                for dst_name in graph.nodes:
                    if src.name == dst_name:
                        continue
                    try:
                        if dst_name > src.name:
                            path = dijkstra_path(graph, src.name, dst_name)
                        else:
                            path = dijkstra_path(graph, dst_name, src.name)[::-1]
                        
                        next_hop = path[1]
                        routing_protocol = src.network_manager.get_routing_protocol()
                        routing_protocol.add_forwarding_rule(dst_name, next_hop)
                    except exception.NetworkXNoPath:
                        print(f"Warning: No path between {src.name} and {dst_name}")

if __name__ == "__main__":
    # Test the Fidelity-Aware Routing initialization
    print("Loading custom Fidelity-Aware topology...")
    network_config = "SeQUeNCe/example/demo_for_beginners/star_network.json"
    
    topo = FidelityAwareNetTopo(network_config)
    print("Fidelity-Aware Routing tables successfully initialized!")

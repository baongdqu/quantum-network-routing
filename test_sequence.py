from sequence.kernel.timeline import Timeline
from sequence.topology.router_net_topo import RouterNetTopo
import time

def test_simulation():
    print("Setting up simulation...")
    # Initialize the simulation timeline
    tl = Timeline(2e12) # 2 seconds simulation stop time

    # Build the topology from JSON
    # Pointing to the cloned example JSON
    network_config = "SeQUeNCe/example/demo_for_beginners/star_network.json"
    print(f"Loading topology from {network_config}...")
    topo = RouterNetTopo(network_config)
    
    # Init the timeline on the topology
    tl.init()
    
    # Just running a short bit of time to ensure it does not crash
    print("Starting simulation...")
    start_time = time.time()
    tl.run()
    end_time = time.time()
    
    print(f"Simulation completed successfully in {end_time - start_time:.2f} seconds!")
    print(f"Nodes successfully initialized: {[n for n in topo.nodes]}")

if __name__ == "__main__":
    test_simulation()

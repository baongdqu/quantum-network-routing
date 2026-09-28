import time
import pandas as pd
from sequence.constants import SECOND
from sequence.topology.router_net_topo import RouterNetTopo
from sequence.app.random_request import RandomRequestApp

# Import our custom topologies
from baseline_routing import HopCountNetTopo
from fidelity_routing import FidelityAwareNetTopo

def set_parameters(topology, simulation_time, attenuation):
    """Sets standard simulation parameters across both topologies for a fair comparison."""
    PS_PER_MS = 1e9
    
    # set timeline stop time
    topology.get_timeline().stop_time = (simulation_time * PS_PER_MS)
    
    # set memory parameters
    MEMO_FREQ = 2e3
    MEMO_EXPIRE = 0
    MEMO_EFFICIENCY = 1
    MEMO_FIDELITY = 0.95
    for node in topology.get_nodes_by_type(RouterNetTopo.QUANTUM_ROUTER):
        memory_array = node.get_components_by_type("MemoryArray")[0]
        memory_array.update_memory_params("frequency", MEMO_FREQ)
        memory_array.update_memory_params("coherence_time", MEMO_EXPIRE)
        memory_array.update_memory_params("efficiency", MEMO_EFFICIENCY)
        memory_array.update_memory_params("raw_fidelity", MEMO_FIDELITY)

    # set detector parameters
    DETECTOR_EFFICIENCY = 0.9
    DETECTOR_COUNT_RATE = 5e7
    DETECTOR_RESOLUTION = 100
    for node in topology.get_nodes_by_type(RouterNetTopo.BSM_NODE):
        bsm = node.get_components_by_type("SingleAtomBSM")[0]
        bsm.update_detectors_params("efficiency", DETECTOR_EFFICIENCY)
        bsm.update_detectors_params("count_rate", DETECTOR_COUNT_RATE)
        bsm.update_detectors_params("time_resolution", DETECTOR_RESOLUTION)
        
    # set quantum channel parameters
    QC_FREQ = 1e11
    for qc in topology.qchannels:
        qc.attenuation = attenuation
        qc.frequency = QC_FREQ

def run_simulation(topo_class, network_config, sim_time_ms, qc_atten):
    """Runs the simulation for a specific topology class and returns collected metrics."""
    network_topo = topo_class(network_config)
    set_parameters(network_topo, sim_time_ms, qc_atten)
    
    # construct random request applications
    quantum_router_nodes = network_topo.get_nodes_by_type(RouterNetTopo.QUANTUM_ROUTER)
    node_names = [node.name for node in quantum_router_nodes]
    apps = []
    
    for i, (name, node) in enumerate(zip(node_names, quantum_router_nodes)):
        other_nodes = node_names[:]
        other_nodes.remove(name)
        # Create random request app generating entanglement requests
        app = RandomRequestApp(node, other_nodes, i,
                               min_dur=0.4e12, max_dur=0.5e12, min_size=1,
                               max_size=5, min_fidelity=0.8, max_fidelity=0.85)
        apps.append(app)
        app.start()
    
    # run the simulation
    tl = network_topo.get_timeline()
    tl.show_progress = False
    tl.init()
    
    print(f"Running simulation with {topo_class.__name__}...")
    tick = time.time()
    tl.run()
    run_time = time.time() - tick
    
    # Extract reservation metrics
    metrics = []
    for node in network_topo.get_nodes_by_type(RouterNetTopo.QUANTUM_ROUTER):
        node_name = node.name
        for reservation in node.network_manager.protocol_stack[1].accepted_reservations:
            s_t = reservation.start_time / SECOND
            e_t = reservation.end_time / SECOND
            size = reservation.memory_size
            if reservation.initiator != node.name and reservation.responder != node.name:
                size *= 2
            
            # Record fidelity metric (min requested fidelity)
            fidelity = reservation.fidelity
            
            metrics.append({
                "Policy": topo_class.__name__,
                "Node": node_name,
                "Start Time (s)": s_t,
                "End Time (s)": e_t,
                "Duration (s)": e_t - s_t,
                "Memory Size": size,
                "Fidelity Target": fidelity
            })
            
    return metrics, run_time

if __name__ == "__main__":
    network_config = "SeQUeNCe/example/demo_for_beginners/star_network.json"
    sim_time_ms = 3000  # 3 seconds simulation time
    qc_atten = 1e-4     # standard attenuation
    
    all_metrics = []
    
    # Run Baseline (Hop-Count)
    metrics_baseline, rt_base = run_simulation(HopCountNetTopo, network_config, sim_time_ms, qc_atten)
    all_metrics.extend(metrics_baseline)
    print(f"Baseline finished in {rt_base:.2f} seconds.\n")
    
    # Run Fidelity-Aware
    metrics_fidelity, rt_fid = run_simulation(FidelityAwareNetTopo, network_config, sim_time_ms, qc_atten)
    all_metrics.extend(metrics_fidelity)
    print(f"Fidelity-Aware finished in {rt_fid:.2f} seconds.\n")
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(all_metrics)
    
    if df.empty:
        print("No reservations were successfully established during the simulations.")
    else:
        # Save raw benchmark data
        df.to_csv("benchmark_results.csv", index=False)
        print("Benchmarking Complete! Saved results to 'benchmark_results.csv'")
        
        # Summary statistics
        summary = df.groupby("Policy").agg({
            "Duration (s)": ["mean", "sum"],
            "Memory Size": ["sum", "mean"]
        })
        print("\n--- Summary Statistics ---")
        print(summary)

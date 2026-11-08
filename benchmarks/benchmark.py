import sys
import time
from pathlib import Path
import pandas as pd

# Add project root and src/ to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from sequence.constants import SECOND
from sequence.topology.router_net_topo import RouterNetTopo
from sequence.app.random_request import RandomRequestApp

# Import custom topologies from src
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
    for qc in topology.get_qchannels():
        if attenuation is not None:
            qc.attenuation = attenuation

def run_simulation(topology_class, config_file, simulation_time_ms=1000, attenuation=1e-5):
    """Initializes and executes the simulation for a specific topology."""
    # Resolve config file path if relative
    config_path = Path(config_file)
    if not config_path.is_absolute() and not config_path.exists():
        if (PROJECT_ROOT / "configs" / config_file).exists():
            config_path = PROJECT_ROOT / "configs" / config_file
        elif (PROJECT_ROOT / config_file).exists():
            config_path = PROJECT_ROOT / config_file

    topo_name = topology_class.__name__
    print(f"[{topo_name}] Initializing simulation with config: {config_path}")
    
    # Pass resolved string path to SeQUeNCe
    topology = topology_class(str(config_path))
    set_parameters(topology, simulation_time_ms, attenuation)

    # Attach random request applications to end routers
    start_time = 1 * SECOND
    end_time = (simulation_time_ms / 1000) * SECOND
    
    # Connect applications
    for node_name in ["router_1", "router_2", "router_3", "router_4"]:
        node = topology.get_nodes_by_type(RouterNetTopo.QUANTUM_ROUTER)
        target_nodes = [n for n in node if n.name == node_name]
        if target_nodes:
            app = RandomRequestApp(target_nodes[0], [n.name for n in node if n.name != node_name],
                                  10, 100, 500, start_time, end_time, 1, 0.9)
            app.start()

    tl = topology.get_timeline()
    tl.init()
    
    t_start = time.time()
    tl.run()
    runtime = time.time() - t_start

    # Extract metrics
    metrics = []
    for node in topology.get_nodes_by_type(RouterNetTopo.QUANTUM_ROUTER):
        rsvp = node.network_manager.protocol_stack[0] # ReservationProtocol
        for card in rsvp.approved_reservations:
            metrics.append({
                "Policy": topo_name,
                "Node": node.name,
                "Initiator": card.initiator,
                "Responder": card.responder,
                "Memory Size": card.memory_size,
                "Duration (s)": (card.end_time - card.start_time) / SECOND
            })
            
    return metrics, runtime

if __name__ == "__main__":
    configs_file = PROJECT_ROOT / "configs" / "asymmetric_network.json"
    sim_time_ms = 1000
    
    # Run Baseline
    metrics_base, time_base = run_simulation(HopCountNetTopo, str(configs_file), sim_time_ms)
    
    # Run Fidelity-Aware
    metrics_fid, time_fid = run_simulation(FidelityAwareNetTopo, str(configs_file), sim_time_ms)
    
    # Save combined results
    all_metrics = metrics_base + metrics_fid
    df = pd.DataFrame(all_metrics)
    
    output_csv = PROJECT_ROOT / "results" / "data" / "benchmark_results.csv"
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    
    print("\n" + "="*50)
    print("BENCHMARK EXECUTION SUMMARY")
    print("="*50)
    print(f"Hop-Count Runtime     : {time_base:.2f} seconds")
    print(f"Fidelity-Aware Runtime: {time_fid:.2f} seconds")
    print(f"Total metrics recorded: {len(all_metrics)}")
    print(f"Results written to    : {output_csv}")

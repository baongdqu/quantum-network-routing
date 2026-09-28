import time
import pandas as pd
from sequence.constants import SECOND
from sequence.topology.router_net_topo import RouterNetTopo
from sequence.app.random_request import RandomRequestApp

def set_parameters(topology, simulation_time, attenuation):
    PS_PER_MS = 1e9
    topology.get_timeline().stop_time = (simulation_time * PS_PER_MS)
    
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

    DETECTOR_EFFICIENCY = 0.9
    DETECTOR_COUNT_RATE = 5e7
    DETECTOR_RESOLUTION = 100
    for node in topology.get_nodes_by_type(RouterNetTopo.BSM_NODE):
        bsm = node.get_components_by_type("SingleAtomBSM")[0]
        bsm.update_detectors_params("efficiency", DETECTOR_EFFICIENCY)
        bsm.update_detectors_params("count_rate", DETECTOR_COUNT_RATE)
        bsm.update_detectors_params("time_resolution", DETECTOR_RESOLUTION)
        
    QC_FREQ = 1e11
    for qc in topology.qchannels:
        qc.attenuation = attenuation
        qc.frequency = QC_FREQ

def test():
    network_config = "SeQUeNCe/example/demo_for_beginners/star_network.json"
    network_topo = RouterNetTopo(network_config)
    set_parameters(network_topo, 3000, 1e-4)
    
    quantum_router_nodes = network_topo.get_nodes_by_type(RouterNetTopo.QUANTUM_ROUTER)
    node_names = [node.name for node in quantum_router_nodes]
    apps = []
    for i, (name, node) in enumerate(zip(node_names, quantum_router_nodes)):
        other_nodes = node_names[:]
        other_nodes.remove(name)
        app = RandomRequestApp(node, other_nodes, i,
                               min_dur=0.4e12, max_dur=0.5e12, min_size=1,
                               max_size=5, min_fidelity=0.8, max_fidelity=0.85)
        apps.append(app)
        app.start()
    
    tl = network_topo.get_timeline()
    tl.show_progress = True
    tl.init()
    print("Initial events in timeline:", len(tl.events))
    tick = time.time()
    tl.run()
    print("Execution time: %.2f sec" % (time.time() - tick))
    
    for app in apps:
        print("Node", app.node.name, "reservations:", len(app.reserves))

if __name__ == "__main__":
    test()

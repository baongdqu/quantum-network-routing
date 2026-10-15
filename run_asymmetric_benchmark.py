import time
import pandas as pd
import matplotlib.pyplot as plt
from baseline_routing import HopCountNetTopo
from fidelity_routing import FidelityAwareNetTopo
from benchmark import run_simulation

def run_experiment():
    network_config = "asymmetric_network.json"
    sim_time_ms = 4000  # 4 seconds
    qc_atten = None     # Use individual channel attenuations from JSON
    
    print("="*60)
    print("🚀 RUNNING ASYMMETRIC QUANTUM NETWORK BENCHMARK (SeQUeNCe)")
    print("="*60)
    
    # 1. Run Baseline (Hop-Count)
    print("\n[1/2] Running Hop-Count Baseline...")
    metrics_baseline, rt_base = run_simulation(HopCountNetTopo, network_config, sim_time_ms, qc_atten)
    print(f"-> Hop-Count completed in {rt_base:.2f}s | Reservations: {len(metrics_baseline)}")
    
    # 2. Run Fidelity-Aware
    print("\n[2/2] Running Fidelity-Aware Routing...")
    metrics_fidelity, rt_fid = run_simulation(FidelityAwareNetTopo, network_config, sim_time_ms, qc_atten)
    print(f"-> Fidelity-Aware completed in {rt_fid:.2f}s | Reservations: {len(metrics_fidelity)}")
    
    all_metrics = metrics_baseline + metrics_fidelity
    df = pd.DataFrame(all_metrics)
    
    if df.empty:
        print("\n[!] No reservations established. Try increasing simulation time or adjusting attenuation.")
        return
        
    df.to_csv("benchmark_asymmetric_results.csv", index=False)
    print("\n✅ Results saved to 'benchmark_asymmetric_results.csv'")
    
    # Generate summary
    summary = df.groupby("Policy").agg({
        "Duration (s)": ["mean", "count"],
        "Memory Size": ["sum", "mean"]
    })
    print("\n--- Summary Statistics ---")
    print(summary)
    
    # Generate plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Total Entanglement Memory Throughput
    mem_sum = df.groupby("Policy")["Memory Size"].sum()
    axes[0].bar(mem_sum.index, mem_sum.values, color=['#e74c3c', '#2ecc71'], width=0.5)
    axes[0].set_title("Total Entangled Memory Delivered (Higher is Better)")
    axes[0].set_ylabel("Total Reserved Quantum Memories")
    for i, v in enumerate(mem_sum.values):
        axes[0].text(i, v + 0.5, str(int(v)), ha='center', fontweight='bold')
        
    # Plot 2: Average Reservation Duration / Latency
    dur_mean = df.groupby("Policy")["Duration (s)"].mean()
    axes[1].bar(dur_mean.index, dur_mean.values, color=['#e74c3c', '#2ecc71'], width=0.5)
    axes[1].set_title("Average Reservation Duration (s)")
    axes[1].set_ylabel("Duration in Seconds")
    for i, v in enumerate(dur_mean.values):
        axes[1].text(i, v * 1.02, f"{v:.3f}s", ha='center', fontweight='bold')
        
    plt.tight_layout()
    plt.savefig("asymmetric_routing_comparison.png", dpi=300)
    print("📊 Generated chart: 'asymmetric_routing_comparison.png'")

if __name__ == "__main__":
    run_experiment()

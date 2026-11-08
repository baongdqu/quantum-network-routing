import sys
import time
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Add project root and src/ to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from baseline_routing import HopCountNetTopo
from fidelity_routing import FidelityAwareNetTopo
from benchmarks.benchmark import run_simulation

def run_experiment():
    network_config = PROJECT_ROOT / "configs" / "asymmetric_network.json"
    sim_time_ms = 4000  # 4 seconds
    qc_atten = None     # Use individual channel attenuations from JSON
    
    print("="*60)
    print("🚀 RUNNING ASYMMETRIC QUANTUM NETWORK BENCHMARK (SeQUeNCe)")
    print("="*60)
    
    # 1. Run Baseline (Hop-Count)
    print("\n[1/2] Running Hop-Count Baseline...")
    metrics_baseline, rt_base = run_simulation(HopCountNetTopo, str(network_config), sim_time_ms, qc_atten)
    print(f"-> Hop-Count completed in {rt_base:.2f}s | Reservations: {len(metrics_baseline)}")
    
    # 2. Run Fidelity-Aware
    print("\n[2/2] Running Fidelity-Aware Routing...")
    metrics_fidelity, rt_fid = run_simulation(FidelityAwareNetTopo, str(network_config), sim_time_ms, qc_atten)
    print(f"-> Fidelity-Aware completed in {rt_fid:.2f}s | Reservations: {len(metrics_fidelity)}")
    
    all_metrics = metrics_baseline + metrics_fidelity
    df = pd.DataFrame(all_metrics)
    
    if df.empty:
        print("\n[!] No reservations established. Try increasing simulation time or adjusting attenuation.")
        return
        
    output_csv = PROJECT_ROOT / "results" / "data" / "benchmark_asymmetric_results.csv"
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Results saved to '{output_csv}'")
    
    # Generate summary
    summary = df.groupby("Policy").agg({
        "Duration (s)": ["mean", "count"],
        "Memory Size": ["sum", "mean"]
    })
    
    print("\n" + "="*60)
    print("📊 EMPIRICAL SUMMARY TABLE")
    print("="*60)
    print(summary)
    
    # Plotting comparison
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Throughput (Total Memory Size Delivered)
    mem_sum = df.groupby("Policy")["Memory Size"].sum()
    colors = ['#e74c3c' if p == 'HopCountNetTopo' else '#2ecc71' for p in mem_sum.index]
    bars1 = axes[0].bar(mem_sum.index, mem_sum.values, color=colors, width=0.5)
    axes[0].set_title("Total Entangled Memory Delivered (Higher is Better)", fontsize=11, fontweight='bold')
    axes[0].set_ylabel("Total Reserved Quantum Memories")
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)
    for bar in bars1:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{int(yval)}", ha='center', va='bottom', fontweight='bold')
        
    # Latency / Reservation Duration
    dur_mean = df.groupby("Policy")["Duration (s)"].mean()
    bars2 = axes[1].bar(dur_mean.index, dur_mean.values, color=colors, width=0.5)
    axes[1].set_title("Average Reservation Duration (s)", fontsize=11, fontweight='bold')
    axes[1].set_ylabel("Duration in Seconds")
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)
    for bar in bars2:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2.0, yval + 0.01, f"{yval:.3f}s", ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    output_fig = PROJECT_ROOT / "results" / "figures" / "asymmetric_routing_comparison.png"
    output_fig.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_fig, dpi=300)
    print(f"✅ Comparison plot saved to '{output_fig}'")

if __name__ == "__main__":
    run_experiment()

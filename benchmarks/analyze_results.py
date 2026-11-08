import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def main():
    csv_path = PROJECT_ROOT / "results" / "data" / "benchmark_results.csv"
    if not csv_path.exists():
        print(f"Data file not found at: {csv_path}. Did you run benchmark.py?")
        return

    df = pd.read_csv(csv_path)
    if df.empty:
        print("No data in benchmark_results.csv")
        return

    # Calculate mean metrics per policy
    summary = df.groupby("Policy").agg({
        "Duration (s)": "mean",
        "Memory Size": "sum"
    }).reset_index()

    # Create figure and axis objects
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Average Reservation Duration (Latency)
    ax1.bar(summary["Policy"], summary["Duration (s)"], color=['#1f77b4', '#ff7f0e'])
    ax1.set_title("Average Entanglement Reservation Duration")
    ax1.set_ylabel("Duration (Seconds)")
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Plot 2: Total Memory Sized Reserved (Throughput proxy)
    ax2.bar(summary["Policy"], summary["Memory Size"], color=['#2ca02c', '#d62728'])
    ax2.set_title("Total Reserved Entanglement Memory")
    ax2.set_ylabel("Total Memory Size")
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    output_png = PROJECT_ROOT / "results" / "figures" / "routing_comparison.png"
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png, dpi=300)
    print(f"Comparison plot successfully saved to '{output_png}'")

if __name__ == "__main__":
    main()

import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Try importing tkinter for GUI
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

from benchmark import run_simulation
from baseline_routing import HopCountNetTopo
from fidelity_routing import FidelityAwareNetTopo

NETWORK_CONFIG = "SeQUeNCe/example/demo_for_beginners/star_network.json"
SIM_TIME = 3000
ATTENUATION = 1e-4

def run_cli():
    print("="*50)
    print("🔬 QUANTUM ROUTING LABORATORY (CLI) 🔬")
    print("="*50)
    print("1. Run Baseline (Hop-Count) Simulation")
    print("2. Run Fidelity-Aware Simulation")
    print("3. Run Both & Compare")
    print("4. Exit")
    print("="*50)
    
    choice = input("Select an option (1-4): ").strip()
    
    if choice == '1':
        print("\nRunning Baseline Simulation...")
        metrics, rt = run_simulation(HopCountNetTopo, NETWORK_CONFIG, SIM_TIME, ATTENUATION)
        print(f"Finished in {rt:.2f}s")
        df = pd.DataFrame(metrics)
        print(df.groupby("Node")["Duration (s)"].mean() if not df.empty else "No successful reservations.")
        
    elif choice == '2':
        print("\nRunning Fidelity-Aware Simulation...")
        metrics, rt = run_simulation(FidelityAwareNetTopo, NETWORK_CONFIG, SIM_TIME, ATTENUATION)
        print(f"Finished in {rt:.2f}s")
        df = pd.DataFrame(metrics)
        print(df.groupby("Node")["Duration (s)"].mean() if not df.empty else "No successful reservations.")
        
    elif choice == '3':
        print("\nRunning Both Simulations...")
        m1, rt1 = run_simulation(HopCountNetTopo, NETWORK_CONFIG, SIM_TIME, ATTENUATION)
        m2, rt2 = run_simulation(FidelityAwareNetTopo, NETWORK_CONFIG, SIM_TIME, ATTENUATION)
        
        print(f"Baseline finished in {rt1:.2f}s | Fidelity finished in {rt2:.2f}s")
        df = pd.DataFrame(m1 + m2)
        if not df.empty:
            summary = df.groupby("Policy").agg({"Duration (s)": "mean", "Memory Size": "sum"})
            print("\n--- Comparison Summary ---")
            print(summary)
        else:
            print("No reservations.")
            
    elif choice == '4':
        sys.exit(0)
    else:
        print("Invalid choice.")
    
    input("\nPress Enter to return to menu...")
    run_cli()


def run_gui():
    if not GUI_AVAILABLE:
        print("Tkinter is not available. Falling back to CLI.")
        run_cli()
        return

    root = tk.Tk()
    root.title("Quantum Routing Laboratory")
    root.geometry("800x600")

    # Main Frame
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Header
    ttk.Label(main_frame, text="🔬 Quantum Routing Laboratory", font=("Helvetica", 18, "bold")).pack(pady=10)

    # Canvas Frame for Plot
    canvas_frame = ttk.Frame(main_frame)
    canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def display_results(metrics):
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        df = pd.DataFrame(metrics)
        if df.empty:
            ttk.Label(canvas_frame, text="No reservations completed.", foreground="red").pack()
            return
            
        summary = df.groupby("Policy").agg({"Duration (s)": "mean", "Memory Size": "sum"}).reset_index()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        
        ax1.bar(summary["Policy"], summary["Duration (s)"], color=['#1f77b4', '#ff7f0e'])
        ax1.set_title("Avg Duration (Latency)")
        
        ax2.bar(summary["Policy"], summary["Memory Size"], color=['#2ca02c', '#d62728'])
        ax2.set_title("Total Memory (Throughput)")

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_run_baseline():
        status_var.set("Running Baseline...")
        root.update()
        m, _ = run_simulation(HopCountNetTopo, NETWORK_CONFIG, SIM_TIME, ATTENUATION)
        display_results(m)
        status_var.set("Done.")

    def on_run_fidelity():
        status_var.set("Running Fidelity-Aware...")
        root.update()
        m, _ = run_simulation(FidelityAwareNetTopo, NETWORK_CONFIG, SIM_TIME, ATTENUATION)
        display_results(m)
        status_var.set("Done.")

    def on_run_both():
        status_var.set("Running Both...")
        root.update()
        m1, _ = run_simulation(HopCountNetTopo, NETWORK_CONFIG, SIM_TIME, ATTENUATION)
        m2, _ = run_simulation(FidelityAwareNetTopo, NETWORK_CONFIG, SIM_TIME, ATTENUATION)
        display_results(m1 + m2)
        status_var.set("Done.")

    # Controls
    controls = ttk.Frame(main_frame)
    controls.pack(fill=tk.X, pady=10)

    ttk.Button(controls, text="Run Baseline", command=on_run_baseline).pack(side=tk.LEFT, padx=5)
    ttk.Button(controls, text="Run Fidelity", command=on_run_fidelity).pack(side=tk.LEFT, padx=5)
    ttk.Button(controls, text="Run Both & Compare", command=on_run_both).pack(side=tk.LEFT, padx=5)

    status_var = tk.StringVar(value="Ready.")
    ttk.Label(main_frame, textvariable=status_var, font=("Helvetica", 10, "italic")).pack(side=tk.BOTTOM, pady=5)

    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quantum Routing Laboratory")
    parser.add_argument('--cli', action='store_true', help="Run in CLI mode")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        run_gui()

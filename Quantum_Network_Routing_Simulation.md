# Quantum Network Routing Simulation (Project 13)

This project implements and benchmarks routing policies on a simulated quantum network using the [SeQUeNCe](https://github.com/sequence-toolbox/SeQUeNCe) simulator.

Unlike classical routing, which typically relies on hop count, quantum routing must account for fidelity decay at every hop. The core objective of this project is to simulate and compare a baseline **Hop-Count Routing Protocol** against a custom **Fidelity-Aware Routing Protocol**.

## Features

- **Hop-Count Routing:** Evaluates paths based strictly on the shortest physical distance (fewest links).
- **Fidelity-Aware Routing:** Selects paths that minimize the total expected attenuation rate (`distance * attenuation`), which maximizes end-to-end fidelity for entangled pairs.
- **Interactive Laboratory App:** A bundled tool (`laboratory.py`) allowing you to run simulations and compare the outcomes visually or via a command-line interface.

---

## How to Run the Laboratory Application

I have created a complete interactive "Laboratory" application for you! It bundles the benchmarking scripts and the matplotlib visualizations into a unified application that supports both a Command-Line Interface (CLI) and a Graphical User Interface (GUI).

To view and interact with the laboratory, you can run the following commands in your terminal:

### Launch the GUI (Recommended)
This will open a window where you can click buttons to run the baseline, fidelity-aware, or both algorithms back-to-back. It dynamically draws the comparison bar charts directly inside the app!

```powershell
.\venv\Scripts\python.exe laboratory.py
```

### Launch the CLI mode
This will open an interactive text menu directly in your terminal where you can select which simulation to run and see the output tables textually.

```powershell
.\venv\Scripts\python.exe laboratory.py --cli
```

# Project 13: Quantum Network Simulation - Plan

## 1. Project Overview
**Category:** Networking
**Difficulty:** Advanced
**Goal:** Implement and benchmark routing policies on a simulated quantum network. Unlike classical routing where hop count is used, quantum routing must account for fidelity decay at every hop. The core objective is to deliver an end-to-end entangled pair by generating link-level entanglement and swapping it along an optimal path.

## 2. Simulator Selection
**Selected Simulator:** **SeQUeNCe** (Python, discrete-event)
*   *Why this tool?* It is best suited for full-stack simulation of quantum links, systems, and networks, offering a highly modular design.

## 3. Implementation Steps

### Phase 1: Setup and Baseline
*   Set up a Python environment.
*   Install the SeQUeNCe simulator and its dependencies (Python, PyTorch, TensorBoard, pandas, Matplotlib).
*   Run the provided examples/tutorials for SeQUeNCe to establish a working baseline.
*   Define the network topology (e.g., number of nodes, distances, base error rates).

### Phase 2: Core Implementation
*   Implement baseline routing policies (e.g., shortest path based on hop count).
*   Implement fidelity-aware routing policies (e.g., path selection based on end-to-end fidelity estimations).
*   Set up entanglement generation and swapping mechanisms across the chosen paths.

### Phase 3: Benchmarking and Evaluation
*   Run simulations using the different routing policies under identical network conditions.
*   Measure key metrics: end-to-end fidelity, entanglement generation rate (throughput), and latency.
*   Log the data systematically for post-processing.

### Phase 4: Analysis and Reporting
*   Analyze the collected data using `pandas`.
*   Visualize the trade-offs between different routing policies using `Matplotlib`.
*   Summarize the findings, specifically addressing why hop count is insufficient and how fidelity-aware routing improves outcomes.

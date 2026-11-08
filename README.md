# Quantum Network Routing Simulation (Project 13)

[![Course](https://img.shields.io/badge/Course-NT409%20Quantum%20Computing-blue.svg)](https://uit.edu.vn)
[![Framework](https://img.shields.io/badge/Simulator-SeQUeNCe%20(Argonne%20Lab)-purple.svg)](https://github.com/sequence-toolbox/SeQUeNCe)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An academic, full-stack discrete-event quantum network simulation project developing and benchmarking **Fidelity-Aware Quantum Routing** against classical **Hop-Count Baseline (Dijkstra)** routing on asymmetric quantum mesh topologies using **SeQUeNCe** (Argonne National Laboratory).

---

## 📁 Project Directory Structure

```
quantum-network-routing/
├── configs/                          # Network topology JSON specifications
│   └── asymmetric_network.json       # 5-node asymmetric quantum mesh
│
├── src/                              # Core routing algorithms & custom topologies
│   ├── __init__.py
│   ├── baseline_routing.py           # Hop-Count Baseline routing (Dijkstra)
│   ├── fidelity_routing.py           # Fidelity-Aware routing (-ln(T) metric)
│   ├── draw_custom.py                # Quantum network topology visualizer
│   └── laboratory.py                 # Interactive GUI/CLI simulation suite
│
├── benchmarks/                       # Automated simulation & benchmark runners
│   ├── run_asymmetric_benchmark.py   # Asymmetric routing benchmark runner
│   ├── benchmark.py                  # Symmetric star topology runner
│   └── analyze_results.py            # Result aggregation & plotting script
│
├── results/                          # Simulation outputs & publication figures
│   ├── data/
│   │   ├── benchmark_results.csv
│   │   └── benchmark_asymmetric_results.csv
│   └── figures/
│       ├── routing_comparison.png
│       └── asymmetric_routing_comparison.png
│
├── tests/                            # Validation & unit test scripts
│   ├── test_base.py
│   └── test_sequence.py
│
├── docs/                             # Technical reports, strategies & course documentation
│   ├── Báo cáo tiến độ NT409 - Nhóm 10.md    # Midterm progress report (UIT)
│   ├── Phase_4_Analysis_Report.md             # In-depth SeQUeNCe analysis report
│   ├── Cloud_Computing_Integration_Strategy.md# Cloud/Azure scaling blueprint
│   ├── Azure_For_Students_Implementation_Guide.md
│   └── comparison/                           # Head-to-head comparison with Qiskit/QuNetSim
│       ├── comparison_report_vi.md           (Vietnamese version)
│       └── comparison_report_en.md           (English version)
│
├── presentation/                     # Defense slide deck
│   └── slides_presentation.html      # Interactive HTML slides (KaTeX + Vintage theme)
│
├── scratch/                          # Working scratchpad & historical records
│   ├── legacy_docs/                  (Initial project plans & early guides)
│   ├── screenshots/                  (Verification screenshots & team records)
│   └── course_raw/                   (Course syllabus, forms & project proposals)
│
├── Huy/                              # Team member Huy's analysis workspace
│   └── analysis.md
│
├── SeQUeNCe/                         # Core discrete-event simulation submodule
├── quantum_network_simulation_0708/  # Peer reference benchmark submodule
│
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Environment Setup
Clone the repository with submodules:
```bash
git clone --recurse-submodules https://github.com/baongdqu/quantum-network-routing.git
cd quantum-network-routing
pip install -r requirements.txt
```

### 2. Running Simulations & Benchmarks
Execute the asymmetric routing comparison:
```bash
python benchmarks/run_asymmetric_benchmark.py
```

Run the interactive Laboratory application (GUI / CLI):
```bash
python src/laboratory.py
# Or terminal CLI mode:
python src/laboratory.py --cli
```

### 3. Viewing the Defense Presentation
Open the interactive slide deck in any browser:
```bash
start presentation/slides_presentation.html
```
- Press `F` to toggle full-screen presentation mode.
- Use arrow keys `←` / `→` or `Space` to navigate through slides.

---

## 📊 Key Findings Summary

| Evaluation Metric | Hop-Count Baseline | Fidelity-Aware Routing | Improvement / Advantage |
| :--- | :---: | :---: | :--- |
| **Path Selected** | $N_1 \to N_0 \to N_3$ (2 hops) | $N_1 \to N_2 \to N_4 \to N_3$ (3 hops) | Takes 3 clean hops over 2 noisy hops |
| **Cumulative Loss ($-\sum \ln T$)** | **2.50** ($T = 8.2\%$) | **0.30** ($T = 74.1\%$) | **Loss reduced by > 8.3x** |
| **Delivered Memories (Throughput)** | 102 memories | 114 memories | **Fidelity-Aware increases +11.8%** |
| **Simulation Runtime** | 25.63 s | 12.35 s | **Fidelity-Aware is 2x faster** |

---

## 👥 Contributors (Team 10 - NT409)
- **Nguyễn Gia Huy** - Student ID: `25520708`
- **Văn Cấp Tiến Dũng** - Student ID: `25520387`
- **Nguyễn Duy Quốc Bảo** - Student ID: `23520119`
- **Instructor:** M.Sc. Phan Trung Phát (VNUHCM - University of Information Technology)

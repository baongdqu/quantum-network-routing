# Quantum Routing Analysis Report

## Summary of Findings
The benchmark simulated two routing protocols on the `star_network.json` topology:
1. **HopCountNetTopo (Baseline):** Routes traffic based strictly on the fewest physical links (hop-count).
2. **FidelityAwareNetTopo:** Routes traffic by minimizing the total expected attenuation (`distance * attenuation`), which maximizes end-to-end fidelity.

---

## 1. Understanding the Metrics
When the simulator runs, it pretends that the routers are constantly requesting to share quantum entanglement with each other. We measured two key performance indicators:
*   **Average Duration (Latency):** This is the average time (in seconds) it took for the network to successfully create and lock in a quantum entanglement link between two routers. A lower number is better because it means the connection was established faster.
*   **Total Memory Size (Throughput):** This represents how many "quantum memories" were successfully entangled and reserved across the entire simulation. A higher number is better because it means more entanglement was successfully delivered (higher bandwidth).

## 2. Why the Results are Identical
If you look at the benchmark results, you will notice that both routing algorithms achieved the exact same average duration and total memory size. This happened because of the specific network map we used to test them: the **`star_network.json`**. 

Imagine a perfectly symmetrical star: there is one central router, and four edge routers connected to it. Every single connection is exactly the same length (500 km) and has the exact same fiber-optic quality.

*   **How Hop-Count saw it:** "To get from Router 1 to Router 2, I have to go through the center. That is exactly 2 hops."
*   **How Fidelity-Aware saw it:** "To get from Router 1 to Router 2, I have to go through the center which costs a total of 1000km of attenuation loss. There are no better alternatives."

Because the network was perfectly balanced and symmetrical, **both algorithms independently calculated that the exact same path was the best path.** Since both algorithms ended up routing the traffic through the exact same cables, the simulator output identical performance numbers for both.

## 3. Why is Hop-Count Insufficient in Real Quantum Networks?
While hop-count worked perfectly in this small, symmetrical test environment, real-world quantum networks are highly heterogeneous and messy. 

Imagine Router A and Router B are connected by two possible paths:
1.  **Path 1 (1 Hop):** A direct 100km cable, but it's very old and noisy (high attenuation loss).
2.  **Path 2 (2 Hops):** A path that goes through an intermediate Router C, using two brand-new, ultra-clear 20km cables.

Here is where the algorithms would behave differently:
*   **Hop-Count is naive:** It would say: *"Path 1 is only 1 hop! I'm taking that one!"* Because the cable is so noisy, the quantum signal would degrade, and the latency would skyrocket or the connection would fail entirely.
*   **Fidelity-Aware is smart:** It looks at the actual quality of the cables and says: *"Path 1 is too noisy. Even though Path 2 requires an extra hop, the total signal loss is much lower."* It routes the traffic through Path 2, delivering a fast, high-quality entangled connection.

A pure hop-count algorithm will naively choose the shortest physical path, resulting in unusable, heavily decohered entanglement in unbalanced networks. The **Fidelity-Aware** algorithm correctly assesses the total attenuation and routes the quantum states safely, successfully delivering a high-fidelity entangled pair to the end-users.

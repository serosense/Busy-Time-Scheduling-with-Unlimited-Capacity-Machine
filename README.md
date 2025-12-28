# Busy Time Scheduling (Unlimited Capacity)

This project implements a **Dynamic Programming** algorithm to solve the *Busy Time Scheduling* problem on a machine with unlimited capacity. The goal is to optimize the usage of a high-power machine by minimizing the total time it remains turned on ("busy time") while ensuring all jobs are completed within their specific time windows.

The solution is based on the paper *"Real-time scheduling to minimize machine busy times"* (Khandekar et al., 2015)

## Problem Description

We are given a set of $n$ jobs. Each job $i$ is defined by three integers:
* $r_i$: Release time.
* $d_i$: Deadline.
* $p_i$: Processing time (where $p_i \le d_i - r_i$).

The algorithm calculates a start time $s_i$ for each job such that $r_i \le s_i$ and $s_i + p_i \le d_i$. The objective is to minimize the measure of the union of all execution intervals, effectively minimizing the total time the machine is active

## Algorithm Implementation

The solution is implemented in **Python** using a recursive Dynamic Programming approach with Memoization.

### Logic & Complexity
Per the project requirements, the algorithm is **pseudopolynomial**. It redefines the set of "interesting times" $\mathcal{T}$ to include all integers in the range of the input times. The expected running time is $O(n^2T^2 + nT^3)$.

### Core Functions
1.  **`costs(t1, t2, l, ...)`**: This is the main recursive function. It implements the recurrence relation derived from Lemma 3.4 of the referenced paper.
    * It identifies the "pivot" job with the maximum processing time ($p$) within the current interval $[t_1, t_2)$.
    * It iterates through all valid start times for this job.
    * It recursively calculates the minimum cost for the left $[t_1, t)$ and right $[t+p, t_2)$ sub-intervals.
    * It uses `@lru_cache` for memoization to store optimal substructure results.

2.  **`fit_unscheduled_jobs_into_intervals`**: Since the DP recurrence focuses on "critical" jobs that bridge intervals, a post-processing step is included to greedily place any remaining smaller jobs into the existing busy intervals (gaps) without increasing the total cost.

3.  **`create_full_time_range`**: Generates the discrete time steps required for the pseudopolynomial iteration.

## 💡 Real-World Use Case: The "Infinite Truck" Logistics Problem

To understand the utility of this algorithm, consider a **logistics company** managing a specialized transport truck.
* **The Cost:** Renting the truck costs **$100 per minute** of engine time.
* **The Advantage:** The truck has **unlimited capacity** (it can carry 1 or 1,000 packages simultaneously for the same cost).
* **The Challenge:** Clients have different "Ready Times" ($r_i$) and "Deadlines" ($d_i$).

### The Scenario
You have 4 clients.
* **Clients A, B, C:** Packages ready at **12:00**. Deadline at **18:00**. Trip takes **1 hour**.
* **Client D:** Package ready at **08:00**. Deadline at **10:00**. Trip takes **1 hour**.

#### ❌ Without Optimization (Naive Approach)
1.  Driver services Client D at 08:00. **(Cost: 60 mins)**.
2.  Driver waits. At 12:00, services Client A. **(Cost: +60 mins)**.
3.  Driver returns for Client B at 13:30. **(Cost: +60 mins)**.
4.  Finally, services Client C. **(Cost: +60 mins)**.
* **Total:** 240 minutes of active time. 💸 **Massive Waste.**

#### ✅ With This Algorithm
The system mathematically analyzes the **slack** (flexibility) of every job:
1.  It detects that Clients A, B, and C can be **delayed**. Although ready at 12:00, shifting them to **14:00** aligns them perfectly into a single batch while still meeting the 18:00 deadline.
2.  It recognizes Client D is an outlier that cannot be merged.

**Optimal Schedule:**
* **Batch 1 (08:00 - 09:00):** Transports Client D.
* **Batch 2 (14:00 - 15:00):** Transports A, B, and C simultaneously.
* **Total:** **120 minutes**. 🚀 **50% Cost Reduction.**

---

## 🧠 Algorithmic Deep Dive: Beyond Simple Heuristics

While the example above seems simple, the computational problem is **NP-Hard** in general contexts. Simple "greedy" strategies fail when dependencies cascade. This project solves it using a **Recursive Decision Tree**.

### The "Butterfly Effect" of Scheduling
Consider a scenario with one **Long Job (Pivot)** and several overlapping **Short Jobs**.
* **Pivot Job ($P$):** Length 10. Flexible Window `[0, 30]`.
* **Job A, B, C:** Small jobs scattered across the timeline.

The algorithm must decide where to place $P$. This single decision **fractures** the timeline into two independent sub-problems (Left and Right).

#### The Recursion Logic
If we shift the Pivot $P$ to start at $t=5$:
1.  **Pivot:** Occupies `[5, 15]`.
2.  **Left Sub-problem (`t < 5`):** The algorithm recursively solves the optimal schedule for any job trapped before $t=5$.
3.  **Right Sub-problem (`t > 15`):** The algorithm recursively solves for jobs after $t=15$.
4.  **Overlap Calculation:** It checks which jobs are "swallowed" (covered for free) by the Pivot's interval `[5, 15]`.

[cite_start]The code implements this recurrence relation[cite: 516]:
$$Cost([t_1, t_2), \ell) = \min_{t \in \mathcal{T}} \left( \text{BusyTime}(P, t) + Cost_{Left}(t_1, t) + Cost_{Right}(t+p, t_2) \right)$$

By using **Memoization** (`@lru_cache`), we avoid recalculating these branches, turning an exponential problem into a manageable **Pseudopolynomial** one.

---

## ⚙️ Implementation Details

### Complexity
* [cite_start]**Time Complexity:** $O(n^2 T^2 + n T^3)$[cite: 514].
    * $n$: Number of jobs.
    * $T$: Range of "Interesting Times" (from earliest release to latest deadline).
* This complexity makes the solution highly efficient for bounded time ranges, guaranteeing the **Global Optimum**.

### Code Structure
* **`costs(t1, t2, l)`**: The driver function. Uses Dynamic Programming to find the minimum busy time.
* **`fit_unscheduled_jobs`**: A post-processing heuristic. [cite_start]Since the DP focuses on "interval-bridging" jobs, this function greedily inserts non-critical jobs into existing gaps[cite: 516].
* **`create_full_time_range`**: Discretizes the timeline to ensure mathematical precision.

---

## 🚀 How to Run

### Prerequisites
* Python 3.x
* Standard libraries: `functools`, `typing`, `os`.

### Execution
1.  Clone the repo.
2.  Place input files in the root directory named `instance01.txt`, `instance02.txt`, etc.
3.  Run:
    ```bash
    python Project_CS430.py
    ```

### Input Format
The first line contains $n$ (number of jobs). Following lines contain $r_i, d_i, p_i$:
```text
5
19 31 2
4 8 2
...

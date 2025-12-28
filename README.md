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

## Requirements

* **Language**: Python 3.x 
* **Libraries**: Standard Python libraries (`functools`, `typing`, `os`).

## How to Run

1.  Ensure the script `Project_CS430.py` is in the same directory as your input files.
2.  Input files must be named `instance01.txt`, `instance02.txt`, ..., `instance99.txt`.
3.  Run the script:

```bash
python Project_CS430.py

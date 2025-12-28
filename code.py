from functools import lru_cache
from typing import List, Tuple
import os

class Job:
    def __init__(self, index, r, d, p):
        self.index = index  
        self.r = r          
        self.d = d          
        self.p = p          

## Creates a list of all the interesting times.
def create_full_time_range(jobs):
    min_release_time = min(job.r for job in jobs)
    max_deadline = max(job.d for job in jobs)
    return list(range(min_release_time, max_deadline + 1))

## Returns index of job with maximum p in jobs(t1, t2, l)
def find_job(t1, t2, l, jobs_list): 
    max_p = 0
    max_p_index = -1
    for i in range(len(jobs_list)):
        job = jobs_list[i]
        r, d, p = job.r, job.d, job.p
        if p <= l and p > max_p and (t1 - r < p) and (d - t2 < p):
            max_p = p
            max_p_index = i
    return max_p_index

## Returns all the jobs that have not been scheduled yet
def get_unscheduled_jobs(jobs_list, start_times):
    scheduled_indices = set(start_times.keys())
    unscheduled_jobs = [job for job in jobs_list if job.index not in scheduled_indices]
    return unscheduled_jobs

## Returns all the possible earliest start of the unscheduled inside of the busy intervals
def fit_unscheduled_jobs_into_intervals(unscheduled_jobs, intervals):
    additional_start_times = {}
    for job in unscheduled_jobs:
        r, d, p = job.r, job.d, job.p
        for interval_start, interval_end in intervals:
            earliest_start = max(interval_start, r)
            latest_finish = min(interval_end, d)
            if earliest_start + p <= latest_finish:
                additional_start_times[job.index] = earliest_start
                break 
    return additional_start_times

## Looks for all the busy intervals
def look_fits(jobs_list, start_times):
    intervals = []
    for key, start in start_times.items():
        start_time = start
        finish_time = start + jobs_list[key].p
        intervals.append((start_time, finish_time))
    intervals.sort(key=lambda x: x[0])
    return intervals

start_times = {}

## Calculates the cost
@lru_cache(None)
def costs(t1, t2, l, jobs_list, time_range):
    job_index = find_job(t1, t2, l, jobs_list)
    if job_index == -1:
        return 0
    min_cost = float('inf')
    job = jobs_list[job_index]
    r, d, p = job.r, job.d, job.p

    for start_time in [t for t in time_range if r <= t <= d - p]:
        busy_time = min(p, t2 - t1, t2 - start_time, start_time + p - t1)
        cost_left = costs(t1, start_time, p, jobs_list, time_range)
        cost_right = costs(start_time + p, t2, p, jobs_list, time_range)
        total_cost = busy_time + cost_left + cost_right

        if total_cost < min_cost:
            min_cost = total_cost
            start_times[job.index] = start_time

    return min_cost

## Reads the input instance
def read_input(file_path: str) -> List[Job]:
    jobs = []
    with open(file_path, 'r') as file:
        n = int(file.readline().strip())  # N JOBS
        print(n)
        for i in range(n):
            r, d, p = map(int, file.readline().strip().split())
            jobs.append(Job(i, r, d, p))
    return jobs

## Writes the output solution
def write_output(file_path: str, start_times: dict, jobs: List[Job]):
    with open(file_path, 'w') as file:
        print(start_times)
        for job in jobs:
            file.write(f"{start_times[job.index]}\n")


def busy_time_scheduling(file_input: str, file_output: str):
    global start_times 
    start_times = {}

    jobs = read_input(file_input)
    jobs_list = jobs

    time_range = create_full_time_range(jobs)

    total_cost = costs(0, max(time_range), max(job.p for job in jobs), tuple(jobs), tuple(time_range))
    print("Optimum total cost: ", total_cost)
    
    intervals = look_fits(jobs_list, start_times)
    unscheduled_jobs = get_unscheduled_jobs(jobs_list, start_times)
    additional_start_times = fit_unscheduled_jobs_into_intervals(unscheduled_jobs, intervals)
    all_start_times = {**start_times, **additional_start_times}

    print(all_start_times)

    write_output(file_output, all_start_times, jobs)


def process_all_instances():
    for i in range(100):
        instance_file = f"instance{i:02d}.txt"
        solution_file = f"solution{i:02d}.txt"
        
        if os.path.exists(instance_file):
            print(f"Processing {instance_file}...")
            try:
                busy_time_scheduling(instance_file, solution_file)
                print(f"Solution saved in {solution_file}\n")
            except Exception as e:
                print(f"Error processing {instance_file}: {e}\n")
        else:
            print(f"{instance_file} doesn't exist. Skipping...\n")

process_all_instances()
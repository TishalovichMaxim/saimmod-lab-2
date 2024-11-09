from typing import List
from metrics import AllMetrics
from model import CallPointModel
import numpy as np
import matplotlib.pyplot as plt

def task4():
    model = CallPointModel(1)

    metrics_arr: List[List[AllMetrics]] = []
    simulation_time = 10_000
    n_runs = 1

    for n_call_rooms in range(1, 201):
        model.n_call_rooms = n_call_rooms

        curr_arr: List[AllMetrics] = []
    
        for _ in range(n_runs):
            curr_metrics = model.run(simulation_time)
            print(curr_metrics.avg_queue_len)
            curr_arr.append(curr_metrics)
        
        metrics_arr.append(curr_arr)

    q_len_values = np.empty(len(metrics_arr))
    for i, arr in enumerate(metrics_arr):
        q_len_values[i] = np.mean(list(map(lambda m: m.avg_queue_len, arr)))

    fig, ax = plt.subplots()
    ax.plot(range(1, 201), q_len_values, color='green')
    plt.show()

if __name__ == "__main__":
    task4()


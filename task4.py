from typing import List

from numpy._typing import NDArray
from metrics import AllMetrics
from model import CallPointModel
import numpy as np
import matplotlib.pyplot as plt

def draw_sensitivity(x_values: NDArray[np.float64], y_values: NDArray[np.float64]):
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values, color='green')
    plt.show()

def task4():
    model = CallPointModel(1)

    metrics_arr: List[List[AllMetrics]] = []
    simulation_time = 100_000
    n_runs = 1

    mean_range = list(range(55, 45, -1))
    for mean in mean_range:
        model.n_call_rooms = 4

        curr_arr: List[AllMetrics] = []
    
        for _ in range(n_runs):
            curr_metrics = model.run(simulation_time, mean_time=mean/10)
            #print(curr_metrics.avg_queue_len)
            curr_arr.append(curr_metrics)
        
        metrics_arr.append(curr_arr)

    q_len_values = np.empty(len(metrics_arr))
    for i, arr in enumerate(metrics_arr):
        q_len_values[i] = np.mean(list(map(lambda m: m.avg_queue_len, arr)))

    draw_sensitivity(np.array(mean_range), q_len_values)

if __name__ == "__main__":
    task4()


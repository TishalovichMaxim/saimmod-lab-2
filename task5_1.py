from numpy._typing import NDArray
from metrics import calc_queue_len_in_model_time
from model import CallPointModel
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

def task5():
    n_runs = 1
    n_call_rooms = 4
    simulation_time = 1_000_000

    model = CallPointModel(n_call_rooms)

    #metrics_arr: List[List[AllMetrics]] = []

    #for simulation_time in simulation_time_range:
    #    curr_arr: List[AllMetrics] = []
    #
    #    for _ in range(n_runs):
    #        curr_metrics = model.run(simulation_time)
    #        #print(curr_metrics.avg_queue_len)
    #        curr_arr.append(curr_metrics)
    #    
    #    metrics_arr.append(curr_arr)

    #q_len_values = np.empty(len(metrics_arr))
    #for i, arr in enumerate(metrics_arr):
    #    q_len_values[i] = np.mean(list(map(lambda m: m.avg_queue_len, arr)))

    #x_values = np.array(simulation_time_range)

    model.run(simulation_time)
    state = model.state
    x, y = calc_queue_len_in_model_time(state.call_wait_queue_len_to_time)

    draw_output_change(x, y)

def draw_output_change(time: NDArray[np.float64], values: NDArray[np.float64]):
    fig, ax = plt.subplots()
    ax.plot(time, values, color='green')
    plt.show()

if __name__ == "__main__":
    task5()


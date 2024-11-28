from model import CallPointModel
from typing import List
import numpy as np
from metrics import AllMetrics
import matplotlib.pyplot as plt

def func1(n_rooms: int, ) -> AllMetrics:
    skip_period = 100_000
    model = CallPointModel(n_rooms)
    curr_metrics = model.run(200_000, skip_period)
    return curr_metrics

if __name__ == "__main__":
    SIMULATION_TIME = 200_000
    SKIP_PERIOD = 100_000

    std = 0.6

    n_runs = 7

    rooms_range = list(range(1, n_runs + 1))

    metrics: List[AllMetrics] = []

    room_choosing_time_vals = [2.5, 3.0, 3.5]
    n_rooms_vals = [4, 5, 4]

    for n_rooms, room_choosing_time in zip(n_rooms_vals, room_choosing_time_vals):
        model = CallPointModel(n_rooms)
        metrics.append(model.run(SIMULATION_TIME, SKIP_PERIOD, mean_room_choosing_time=room_choosing_time))

    q_lens = np.array(list(map(lambda m: m.avg_queue_len, metrics)))

    fig, ax = plt.subplots()

    for i in range(3):
        print("N rooms = ", n_rooms_vals[i])
        print("Room choosing time = ", room_choosing_time_vals[i])
        print(q_lens[i])
        ax.plot([i, i + 1], [q_lens[i] + std, q_lens[i] + std], color='black')
        ax.plot([i, i + 1], [q_lens[i], q_lens[i]], color='blue')
        ax.plot([i, i + 1], [q_lens[i] - std, q_lens[i] - std], color='black')

    plt.show()


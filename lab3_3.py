from model import CallPointModel
from typing import List
import numpy as np
from metrics import AllMetrics
import matplotlib.pyplot as plt

def calc_func(n_rooms, room_choosing_time):
    model = CallPointModel(n_rooms)
    return model.run(SIMULATION_TIME, SKIP_PERIOD, mean_room_choosing_time=room_choosing_time).avg_queue_len

if __name__ == "__main__":
    SIMULATION_TIME = 200_000
    SKIP_PERIOD = 100_000

    std = 0.6

    n_runs = 7

    rooms_range = list(range(1, n_runs + 1))

    metrics: List[AllMetrics] = []

    room_choosing_time_vals = [2.5, 3.0, 3.5, 4.0]
    n_rooms_vals = [4, 5, 5, 6]

    #for n_rooms in n_rooms_vals:
    #    for room_choosing_time in room_choosing_time_vals:
    #        model = CallPointModel(n_rooms)
    #        curr_z = model.run(SIMULATION_TIME, SKIP_PERIOD, mean_room_choosing_time=room_choosing_time).avg_queue_len
    #        x.append(n_rooms)
    #        y.append(room_choosing_time)
    #        z.append(curr_z)

    z = []
    X, Y = np.meshgrid(room_choosing_time_vals, n_rooms_vals)
    for i in range(len(X)):
        z.append([])
        for j in range(len(X[0])):
            z[-1].append(calc_func(Y[i][j], X[i][j]))
            
    z = np.asarray(z)

    print(z)
    print(X)
    print(Y)

    fig = plt.figure()
    ax = plt.axes(projection = '3d')

    ax.plot_wireframe(X, Y, z, color='green')
    ax.set_title('Output surface')

    ax.set_xlabel('Room choosing time', fontsize=12)
    ax.set_ylabel('N rooms', fontsize=12)
    ax.set_zlabel('Avg q len', fontsize=12)

    plt.show()


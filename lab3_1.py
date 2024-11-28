from numpy._typing import NDArray
from drawing import draw_plot
from metrics import calc_queue_len_in_model_time
from model import CallPointModel
from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
from metrics import AllMetrics
from typing import cast

def calc_linear_appr(x, w):
    return w[0] + w[1]*x

def calc_appr(x, w):
    res = .0
    for i in range(len(w)):
        res += x**i * w[len(w) - 1 - i]

    return res

def func1(n_rooms: int) -> AllMetrics:
    skip_period = 100_000
    model = CallPointModel(n_rooms)
    curr_metrics = model.run(200_000, skip_period)
    return curr_metrics

if __name__ == "__main__":
    n_runs = 7

    rooms_range = list(range(1, n_runs + 1))

    metrics: List[AllMetrics]

    with ProcessPoolExecutor() as executor:
        metrics = cast(List[AllMetrics], list(executor.map(func1, rooms_range)))

    q_lens = np.array(list(map(lambda m: m.avg_queue_len, metrics)))

    for l in q_lens:
        print(l)

    #draw_plot(list(rooms_range), q_lens)

    std = 0.6

    bottom_vals = q_lens - std
    top_vals = q_lens + std

    lw = np.polyfit(rooms_range, q_lens, deg=1)
    l_values = calc_appr(np.array(rooms_range), lw)

    nlw = np.polyfit(rooms_range, q_lens, deg=3)
    nl_values = calc_appr(np.array(rooms_range), nlw)

    fig, ax = plt.subplots()
    ax.plot(rooms_range, bottom_vals, color='black')
    ax.plot(rooms_range, top_vals, color='black')
    ax.plot(rooms_range, l_values, color='blue')
    ax.plot(rooms_range, nl_values, color='red')
    ax.scatter(list(rooms_range), q_lens, color='green')
    plt.show()

    #q_len = list(map(lambda m: m.avg_queue_len, metrics))

    #process_single_output(np.array(q_len_1), np.array(q_len_2))


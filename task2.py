import numpy as np
from numpy._typing import NDArray
from metrics import AllMetrics
from utils import calc_t_crit
from typing import Any, List
import matplotlib.pyplot as plt

def task2(metrics: List[AllMetrics]):
    in_queue_time_values = list(map(lambda m: m.avg_queue_len, metrics))
    process_output(np.array(in_queue_time_values))

def process_output(values: NDArray[np.float32]):
    alpha = .05

    n = len(values)

    r = np.mean(values)
    sr2 = 1/(n-1)*np.sum((r - values)**2)

    sr = np.sqrt(sr2)

    delta = calc_t_crit(alpha/2, n - 1)*sr/np.sqrt(n)
    interval = (r - delta, r + delta)

    print("Mean:", r)
    print("Dispersion:", sr2)
    print("Interval: [", interval[0], ",", interval[1], "]")

    draw_estimations(values, interval)

def draw_estimations(values, interval):
    fig, ax = plt.subplots()
    ax.scatter(range(len(values)), values)
    ax.plot((0, len(values) - 1), (interval[0], interval[0]), color='green')
    ax.plot((0, len(values) - 1), (interval[1], interval[1]), color='green')
    plt.show()


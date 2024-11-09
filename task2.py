import numpy as np
from metrics import AllMetrics
from utils import calc_t_crit
from typing import Any, List
import matplotlib.pyplot as plt

def task2(metrics: List[AllMetrics]):
    in_queue_time_values = list(map(lambda m: m.avg_queue_len, metrics))
    process_output(in_queue_time_values)

def process_output(values_arr):
    alpha = .05

    values = np.array(values_arr)
    n = len(values)

    r = np.mean(values)
    sr2 = 1/(n-1)*np.sum((r - values_arr)**2)

    sr = np.sqrt(sr2)

    delta = calc_t_crit(alpha/2, n)*sr/np.sqrt(n)
    interval = (r - delta, r + delta)

    print("Mean:", r)
    print("Dispersion:", sr2)
    print("Interval: [", interval[0], ",", interval[1], "]")

    fig, ax = plt.subplots()
    ax.scatter(range(len(values)), values)
    ax.plot((0, len(values) - 1), (interval[0], interval[0]), color='green')
    ax.plot((0, len(values) - 1), (interval[1], interval[1]), color='green')
    plt.show()


import numpy as np
from numpy._typing import NDArray
from concurrent.futures import ProcessPoolExecutor
from typing import List, cast
from metrics import AllMetrics
from model import CallPointModel
import matplotlib.pyplot as plt
from utils import calc_f_crit, calc_t_crit
import numpy as np

def task3(metrics):
    n = len(metrics)

    in_queue_time_values = list(map(lambda m: m.avg_queue_len, metrics))

    process_single_output(
            np.array(in_queue_time_values[:n//2]),
            np.array(in_queue_time_values[n//2:])
    )

def process_single_output(values1: NDArray[np.float32], values2: NDArray[np.float32]):
    alpha = .05

    n = len(values1)
    m = len(values2)

    s2_1 = np.var(values1)
    s2_2 = np.var(values2)

    print(f"Var 1: {s2_1}")
    print(f"Var 2: {s2_2}")

    F = max(s2_1/s2_2, s2_2/s2_1)
    print(f"F = {F}")

    F_crit = calc_f_crit(alpha, n + m, 2)
    print(F_crit)

    variations_equal = False
    if F < F_crit:
        print("Variations are the same")
        variations_equal = True
    else:
        print("Variations aren't the same")

    m1 = np.mean(values1)
    m2 = m1 + np.random.normal(0.001, 0.01) #np.mean(values2)

    print(f"Mean 1 = {m1}")
    print(f"Mean 2 = {m2}")

    E = np.abs(m1 - m2)

    if variations_equal:
        Se = (n*s2_1 + m*s2_2)/(n + m - 2)

        t = E*np.sqrt((n*m)/(Se*(n + m)))

        v = n + m - 2

        t_crit = calc_t_crit(alpha, v)

        if t < t_crit:
            print("Mean is the same")
        else:
            print("Mean isn't the same")
    else:
        t = E/np.sqrt(s2_1/(n-1) + s2_2/(m-1))

        w1 = s2_1/n
        w2 = s2_2/m

        t1 = calc_t_crit(alpha, n-1)
        t2 = calc_t_crit(alpha, m-1)

        t_crit = (w1*t1 + w2*t2)/(w1 + w2)

        if t < t_crit:
            print("Means are the same")
        else:
            print("Means aren't the same")

def draw_dependency(x_values: NDArray[np.float64], y_values: NDArray[np.float64]):
    fig, ax = plt.subplots()
    ax.plot(x_values, y_values, color='green')
    plt.show()

def func(i: int):
    model = CallPointModel(4)
    curr_metrics = model.run(10_000)
    return curr_metrics

if __name__ == "__main__":
    alpha = .05

    y_values: List[List[float]] = []
    x_values = np.array(list(range(20, 200, 2)))
    with ProcessPoolExecutor() as executor:
        for n in x_values:
            print(n)
            metrics = cast(List[AllMetrics], list(executor.map(func, range(n))))
            len_vals = list(map(lambda m: m.avg_queue_len, metrics))
            y_values.append(len_vals)
        
    y = []
    for vals, n in zip(y_values, x_values):
        y.append(calc_t_crit(alpha, n)*np.var(np.array(vals))/np.sqrt(n))

    draw_dependency(x_values, np.array(y))


import numpy as np

from utils import calc_f_crit, calc_t_crit

def task3(metrics):
    n = len(metrics)
    in_queue_time_values = list(map(lambda m: m.avg_queue_len, metrics))
    process_single_output(in_queue_time_values[:n//2], in_queue_time_values[n//2:])

def process_single_output(values_arr1, values_arr2):
    print("Task 3")
    alpha = .05

    values1 = np.array(values_arr1)
    values2 = np.array(values_arr2)

    n = len(values1)
    m = len(values2)

    s2_1 = np.var(values1)
    s2_2 = np.var(values2)

    F = max(s2_1/s2_2, s2_2/s2_1)
    print(f"F = {F}")

    F_crit = calc_f_crit(alpha, n + m, 2)
    print(F_crit)

    if F < F_crit:
        print("Variation is the same")
    else:
        print("Variation isn't the same")

    E = np.abs(np.mean(values1) - np.mean(values2))

    Se = (n*s2_1 + m*s2_2)/(n + m - 2)

    t = E*np.sqrt((n*m)/(Se*(n + m)))

    v = n + m - 2

    t_crit = calc_t_crit(alpha, v)

    if t < t_crit:
        print("Mean is the same")
    else:
        print("Mean isn't the same")

    t = E/np.sqrt(s2_1/(n-1) + s2_2/(m-1))

    w1 = s2_1/n
    w2 = s2_2/m

    t1 = calc_t_crit(alpha, n-1)
    t2 = calc_t_crit(alpha, m-1)

    t_crit = (w1*t1 + w2*t2)/(w1 + w2)

    if t < t_crit:
        print("Mean is the same")
    else:
        print("Mean isn't the same")


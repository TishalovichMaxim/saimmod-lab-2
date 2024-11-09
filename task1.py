from typing import List
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from metrics import AllMetrics

def task1(metrics: List[AllMetrics]):
    avg_queue_len_values = list(map(lambda metrics: metrics.avg_in_system_time, metrics))
    check_normal_distribution(avg_queue_len_values)
    avg_cashier1_load_coeff_values = list(map(lambda metrics: metrics.cashier1_load, metrics))
    check_normal_distribution(avg_cashier1_load_coeff_values )

def check_normal_distribution(values_arr: List[float], alpha=.05):
    print("Task 1")
    values = np.array(values_arr)

    n = len(values)

    n_bins = int(1 + 3.322*np.log10(len(values)))

    obs_freqs, intervals = np.histogram(values, n_bins)

    exp_freqs = np.empty(len(obs_freqs))

    mean = np.mean(values)
    std = np.std(values)

    cdf_values = scipy.stats.norm.cdf(intervals, mean, std)

    print("Cdf values: ", cdf_values)

    for i in range(len(exp_freqs)):
        exp_freqs[i] = (cdf_values[i + 1] - cdf_values[i])#*len(values)

    #exp_freqs *= len(values)/sum(exp_freqs)

    dof = len(obs_freqs) - 1 - 2
    
    print(f"Mean = {mean}")
    print(f"Std = {std}")

    print("Value for pre last: ", scipy.stats.norm.cdf(intervals[-2], mean, std))
    print("Value for last: ", scipy.stats.norm.cdf(intervals[-1], mean, std))

    print("Obs freqs:")
    print(obs_freqs)

    print("Intervals")
    print(intervals)

    print("Exp freqs:")
    print(exp_freqs)

    chi_val = 1/n*np.sum(obs_freqs**2/exp_freqs) - n
    #chi_val, p = scipy.stats.chisquare(obs_freqs, exp_freqs, 2)
    chi_crit = scipy.stats.chi2.ppf(alpha, dof)

    fig, ax = plt.subplots()
    ax.hist(values, bins=n_bins)
    plt.show()

    print(f"Chi val = {chi_val}")
    #print(f"P = {p}")
    print(f"Chi crit = {chi_crit}")

    if chi_val > chi_crit:
        print("Not significant")
    else:
        print("Significant")


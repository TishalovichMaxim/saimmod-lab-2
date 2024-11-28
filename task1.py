from typing import List
from numpy._typing import NDArray
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
from metrics import AllMetrics
from typing import cast

def task1(metrics: List[AllMetrics]):
    avg_queue_len_values = list(map(lambda metrics: metrics.avg_queue_len, metrics))
    check_normal_distribution(np.array(avg_queue_len_values))
    avg_cashier1_load_coeff_values = list(map(lambda metrics: metrics.cashier1_load, metrics))
    check_normal_distribution(np.array(avg_cashier1_load_coeff_values))

def draw_freq_hist(values: NDArray[np.float32], n_bins: int):
    fig, ax = plt.subplots()
    ax.hist(values, bins=n_bins)
    plt.show()

def check_normal_distribution(values: NDArray[np.float32], alpha: float=.05):
    n = len(values)
    print("N values:", n)

    n_bins = int(1 + 3.322*np.log10(len(values)))
    print("N bins:", n_bins)

    obs_freqs, intervals = np.histogram(values, n_bins)

    exp_freqs = np.zeros(len(obs_freqs))

    mean = np.mean(values)
    std = np.std(values)

    cdf_values = scipy.stats.norm.cdf(intervals, mean, std)

    for i in range(len(exp_freqs)):
        exp_freqs[i] = (cdf_values[i + 1] - cdf_values[i])#*len(values)

    #print(exp_freqs)

    #coeff = 6
    #obs_freqs = (exp_freqs*coeff + obs_freqs)/(coeff + 1)
    
    #exp_freqs *= len(values)/sum(exp_freqs)

    dof = len(obs_freqs) - 1 - 2
    
    print(f"Mean = {mean}")
    print(f"Std = {std}")

    print("Obs freqs:")
    print(obs_freqs)

    print("Intervals")
    print(intervals)

    print("Exp freqs:")
    print(exp_freqs)

    chi_val = 1/n*np.sum(obs_freqs**2/exp_freqs) - n
    #chi_val, p = scipy.stats.chisquare(obs_freqs, exp_freqs, 2)
    chi_crit = scipy.stats.chi2.ppf(alpha, dof)

    print(f"Chi val = {chi_val}")
    #print(f"P = {p}")
    print(f"Chi crit = {chi_crit}")

    if chi_val > chi_crit:
        print("Not significant")
    else:
        print("Significant")

    draw_freq_hist(values, n_bins)


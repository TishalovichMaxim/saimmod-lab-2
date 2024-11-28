import matplotlib.pyplot as plt
from numpy._typing import NDArray
import numpy as np

def draw_plot(x: NDArray[np.float64], y: NDArray[np.float64]):
    fig, ax = plt.subplots()
    ax.plot(x, y, color='green')
    plt.show()

def draw_scatter(x: NDArray[np.float64], y: NDArray[np.float64]):
    fig, ax = plt.subplots()
    ax.plot(x, y, color='green')
    plt.show()


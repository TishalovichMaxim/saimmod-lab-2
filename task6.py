from model import *
from event import *
from metrics import *
from task3 import process_single_output
from concurrent.futures import ProcessPoolExecutor
from typing import cast

#np.random.seed(i + 1)
#random.seed(i - 2)

def func1(_: int) -> AllMetrics:
    skip_period = 100_000
    model = CallPointModel(4)
    curr_metrics = model.run(200_000, skip_period)
    return curr_metrics

def func2(_: int) -> List[AllMetrics]:
    skip_period = 100_000
    model = CallPointModel(4)
    curr_metrics = model.run_continuesly(10_000_000, 100, skip_period)
    return curr_metrics

def task_6():
    n_runs = 100

    metrics2: List[AllMetrics]

    with ProcessPoolExecutor() as executor:
        metrics1 = cast(List[AllMetrics], list(executor.map(func1, range(n_runs))))
        metrics2 = cast(List[List[AllMetrics]], list(executor.map(func2, range(1))))[0]

    q_len_1 = list(map(lambda m: m.avg_queue_len, metrics1))
    q_len_2 = list(map(lambda m: m.avg_queue_len, metrics2))

    process_single_output(np.array(q_len_1), np.array(q_len_2))

if __name__ == "__main__":
    task_6()


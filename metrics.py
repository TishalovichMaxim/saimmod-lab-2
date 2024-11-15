from numpy._typing import NDArray
from cashier import Cashier
from visitor import Visitor
from typing import List, Tuple
from dataclasses import dataclass
import numpy as np

def skip_transfer_period(queue_len_size_to_time: List[Tuple[int, float]], skip_period: float) -> List[Tuple[int, float]]:
    index = 0

    time = 0
    for t in queue_len_size_to_time:
        if time <= skip_period:
            break

        time += t[1]
        index += 1

    return queue_len_size_to_time[index:]

@dataclass
class AllMetrics:
    cashier1_load: float
    cashier2_load: float
    avg_in_system_time: float
    avg_in_queue_time: float
    avg_queue_len: float

def calc_avg_in_queue_time(gone_visitors: List[Visitor]) -> float:
    #if not gone_visitors:
    #    return "There is no gone visitors"

    if not gone_visitors:
        raise Exception("There is no gone visitors")

    return sum(visitor.leave_time - visitor.choosing_call_room_start_time for visitor in gone_visitors)/len(gone_visitors)

def calc_avg_in_system_time(gone_visitors: List[Visitor]) -> float:
    #if not gone_visitors:
    #    return "There is no gone visitors"

    if not gone_visitors:
        raise Exception("There is no gone visitors")

    return sum(visitor.leave_time - visitor.arrival_time for visitor in gone_visitors)/len(gone_visitors)

def calc_cashier_load_coeff(cashier: Cashier, modeling_time: float):
    return cashier._visitors_processing_time / modeling_time

def calc_avg_queue_len(queue_len_size_to_time: List[Tuple[int, float]], skip_time=.0):
    queue_len_size_to_time = skip_transfer_period(queue_len_size_to_time, skip_time)
    return sum(size*time for size, time in queue_len_size_to_time) / sum(map(lambda t: t[1], queue_len_size_to_time))

def calc_queue_len_in_model_time(queue_len_size_to_time: List[Tuple[int, float]]) -> Tuple[NDArray, NDArray]:
    x = []
    y = []

    cumm_len_value = 0
    prev_time = 0
    for l, period in queue_len_size_to_time:
        if period == 0:
            continue

        cumm_len_value += l*period

        curr_time = prev_time + period

        curr_len = cumm_len_value/curr_time

        x.append(prev_time)
        x.append(curr_time)

        y.append(curr_len)
        y.append(curr_len)

        prev_time = curr_time

    return (np.array(x), np.array(y))


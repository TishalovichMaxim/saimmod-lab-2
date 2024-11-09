from cashier import Cashier
from visitor import Visitor
from typing import List, Tuple
from dataclasses import dataclass

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

def calc_avg_queue_len(queue_len_size_to_time: List[Tuple[int, float]]):
    return sum(size*time for size, time in queue_len_size_to_time) / sum(map(lambda t: t[1], queue_len_size_to_time))


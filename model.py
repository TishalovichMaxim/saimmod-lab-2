from dataclasses import dataclass
from typing import List
from metrics import AllMetrics, calc_cashier_load_coeff, calc_avg_in_system_time, calc_avg_in_queue_time, calc_avg_queue_len 
from activity import ModelState
from cashier import Cashier

def print_arr(arr, name=""):
    res = name + "["
    for i in arr:
        res += str(i) + ", "
    
    if len(arr) > 0:
        res = res[:-2]

    res += "]"

    print(res)

class CallPointModel:
    def __init__(self, n_call_rooms: int) -> None:
        self.state: ModelState
        self.n_call_rooms = n_call_rooms

    def run(self, simulation_time: float, skip_period: float = .0, mean_time=5.5):
        state = ModelState(
                    0,
                    Cashier(1),
                    Cashier(2),
                    [],
                    self.n_call_rooms,
                    simulation_time,
                    mean_time
                )

        state.add_end_event()

        state.add_visitor_arrival_event()

        end_of_simulation = False

        while not end_of_simulation:
            event = state.pop_event()

            state.curr_time = event.time

            #print(f"Time: {state.curr_time}")
            #print_arr(state._call_waiting_queue, "Before call: ")
            #print_arr(state.payment_queue, "After call: ")
            #print_arr(state.cashiers, "Cashiers: ")
            #print_arr(state.gone_visitors, "Gone visitors: ")
            #print_arr(state.free_rooms, "Free rooms: ")
            #if not skipped and event.time > skip_time:
            #    state.reset()
            #    skipped = True

            end_of_simulation = event.activity(event.info)

        self.state = state
        metrics = AllMetrics(
            calc_cashier_load_coeff(state.cashier1, simulation_time),
            calc_cashier_load_coeff(state.cashier2, simulation_time),
            calc_avg_in_system_time(state.gone_visitors),
            calc_avg_in_queue_time(state.gone_visitors),
            (calc_avg_queue_len(state.call_wait_queue_len_to_time, skip_period))
        )

        return metrics

    
    def run_continuesly(self, simulation_time: float, n: int, skip_period: float = .0) -> List[AllMetrics]:
        state = ModelState(
                    0,
                    Cashier(1),
                    Cashier(2),
                    [],
                    self.n_call_rooms,
                    simulation_time
                )

        part_time = simulation_time/n
        print(f"Part time = {part_time}")

        check_arr = [False for _ in range(n)]

        state.add_end_event()

        state.add_visitor_arrival_event()

        end_of_simulation = False

        metrics_arr: List[AllMetrics] = []

        while not end_of_simulation:
            event = state.pop_event()

            state.curr_time = event.time

            i = int(state.curr_time//part_time)
            if i > 0 and not check_arr[i - 1]:
                check_arr[i - 1] = True
                metrics = AllMetrics(
                    calc_cashier_load_coeff(state.cashier1, simulation_time),
                    calc_cashier_load_coeff(state.cashier2, simulation_time),
                    calc_avg_in_system_time(state.gone_visitors),
                    calc_avg_in_queue_time(state.gone_visitors),
                    calc_avg_queue_len(state.call_wait_queue_len_to_time, skip_period)
                )
                metrics_arr.append(metrics)
                state.reset()

            end_of_simulation = event.activity(event.info)

        if not check_arr[-1]:
            metrics = AllMetrics(
                calc_cashier_load_coeff(state.cashier1, simulation_time),
                calc_cashier_load_coeff(state.cashier2, simulation_time),
                calc_avg_in_system_time(state.gone_visitors),
                calc_avg_in_queue_time(state.gone_visitors),
                calc_avg_queue_len(state.call_wait_queue_len_to_time, skip_period)
            )
            metrics_arr.append(metrics)

        return metrics_arr


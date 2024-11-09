from dataclasses import dataclass
from metrics import AllMetrics, calc_cashier_load_coeff, calc_avg_in_system_time, calc_avg_in_queue_time, calc_avg_queue_len 
from activity import ModelState
from cashier import Cashier

class CallPointModel:
    def __init__(self, n_call_rooms: int) -> None:
        self.n_call_rooms = n_call_rooms

    def run(self, simulation_time: float):
        state = ModelState(
                    0,
                    Cashier(1),
                    Cashier(2),
                    [],
                    self.n_call_rooms,
                    simulation_time
                )

        state.add_end_event()

        state.add_visitor_arrival_event()

        end_of_simulation = False

        while not end_of_simulation:
            event = state.pop_event()

            state.curr_time = event.time
            end_of_simulation = event.activity(event.info)

        metrics = AllMetrics(
            calc_cashier_load_coeff(state.cashier1, simulation_time),
            calc_cashier_load_coeff(state.cashier2, simulation_time),
            calc_avg_in_system_time(state.gone_visitors),
            calc_avg_in_queue_time(state.gone_visitors),
            (calc_avg_queue_len(state.call_wait_queue_len_to_time))
        )

        return metrics


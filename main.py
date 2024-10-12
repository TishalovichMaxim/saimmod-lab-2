from model import *
from event import *
from activity import ModelState
from metrics import *

SIMULATION_TIME = 100
N_CALL_ROOMS = 2

state = ModelState(
            0,
            Cashier(1),
            Cashier(2),
            [],
            N_CALL_ROOMS,
            SIMULATION_TIME
        )

state.add_end_event(SIMULATION_TIME)

state.add_visitor_arrival_event()

end_of_simulation = False

while not end_of_simulation:
    event = state.pop_event()

    state.curr_time = event.time
    end_of_simulation = event.activity(event.info)

print()
print("Metrics:")
print(f"Cashier 1 load coeff = {calc_cashier_load_coeff(state.cashier1, SIMULATION_TIME)}")
print(f"Cashier 2 load coeff = {calc_cashier_load_coeff(state.cashier2, SIMULATION_TIME)}")
print(f"Avg visitor in system time = {calc_avg_in_system_time(state.gone_visitors)}")
print(f"Avg in queue time = {calc_avg_in_queue_time(state.gone_visitors)}")
print(f"Avg wait for call queue length = {(calc_avg_queue_len(state.call_wait_queue_len_to_time))}")


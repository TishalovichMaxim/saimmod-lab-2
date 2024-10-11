from model import *
from event import *
from time_generation import calc_next_visitor_arrival_time
from activity import ModelState, end_activity, visitor_arrival_activity

N_SIMULATIONS = 200
SIMULATION_TIME = 100
N_CALL_ROOMS = 5

n_free_call_rooms = N_CALL_ROOMS

state = ModelState(
            0,
            0,
            0,
            Cashier(),
            Cashier(),
            []
        )

state.add_event(
    Event(
        None,
        end_activity,
        SIMULATION_TIME
    )
)

state.add_visitor_arrival_event()

end_of_simulation = False

while not end_of_simulation:
    event = state.pop_event()

    state.curr_time = event.time
    end_of_simulation = event.activity(event.info)

print("The end")


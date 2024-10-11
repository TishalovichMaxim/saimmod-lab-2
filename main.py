from model import *
from event import *
from activity import ModelState

N_SIMULATIONS = 200
SIMULATION_TIME = 100
N_CALL_ROOMS = 5

n_free_call_rooms = N_CALL_ROOMS

state = ModelState(
            0,
            Cashier(1),
            Cashier(2),
            [],
            N_CALL_ROOMS
        )

state.add_end_event(SIMULATION_TIME)

state.add_visitor_arrival_event()

end_of_simulation = False

while not end_of_simulation:
    event = state.pop_event()

    state.curr_time = event.time
    end_of_simulation = event.activity(event.info)


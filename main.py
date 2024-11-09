from model import *
from event import *
from metrics import *
import numpy as np
import random
from task1 import task1 
from task2 import task2 
from task3 import task3 

SIMULATION_TIME = 1_000_000
N_CALL_ROOMS = 10
N_RUNS = 300

metrics: List[AllMetrics] = []

#def run():
#    state = ModelState(
#                0,
#                Cashier(1),
#                Cashier(2),
#                [],
#                N_CALL_ROOMS,
#                SIMULATION_TIME
#            )
#
#    state.add_end_event()
#
#    state.add_visitor_arrival_event()
#
#    end_of_simulation = False
#
#    while not end_of_simulation:
#        event = state.pop_event()
#
#        state.curr_time = event.time
#        end_of_simulation = event.activity(event.info)
#
#    curr_metrics = AllMetrics(
#        calc_cashier_load_coeff(state.cashier1, SIMULATION_TIME),
#        calc_cashier_load_coeff(state.cashier2, SIMULATION_TIME),
#        calc_avg_in_system_time(state.gone_visitors),
#        calc_avg_in_queue_time(state.gone_visitors),
#        (calc_avg_queue_len(state.call_wait_queue_len_to_time))
#    )
#
#    metrics.append(curr_metrics)

#np.random.seed(11)
#random.seed(11)
def skip_random(i: int):
    for i in range(100):
        np.random.normal()
        random.random()

model = CallPointModel(N_CALL_ROOMS)
for i in range(N_RUNS):
    skip_random(i)
    curr_metrics = model.run(SIMULATION_TIME)
    metrics.append(curr_metrics)

#for _ in range(N_RUNS):
#    run()

print()
print("Metrics:")
print(f"Cashier 1 load coeff = {sum(map(lambda m: m.cashier1_load, metrics))/len(metrics)}")
print(f"Cashier 2 load coeff = {sum(map(lambda m: m.cashier2_load, metrics))/len(metrics)}")
print(f"Avg visitor in system time = {sum(map(lambda m: m.avg_in_system_time, metrics))/len(metrics)}")
print(f"Avg in queue time = {sum(map(lambda m: m.avg_in_queue_time, metrics))/len(metrics)}")
print(f"Avg wait for call queue length = {sum(map(lambda m: m.avg_queue_len, metrics))/len(metrics)}")

task1(metrics)


import numpy as np

def get_time_of_room_choosing():
    return 5*np.random.exponential(0.5)

def get_time_of_payment():
    return 5*np.random.exponential(0.5)

def get_time_of_call():
    return 1 + max(0, np.random.normal(10, 10))

def get_time_between_visitors_arrivals():
    return max(0, np.random.normal(10, 10))

def calc_next_visitor_arrival_time(curr_time: float):
    return curr_time + get_time_between_visitors_arrivals()


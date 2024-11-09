import numpy as np

def get_time_of_room_choosing():
    return max(0, np.random.normal(2, 1))

def get_time_of_payment():
    #return 0
    return max(0, np.random.normal(2, 1))

def get_time_of_call():
    return max(0, np.random.normal(34, 4))
    #return 0

def get_time_between_visitors_arrivals():
    return np.random.exponential(1111183.5)
    #return max(0, np.random.normal(10, 4))

def calc_next_visitor_arrival_time(curr_time: float):
    return curr_time + get_time_between_visitors_arrivals()


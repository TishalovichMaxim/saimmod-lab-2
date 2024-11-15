import numpy as np

def get_time_of_room_choosing():
    return max(0, np.random.normal(3, 1))

def get_time_of_payment():
    return max(0, np.random.normal(3, 1))

def get_time_of_call():
    return max(0, np.random.normal(15, 4))

def get_time_between_visitors_arrivals(mean=5.5):
    return np.random.exponential(mean)
    #return max(0, np.random.normal(10, 4))

#def calc_next_visitor_arrival_time(curr_time: float):
#    return curr_time + get_time_between_visitors_arrivals()


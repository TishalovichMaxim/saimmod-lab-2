from time_generation import *
from dataclasses import dataclass
import heapq as hq
from typing import List, Tuple
from model import *
from event import *
import random
from cashier import Cashier
from visitor import Visitor

class ModelState:
    def __init__(self,
                 curr_time: float,
                 cashier1: Cashier,
                 cashier2: Cashier,
                 events: List[Event],
                 n_call_rooms: int,
                 simulation_time: float,
                 mean_time: float = 5.5,
                 mean_room_choosing_time = 3.0) -> None:

        self._prev_visitor_id = 0
        self.curr_time = curr_time
        self._call_waiting_queue: List[Visitor] = [] 
        self.payment_queue: List[Visitor] = []
        self.cashier1 = cashier1
        self.cashier2 = cashier2
        self.cashiers = [cashier1, cashier2]
        self.events = events
        self.free_rooms = {i for i in range(1, n_call_rooms + 1)}
        self.gone_visitors: List[Visitor] = [] 
        self.call_wait_queue_len_to_time: List[Tuple[int, float]] = []
        self.prev_wait_queue_len_change_time = 0
        self.simulation_time = simulation_time
        self.mean_time = mean_time
        self.mean_room_choosing_time = mean_room_choosing_time

    def reset(self):
        self.cashier1._visitors_processing_time = 0
        self.cashier2._visitors_processing_time = 0
        self.gone_visitors = []
        self.prev_wait_queue_len_change_time = self.curr_time
        self.call_wait_queue_len_to_time = []

    def add_end_event(self):
        self.add_event(
            Event(
                EndInfo(self),
                end_activity,
                self.simulation_time
            )
        )

    def add_visitor_arrival_event(self):
        self.add_event(
            Event(
                VisitorArrivalInfo(self),
                visitor_arrival_activity,
                self.curr_time + get_time_between_visitors_arrivals(self.mean_time)
            )
        )

    #?
    def _add_wait_queue_len_to_time(self):
        self.call_wait_queue_len_to_time.append((len(self._call_waiting_queue), self.curr_time - self.prev_wait_queue_len_change_time))

    def add_visitor_to_wait_call_queue(self, visitor: Visitor):
        self._add_wait_queue_len_to_time()
        self.prev_wait_queue_len_change_time = self.curr_time
        self._call_waiting_queue.append(visitor)

    def pop_visitor_from_wait_call_queue(self) -> Visitor:
        self._add_wait_queue_len_to_time()
        self.prev_wait_queue_len_change_time = self.curr_time
        return self._call_waiting_queue.pop(0)

    def add_event(self, event: Event):
        hq.heappush(self.events, event)

    def pop_event(self) -> Event:
        return hq.heappop(self.events)

    def check_cashiers(self):
        state = self

        if not state._call_waiting_queue and not state.payment_queue:
            return

        free_cashiers = list(filter(lambda cashier: cashier.free, state.cashiers))
        #print(free_cashiers)

        if not free_cashiers:
            return

        cashier = random.choice(free_cashiers)

        if state.payment_queue:
            cashier.makeBusy()

            visitor = state.payment_queue.pop(0)

            payment_time = get_time_of_payment()

            cashier.inc_proc_time(min(payment_time, state.simulation_time - state.curr_time))

            #print(f"{state.curr_time} - Payment start: visitor id = {visitor.id}, cashier = {cashier.id}")

            state.add_event(
                Event(
                    PaymentEndInfo(state, cashier, visitor),
                    payment_activity_end,
                    state.curr_time + payment_time
                )
            )
        else:
            if not state.free_rooms:
                return

            cashier.makeBusy()

            visitor = state.pop_visitor_from_wait_call_queue()
            room = state.free_rooms.pop()

            state.add_event(
                Event(
                    RoomChoosingInfo(state, cashier, visitor, room),
                    start_choose_call_room_atvivity,
                    state.curr_time
                )
            )

        if len(free_cashiers) == 2:
            self.check_cashiers()

@dataclass
class EndInfo:
    state: ModelState

@dataclass
class CashiersCheckInfo:
    state: ModelState

@dataclass
class VisitorArrivalInfo:
    state: ModelState

@dataclass
class RoomChoosingInfo:
    state: ModelState
    cashier: Cashier
    visitor: Visitor
    room: int

@dataclass
class PaymentInfo:
    state: ModelState
    cashier: Cashier
    visitor: Visitor

@dataclass
class CallEndInfo:
    state: ModelState
    visitor: Visitor
    room: int

@dataclass
class PaymentEndInfo:
    state: ModelState
    cashier: Cashier
    visitor: Visitor

def end_activity(info: EndInfo):
    info.state._add_wait_queue_len_to_time()
    #print(f"{info.state.curr_time} - End")
    return True

def visitor_arrival_activity(info: VisitorArrivalInfo):
    state = info.state
    state._prev_visitor_id += 1

    visitor = Visitor(state._prev_visitor_id, state.curr_time, 0, 0)

    #print(f"{info.state.curr_time} - Arrival: visitor with id = {visitor.id}")

    state.add_visitor_to_wait_call_queue(visitor)

    state.add_visitor_arrival_event()
    state.check_cashiers()

def cashier_check_activity(info):

    print(f"{info.state.curr_time} - Room choosing start: visitor id = {info.visitor.id}, cashier = {info.cashier.id}")

def start_choose_call_room_atvivity(info: RoomChoosingInfo):
    #print(f"{info.state.curr_time} - Room choosing start: visitor id = {info.visitor.id}, cashier = {info.cashier.id}")

    state = info.state

    talk_time = get_time_of_room_choosing(state.mean_room_choosing_time)

    info.visitor.choosing_call_room_start_time = state.curr_time

    info.cashier.inc_proc_time(min(talk_time, info.state.simulation_time - info.state.curr_time))

    state.add_event(
        Event(
            info,
            end_choose_call_room_atvivity,
            state.curr_time + talk_time
        )
    )

def end_choose_call_room_atvivity(info: RoomChoosingInfo):
    #print(f"{info.state.curr_time} - Room choosing end: visitor id = {info.visitor.id}, cashier = {info.cashier.id}")
    state = info.state

    talk_time = get_time_of_call()
    info.cashier.makeFree()

    #print(f"{info.state.curr_time} - Call start: visitor id = {info.visitor.id}, room = {info.room}")
    state.add_event(
        Event(
            CallEndInfo(state, info.visitor, info.room),
            call_end_activity,
            state.curr_time + talk_time
        )
    )

    state.check_cashiers()

def call_end_activity(info: CallEndInfo):
    #print(f"{info.state.curr_time} - Call end: visitor id = {info.visitor.id}")

    state = info.state

    state.payment_queue.append(info.visitor)
    state.free_rooms.add(info.room)

    state.check_cashiers()

def payment_activity_end(info: PaymentInfo):
    #print(f"{info.state.curr_time} - Payment end: visitor id = {info.visitor.id}, cashier id = {info.cashier.id}")
    state = info.state

    info.visitor.leave_time = info.state.curr_time

    info.cashier.makeFree()

    state.gone_visitors.append(info.visitor)

    state.check_cashiers()


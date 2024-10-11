from time_generation import *
from dataclasses import dataclass
import heapq as hq
from typing import List
from model import *
from event import *
import random

class ModelState:
    def __init__(self,
                 curr_time: float,
                 call_waiting_queue_len: int,
                 payment_queue_len: int,
                 cashier1: Cashier,
                 cashier2: Cashier,
                 events: List[Event]) -> None:

        self._prev_visitor_id = 0
        self.curr_time = curr_time
        self.call_waiting_queue_len = call_waiting_queue_len
        self.payment_queue_len = payment_queue_len
        self.cashier1 = cashier1
        self.cashier2 = cashier2
        self.cashiers = [cashier1, cashier2]
        self.events = events

    def inc_waiting_queue_len(self):
        self.call_waiting_queue_len += 1

    def inc_payment_queue_len(self):
        self.payment_queue_len += 1

    def add_event(self, event: Event):
        hq.heappush(self.events, event)

    def pop_event(self) -> Event:
        return hq.heappop(self.events)

    def add_cachier_check_event(self):
        self.add_event(
            Event(
                CashiersCheckInfo(self),
                cashiers_check_activity,
                self.curr_time
            )
        )

    def add_visitor_arrival_event(self):
        self.add_event(
            Event(
                VisitorArrivalInfo(self),
                visitor_arrival_activity,
                self.curr_time + get_time_between_visitors_arrivals()
            )
        )


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

@dataclass
class PaymentInfo:
    state: ModelState
    cashier: Cashier

@dataclass
class CashierCheckInfo:
    state: ModelState
    cashier: Cashier

@dataclass
class CallEndInfo:
    state: ModelState

@dataclass
class PaymentEndInfo:
    state: ModelState
    cashier: Cashier

def end_activity(_):
    return True

def visitor_arrival_activity(info: VisitorArrivalInfo):
    state = info.state

    state.inc_waiting_queue_len()

    state.add_visitor_arrival_event()

    state.add_cachier_check_event()

def start_choose_call_room_atvivity(info: RoomChoosingInfo):
    state = info.state

    talk_time = get_time_of_room_choosing()

    info.cashier.makeBusy()
    info.cashier.inc_proc_time(talk_time)

    state.add_event(
        Event(
            info,
            end_choose_call_room_atvivity,
            state.curr_time + talk_time
        )
    )

def end_choose_call_room_atvivity(info: RoomChoosingInfo):
    state = info.state

    talk_time = get_time_of_call()
    info.cashier.makeFree()

    state.add_event(
        Event(
            CallEndInfo(state),
            call_end_activity,
            state.curr_time + talk_time
        )
    )

    state.add_cachier_check_event()

def cashiers_check_activity(info: CashiersCheckInfo):
    state = info.state

    if not state.call_waiting_queue_len and not state.payment_queue_len:
        return

    free_cashiers = list(filter(lambda cashier: cashier.free, state.cashiers))

    if not free_cashiers:
        return

    cashier = random.choice(free_cashiers)
    cashier.makeBusy()

    if state.payment_queue_len:
        payment_time = get_time_of_payment()

        cashier.inc_proc_time(payment_time)

        state.add_event(
            Event(
                PaymentEndInfo(state, cashier),
                payment_activity_end,
                state.curr_time + payment_time
            )
        )
    else:
        room_choosing_time = get_time_of_room_choosing()

        cashier.inc_proc_time(room_choosing_time)

        state.add_event(
            Event(
                RoomChoosingInfo(state, cashier),
                end_choose_call_room_atvivity,
                state.curr_time + room_choosing_time
            )
        )

    if len(free_cashiers) == 2:
        cashiers_check_activity(info)

def call_end_activity(info: CallEndInfo):
    state = info.state

    state.inc_payment_queue_len()

    state.add_cachier_check_event()

def payment_activity_end(info: PaymentInfo):
    state = info.state

    info.cashier.makeFree()

    state.add_cachier_check_event()


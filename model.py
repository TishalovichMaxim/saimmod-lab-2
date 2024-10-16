from dataclasses import dataclass

@dataclass
class Visitor:
    id: int
    arrival_time: float
    choosing_call_room_start_time: float
    leave_time: float

class Cashier:
    def __init__(self, id: int) -> None:
        self.id = id
        self._visitors_processing_time = 0
        self.free = True

    def inc_proc_time(self, dt):
        self._visitors_processing_time += dt

    def makeBusy(self):
        self.free = False

    def makeFree(self):
        self.free = True


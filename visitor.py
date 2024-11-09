from dataclasses import dataclass

@dataclass
class Visitor:
    id: int
    arrival_time: float
    choosing_call_room_start_time: float
    leave_time: float


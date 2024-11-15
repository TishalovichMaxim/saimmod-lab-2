from dataclasses import dataclass

@dataclass
class Visitor:
    id: int
    arrival_time: float
    choosing_call_room_start_time: float
    leave_time: float

    def __str__(self) -> str:
        return f"{self.id}: {self.arrival_time}"


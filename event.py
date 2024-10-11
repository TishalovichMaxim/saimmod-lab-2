from typing import Any
from dataclasses import dataclass, field

@dataclass(order=True)
class Event:
    info: Any = field(compare=False)
    activity: Any = field(compare=False)
    time: float


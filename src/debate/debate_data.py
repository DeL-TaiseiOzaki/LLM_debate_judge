from dataclasses import dataclass

@dataclass
class DebateData:
    topic: str
    affirmative_argument: str
    counter_argument: str
    reconstruction: str
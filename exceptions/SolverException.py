
from dataclasses import dataclass

@dataclass
class SolverException(Exception):
    motivation: str
    blackout_len: int
    nerc_id: int

    def __str__(self):
        return f"""
        Solver exception occurred: 
        Blackout events list length for selected nerc: {self.blackout_len}
        Motivation: {self.motivation}
        Selected nerc ID: {
        self.nerc_id
        }
        """
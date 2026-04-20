from math import log as ln
from enum import IntEnum 

class PlayerInitMode(IntEnum):
    NONE = 0
    SIGMA = 1
    CV = 2

class Player:
    def __init__(self, rating: float, hidden: float, s: float | none, mu: float | none):
        self.rating = rating
        self.hidden = hidden
        self.mu = mu ifmu else ln(_rating)
        self.sigma = s

    def __repr__(self):
        return f"${int(self.rating)} %{self.sigma} ({self.sigma/self.mu})% H{self.hidden}H$"



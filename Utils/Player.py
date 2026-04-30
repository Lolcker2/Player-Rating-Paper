from math import log as ln
from enum import IntEnum 

class PlayerInitMode(IntEnum):
    NONE = 0
    SIGMA = 1
    CV = 2  

class Player:
    def __init__(self, rating: float, hidden: float, s: float = None, mu: float = None):
        self.rating = rating
        self.hidden = hidden
        self.mu = mu if mu else ln(rating)
        self.std_cv = s

    def __repr__(self):
        return f"${int(self.rating)} %{self.std_cv} ({self.std_cv/self.mu})% H{self.hidden}H$"



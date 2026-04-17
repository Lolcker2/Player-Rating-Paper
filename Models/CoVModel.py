from math import sqrt, exp, log as ln
from scipy.stats import norm
from typing_extensions import override

from PrevModels import EloProb

class Player:
    def __init__(self, _rating: float, _hidden: float, _cv: float, _mu:float = 0.0):
        self.rating = _rating
        self.hidden = _hidden
        self.mu = ln(_rating) if _mu == 0.0 else _mu
        self.cv = _cv

    def __repr__(self):
        return f"${int(self.rating)} %{self.cv*self.mu} ({self.cv})% H{self.hidden}H$"

def DeltaRating(_a: Player, _b: Player, _u:bool, _prob=0.0) -> float:
    return KAPPA * (int(_u) - EloProb(_a, _b)) if _prob == 0 else KAPPA * (int(_u) - _prob)

def Damp(_num: float, _u: int):
    def sgn(_x):
        return 2*_x - 1
    return _u - sgn(_u) * (32/3) * pow(_num, 3) + sgn(_u) * 16 * pow(_num, 2) - sgn(_u) * (19/3) * _num

# calculate the new cv based on the third formula and clamping its minimum to 0.15
def NewCv(_cv: float, _mu: float, _u: int, _p: float) -> float:
    return max(0.15, _cv + (ETA * Damp(abs(_u - _p), _u) - GAMMA * _cv))

# updating player's delta and cvs based on their match result
def Update(_a: Player, _b: Player, _u: bool):
    prob = EstProb(_a, _b)
    delta = DeltaRating(_a, _b, _u, prob)
    cvs = [NewCv(_a.cv, _a.mu, _u, prob), NewCv(_b.cv, _b.mu, not _u, 1 - prob)]
    return (Player(_a.rating + delta, _a.hidden, cvs[0]),
            Player(_b.rating - delta, _b.hidden, cvs[1]))

# our probability formula
def EstProb(_a: Player, _b: Player)->float:
    return norm.cdf((_a.mu - _b.mu) / sqrt((_a.cv*_a.mu) ** 2 + (_b.cv*_b.mu) ** 2))

def GetStr(_num: float)->float:
    return exp(_num / SCALAR)



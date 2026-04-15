from math import sqrt, exp, log as ln
from scipy.stats import norm

class Player:
    def __init__(self, _rating: float, _hidden: float, _s: float, _mu:float = 0.0):
        self.rating = _rating
        self.hidden = _hidden
        self.mu = ln(_rating) if _mu == 0.0 else _mu
        self.sigma = _s

    def __repr__(self):
        return f"${int(self.rating)} %{self.sigma} ({self.sigma/self.mu})% H{self.hidden}H$"

def DeltaRating(_a: Player, _b: Player, _u:bool, _prob=0.0) -> float:
    return KAPPA * (int(_u) - EloProb(_a, _b)) if _prob == 0 else KAPPA * (int(_u) - _prob)

def Damp(_num: float, _u: int):
    def sgn(_x):
        return 2*_x - 1
    return _u - sgn(_u) * (32/3) * pow(_num, 3) + sgn(_u) * 16 * pow(_num, 2) - sgn(_u) * (19/3) * _num

# calculate the new sigma based on the third formula
def NewSigma(_sigma: float, _u: int, _p: float) -> float:
    return _sigma + (ETA * Damp(abs(_u - _p), _u) - GAMMA * _sigma)

# updating player's delta and sigmas based on their match result
def Update(_a: Player, _b: Player, _u: bool):
    prob = EstProb(_a, _b)
    delta = DeltaRating(_a, _b, _u, prob)
    sigmas = [NewSigma(_a.sigma, _u, prob), NewSigma(_b.sigma, not _u, 1 - prob)]
    return (Player(_a.rating + delta, _a.hidden, sigmas[0]),
            Player(_b.rating - delta, _b.hidden, sigmas[1]))

# our probability formula
def EstProb(_a: Player, _b: Player)->float:
    return norm.cdf((_a.mu - _b.mu) / sqrt(_a.sigma ** 2 + _b.sigma ** 2))

def GetStr(_num: float)->float:
    return exp(_num / SCALAR)


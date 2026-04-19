from math import sqrt, exp, log as ln
from scipy.stats import norm
from Models.PrevModels import EloProb, EstProb, DeltaRating, Damp, GetStr
from Utils.Player import Player



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





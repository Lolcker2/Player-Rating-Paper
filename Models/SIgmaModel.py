from math import sqrt, exp, log as ln
from scipy.stats import norm
from Utils.Player import Player
from Models.PrevModels import EloProb, EstProb, DeltaRating, Damp, GetStr


# calculate the new sigma based on the third formula
def NewSigma(_sigma: float, _u: int, _p: float) -> float:
    return _sigma + (ETA * Damp(abs(_u - _p), _u) - GAMMA * _sigma)

# updating player's delta and sigmas based on their match result
def Update(_a: Player, _b: Player, _u: bool):
    prob = EstProb(_a, _b, True)
    delta = DeltaRating(_a, _b, _u, prob)
    sigmas = [NewSigma(_a.sigma, _u, prob), NewSigma(_b.sigma, not _u, 1 - prob)]
    return (Player(_a.rating + delta, _a.hidden, sigmas[0]),
            Player(_b.rating - delta, _b.hidden, sigmas[1]))



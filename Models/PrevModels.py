from math import exp, log as ln
from Utils.Constants import KAPPA, SCALAR
from Utils.Player import Player


def Damp(_num: float, _u: int):
    def sgn(_x):
        return 2*_x - 1
    return _u - sgn(_u) * (32/3) * pow(_num, 3) + sgn(_u) * 16 * pow(_num, 2) - sgn(_u) * (19/3) * _num

# our probability formula
def EstProb(_a: Player, _b: Player, _sigma: bool)->float:
    if _sigma:
        return norm.cdf((_a.mu - _b.mu) / sqrt(_a.sigma ** 2 + _b.sigma ** 2))
    return norm.cdf((_a.mu - _b.mu) / sqrt((_a.cv*_a.mu) ** 2 + (_b.cv*_b.mu) ** 2))

def DeltaRating(_a: Player, _b: Player, _u:bool, _prob=0.0) -> float:
    return KAPPA * (int(_u) - EloProb(_a, _b)) if _prob == 0 else KAPPA * (int(_u) - _prob)

def Update(_a: Player, _b: Player, _u: bool):
    prob = EloProb(_a, _b)
    delta = DeltaRating(_a, _b, _u, prob)
    return Player(_a.rating + delta, _a.hidden), Player(_b.rating - delta, _b.hidden)

def GetStr(_num: float)->float:
    return exp(_num / SCALAR)

def EloProb(_a: Player, _b: Player, _hidden:bool=False)->float:
    num = round(1 / (1 + exp((_b.hidden - _a.hidden) / SCALAR)), 2) if _hidden else (
        round(1 / (1 + exp((_b.rating - _a.rating) / SCALAR)), 2))
    return num

def BTMProb(_a: Player, _b: Player, _hidden:bool=False)->float:
    a = GetStr(_a.hidden) if _hidden else GetStr(_a.rating)
    b = GetStr(_b.hidden) if _hidden else GetStr(_b.rating)
    num = round(a/(a + b), 2)
    return num

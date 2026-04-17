from Utils.Constants import KAPPA, GAMMA, ETA, START_RATING, RNG, START_CV
from math import log as ln
from Models.PrevModels import BTMProb
from Utils.Player import Player


def NewPlayer(_rating: float, _hidden: float=0.0, _cv: float=None) -> Player:
    if _cv:
        mu = ln(_rating)
        return Player(_rating, _hidden, _cv*mu, mu)
    return Player(_rating, _hidden)


# Create a list of N players, with constant starting data and random "hidden" strength between 1200 and 1500
def Populate(_N: int, _CV: bool=False)->list:
    if _CV:
        return [NewPlayer(START_RATING, int(1300 + 400*RNG.random()), START_CV) for _ in range(_N)]
    return [NewPlayer(START_RATING, int(1300 + 200*RNG.random())) for _ in range(_N)]


def GetIndex(_n: float, _l: int) -> int:
    return int(_n * _l)

# Generate the result of ~N matches
# each result is the tuple (a: index, b; index, a_win?: bool)
# the outcome of a match is random yet weighted by the expected probability of the braddly terry model
# ~N matches due to filtering matches between a player with himself
def Results(_pop:list, _matches: int):
    def generate(_pop: list, _matches: int)->list:
        length = len(_pop)
        results = RNG.random(size=(_matches, length, 3))
        return [[GetIndex(r[0], length), GetIndex(r[1], length),
                 bool(r[2] < BTMProb(_pop[GetIndex(r[0], length)], _pop[GetIndex(r[1], length)], True))]
                for result in results for r in result]
    return [item for item in generate(_pop, _matches) if item[0] != item[1]]


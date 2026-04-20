from Utils.Constants import KAPPA, GAMMA, ETA, START_RATING, RNG, START_CV, START_SIGMA
from math import log as ln
from Models.PrevModels import BTMProb, EloProb
from Utils.Player import Player, PlayerInitMode


def NewPlayer(rating: float, hidden: float=0.0, sigma_cv: float | none, init_mode: PlayerInitMode = PlayerInitMode.NONE) -> Player:
    if sigma_cv:
        mu = ln(rating)
        return  Player(rating, hidden, sigma_cv*mu, mu) if init_mode == PlayerInitMode.CV else Player(rating, hidden, sigma_cv, mu) 
    return Player(rating, hidden)


# Create a list of N players, with constant starting data and random "hidden" strength between 1200 and 1500
# 0 elo-btm, 1 sigma, 2 cv
def Populate(_N: int, init_mode: PlayerInitMode = PlayerInitMode.NONE)->list:
    match SCV:
        case PlayerInitMode.NONE:
            return [NewPlayer(START_RATING, int(1300 + 200*RNG.random())) for  in range(_N)]
        case PlayerInitMode.SIGMA:
            return [NewPlayer(START_RATING, int(1300 + 400*RNG.random()), START_SIGMA) for  in range(_N)]
        case PlayerInitMode.CV:
            return [NewPlayer(START_RATING, int(1300 + 400*RNG.random()), START_CV) for  in range(_N)]
    


def GetIndex(n: float, l: int) -> int:
    return int(n * l)

# Generate the result of ~N matches
# each result is the tuple (a: index, b; index, a_win?: bool)
# the outcome of a match is random yet weighted by the expected probability of the braddly terry model
# ~N matches due to filtering matches between a player with himself
def Results(population:list, matches: int, BTM: bool=False):
    def generateBTM(population: list, matches: int)->list:
        length = len(population)
        results = RNG.random(size=(matches, length, 3))
        return [[GetIndex(r[0], length), GetIndex(r[1], length),
                 bool(r[2] < BTMProb(population[GetIndex(r[0], length)], pop[GetIndex(r[1], length)], True))]
                for result in results for r in result]

    def generateELO(population: list, matches: int)->list:
        length = len(population)
        results = RNG.random(size=(matches, length, 3))
        return [[GetIndex(r[0], length), GetIndex(r[1], length),
                    bool(r[2] < EloProb(population[GetIndex(r[0], length)], pop[GetIndex(r[1], length)], True))]
                for result in results for r in result]
    if BTM:
        return [item for item in generateBTM(population, matches) if item[0] != item[1]]
    return [item for item in generateELO(population, matches) if item[0] != item[1]]

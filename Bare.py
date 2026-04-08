from math import sqrt, exp, log as ln
from scipy.stats import norm
from numpy.random import default_rng


KAPPA = 1
ETA = 10
GAMMA = 2
SCALAR = 400
START_RATING = 1000
START_CV = 0.2
RNG = default_rng()

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

# get the elo model preceived probability
def EloProb(_a: Player, _b: Player, _hidden:bool=False)->float:
    num = round(1 / (1 + exp((_b.hidden - _a.hidden) / SCALAR)), 2) if _hidden else (
        round(1 / (1 + exp((_b.rating - _a.rating) / SCALAR)), 2))
    return num

def GetStr(_num: float)->float:
    return exp(_num / SCALAR)


################################################################################################################
#                                             Model      /       Players                                       #
################################################################################################################


def NewPlayer(_rating: float, _hidden: float, _cv: float) -> Player:
    mu = ln(_rating)
    return Player(_rating, _hidden, _cv, mu)

# Create a list of N players, with constant starting data and random "hidden" strength between 1200 and 1500
def Populate(_N: int)->list:
    return [NewPlayer(START_RATING, int(1300 + 400*RNG.random()), START_CV) for _ in range(_N)]

def GetIndex(_n: float, _l: int) -> int:
    return int(_n * _l)

# Generate the result of ~N matches
# each result is the tuple (a: index, b; index, a_win?: bool)
# the outcome of a match is random yet weighted by the expected probability of the Elo model
# ~N matches due to filtering matches between a player with himself
def Results(_pop:list, _matches: int):
    def generate(_pop: list, _matches: int)->list:
        length = len(_pop)
        results = RNG.random(size=(_matches, length, 3))
        return [[GetIndex(r[0], length), GetIndex(r[1], length),
                 bool(r[2] < EloProb(_pop[GetIndex(r[0], length)], _pop[GetIndex(r[1], length)], True))]
                for result in results for r in result]
    return [item for item in generate(_pop, _matches) if item[0] != item[1]]

# Simulates the population of players, takes snapshots regularly.
def Itterate(_N: int, _matches: int, _snapshot:int = 1000):
    population = Populate(_N)
    results = Results(population, _matches)
    for i in range(len(results)):
        result = results[i]

        population[result[0]], population[result[1]] = Update(population[result[0]], population[result[1]], result[2])

        if i % _snapshot == 0:
            global snapshot_num
            snapshot_num += 1

            print('\n')
            snap_list = [f"{player.cv *  player.mu}, {player.cv}" for player in sorted(population, key=lambda x: x.cv / x.mu)]
            with open(f"Snapshot@{i/_snapshot}", "w") as f:
                f.write('\n'.join(snap_list))

            print(f"--- Snapshot @ {i} ---")

    final_snapshot = ""
    for player in sorted(population, key=lambda obj: obj.hidden):
        final_snapshot += f"{player.hidden},{int(player.rating)}\n"
    with open("log", "w") as f:
        f.write(final_snapshot)



from math import sqrt, exp, log as ln
from scipy.stats import norm
from numpy.random import default_rng

class Player:
    def __init__(self, _rating: float, _hidden: float, _s: float, _mu:float = 0.0):
        self.rating = _rating
        self.hidden = _hidden
        self.mu = ln(_rating) if _mu == 0.0 else _mu
        self.sigma = _s

    def __repr__(self):
        return f"${int(self.rating)} %{self.sigma*self.mu} ({self.sigma})% H{self.hidden}H$"

def DeltaRating(_a: Player, _b: Player, _u:bool, _prob=0.0) -> float:
    return KAPPA * (int(_u) - EloProb(_a, _b)) if _prob == 0 else KAPPA * (int(_u) - _prob)

def Damp(_num: float, _u: int):
    def sgn(_x):
        return 2*_x - 1
    return _u - sgn(_u) * (32/3) * pow(_num, 3) + sgn(_u) * 16 * pow(_num, 2) - sgn(_u) * (19/3) * _num

def NewSigma(_sigma: float, _mu: float, _u: int, _p: float) -> float:
    # if snapshot_num == 9:
    #     print(f"{Damp(abs(_u - _p), _u)} | {abs(_u - _p)} | {_sigma}")
    return max(0.15, _sigma + (ETA * Damp(abs(_u - _p), _u) - GAMMA * _sigma))

def Update(_a: Player, _b: Player, _u: bool):
    prob = EstProb(_a, _b)
    delta = DeltaRating(_a, _b, _u, prob)
    sigmas = [NewSigma(_a.sigma, _a.mu, _u, prob), NewSigma(_b.sigma, _b.mu, not _u, 1 - prob)]
    # print(sigmas)
    return (Player(_a.rating + delta, _a.hidden, sigmas[0]),
            Player(_b.rating - delta, _b.hidden, sigmas[1]))

def EstProb(_a: Player, _b: Player)->float:
    return norm.cdf((_a.mu - _b.mu) / sqrt((_a.sigma) ** 2 + (_b.sigma) ** 2))

def EloProb(_a: Player, _b: Player, _hidden:bool=False)->float:
    num = round(1 / (1 + exp((_b.hidden - _a.hidden) / SCALAR)), 2) if _hidden else (
        round(1 / (1 + exp((_b.rating - _a.rating) / SCALAR)), 2))
    return num

def GetStr(_num: float)->float:
    return exp(_num / SCALAR)

def BTMProb(_a: Player, _b: Player, _hidden:bool=False)->float:
    a = GetStr(_a.hidden) if _hidden else GetStr(_a.rating)
    b = GetStr(_b.hidden) if _hidden else GetStr(_b.rating)
    num = round(a/(a + b), 2)
    return num


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
# the outcome of a match is random yet weighted by the expected probability of the braddly terry model
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
            snap_list = [f"{player.sigma *  player.mu}, {player.sigma}" for player in sorted(population, key=lambda x: x.sigma / x.mu)]
            with open(f"Snapshot@{i/_snapshot}", "w") as f:
                f.write('\n'.join(snap_list))

            print(f"--- Snapshot @ {i} ---")

    final_snapshot = ""
    for player in sorted(population, key=lambda obj: obj.hidden):
        final_snapshot += f"{player.hidden},{int(player.rating)}\n"
    with open("log", "w") as f:
        f.write(final_snapshot)


if __name__ == '__main__':
    snapshot_num = 0
    KAPPA = 1
    ETA = 10
    GAMMA = 2
    SCALAR = 400
    START_RATING = 1000
    START_CV = 0.2
    RNG = default_rng()

    Itterate(1_000, 1_000, _snapshot=100_000)



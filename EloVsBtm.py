from math import exp, log as ln
from numpy.random import default_rng

class Player:
    def __init__(self, _rating: float, _hidden: float):
        self.rating = _rating
        self.hidden = _hidden

    def __repr__(self):
        return f"${self.rating} H{self.hidden}H$"

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


################################################################################################################
#                                             Model      /       Players                                       #
################################################################################################################


def NewPlayer(_rating: float, _hidden: float=0.0) -> Player:
    return Player(_rating, _hidden)

# Create a list of N players, with constant starting data and random "hidden" strength between 1200 and 1500
def Populate(_N: int)->list:
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

# Simulates the population of players, takes snapshots regularly.
def Itterate(_N: int, _matches: int, _snapshot:int = 1000):
    population = Populate(_N)
    results = Results(population, _matches)
    for i in range(len(results)):
        result = results[i]

        population[result[0]], population[result[1]] = Update(population[result[0]], population[result[1]], result[2])

        if i % _snapshot == 0:
            print(f"--- Snapshot @ {i} ---")
            for player in population:
                print(f"{player.hidden},{int(player.rating)}")
            print('\n')

    final_snapshot = ""
    for player in sorted(population, key=lambda obj: obj.hidden):
        final_snapshot += f"{player.hidden},{int(player.rating)}\n"
    with open("log", "w") as f:
        f.write(final_snapshot)


if __name__ == '__main__':
    KAPPA = 5
    SCALAR = 160
    START_RATING = 600
    RNG = default_rng()

    Itterate(1_000, 1_000, _snapshot=100_000)
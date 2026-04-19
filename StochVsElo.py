from math import sqrt, exp, log as ln
from scipy.stats import norm
from numpy.random import default_rng
from Utils.Player import Player
from Utils.Constants import *
from Utils.Population import *
from Models.PrevModels import DeltaRating, Damp

# calculate the new sigma based on the third formula
def NewSigma(_sigma: float, _u: int, _p: float) -> float:
    if snapshot_num == 9:
        print(f"{Damp(abs(_u - _p), _u)} | {abs(_u - _p)} | {_sigma}")
    return _sigma+ (ETA * Damp(abs(_u - _p), _u) - GAMMA * _sigma)

# updating player's delta and sigmas based on their match result
def Update(_a: Player, _b: Player, _u: bool):
    prob = EstProb(_a, _b)
    delta = DeltaRating(_a, _b, _u, prob)
    sigmas = [NewSigma(_a.sigma, _u, prob), NewSigma(_b.sigma, not _u, 1 - prob)]
    # print(sigmas)
    return (Player(_a.rating + delta, _a.hidden, sigmas[0]),
            Player(_b.rating - delta, _b.hidden, sigmas[1]))

# our probability formula
def EstProb(_a: Player, _b: Player)->float:
    return norm.cdf((_a.mu - _b.mu) / sqrt(_a.sigma ** 2 + _b.sigma ** 2))



# Simulates the population of players, takes snapshots regularly.
def Itterate(_N: int, _matches: int, _snapshot:int = 1000):
    population = Populate(_N, 1)
    results = Results(population, _matches)
    for i in range(len(results)):
        result = results[i]

        population[result[0]], population[result[1]] = Update(population[result[0]], population[result[1]], result[2])

        if i % _snapshot == 0:
            global snapshot_num
            snapshot_num += 1

            print('\n')
            snap_list = [f"{player.sigma}, {player.sigma / player.mu}" for player in sorted(population, key=lambda x: x.sigma / x.mu)]
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
    Itterate(10, 10, _snapshot=10)
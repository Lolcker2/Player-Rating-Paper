from math import sqrt, exp, log as ln
from scipy.stats import norm
from numpy.random import default_rng
from Utils.Player import Player
from Utils.Constants import *
from Utils.Population import *
from Models.PrevModels import DeltaRating, Damp

# calculate the new sigma based on the third formula
def NewSigma(sigma: float, utility: int, probability: float) -> float:
    if snapshot_num == 9:
        print(f"{Damp(abs(utility - probability), utility)} | {abs(utility - probability)} | {sigma}")
    return sigma+ (ETA * Damp(abs(utility - probability), utility) - GAMMA * sigma)

# updating player's delta and sigmas based on their match result
def Update(player_a: Player, player_b: Player, utility: bool):
    prob = EstProb(player_a, player_b)
    delta = DeltaRating(player_a, player_b, utility, prob)
    sigmas = [NewSigma(player_a.sigma, utility, prob), NewSigma(player_b.sigma, not utility, 1 - prob)]
    # print(sigmas)
    return (Player(player_a.rating + delta, player_a.hidden, sigmas[0]),
            Player(player_b.rating - delta, player_b.hidden, sigmas[1]))

# our probability formula
def EstProb(player_a: Player, player_b: Player)->float:
    return norm.cdf((player_a.mu - player_b.mu) / sqrt(player_a.sigma ** 2 + player_b.sigma ** 2))



# Simulates the population of players, takes snapshots regularly.
def Iterate(_N: int, matches: int, snapshot:int = 1000):
    population = Populate(_N, PlayerInitMode.SIGMA)
    results = Results(population, matches)
    for i in range(len(results)):
        result = results[i]

        population[result[0]], population[result[1]] = Update(population[result[0]], population[result[1]], result[2])

        if i % snapshot == 0:
            global snapshot_num
            snapshot_num += 1

            print('\n')
            snap_list = [f"{player.sigma}, {player.sigma / player.mu}" for player in sorted(population, key=lambda x: x.sigma / x.mu)]
            with open(f"Snapshot@{i/snapshot}", "w") as f:
                f.write('\n'.join(snap_list))

            print(f"--- Snapshot @ {i} ---")

    finalsnapshot = ""
    for player in sorted(population, key=lambda obj: obj.hidden):
        finalsnapshot += f"{player.hidden},{int(player.rating)}\n"
    with open("log", "w") as f:
        f.write(finalsnapshot)


if __name__ == '__main__':
    snapshot_num = 0
    Iterate(10, 10, snapshot=10)
from math import sqrt, exp, log as ln
from scipy.stats import norm
from numpy.random import default_rng
from Utils.Player import Player
from Utils.Constants import *
from Utils.Population import *
from Models.PrevModels import DeltaRating, Damp, EstProb
import Models.CoVModel as cov
import Models.SigmaModel as smodel



# Simulates the population of players, takes snapshots regularly.
def Iterate(_N: int, matches: int, snapshot:int = 1000):
    population = Populate(_N, PlayerInitMode.SIGMA)
    results = Results(population, matches)
    for i in range(len(results)):
        result = results[i]

        population[result[0]], population[result[1]] = smodel.Update(population[result[0]], population[result[1]], result[2])

        if i % snapshot == 0:
            global snapshot_num
            snapshot_num += 1

            print('\n')
            snap_list = [f"{player.std_cv}, {player.std_cv / player.mu}" for player in sorted(population, key=lambda x: x.std_cv / x.mu)]
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
from math import sqrt, exp, log as ln
from scipy.stats import norm
from numpy.random import default_rng
from Utils.Player import Player
from Utils.Constants import *
from Utils.Population import *
from Models.PrevModels import DeltaRating, Damp, EstProb
import Models.CoVModel as cov
import Models.SigmaModel as smodel


# Results comes from utils.population and compares elo and btm
# change the method below to elo vs stoch
# also y uses hidden??

# Generate the result of ~N matches
# each result is the tuple (a: index, b; index, a_win?: bool)
# the outcome of a match is random yet weighted by the expected probability of the braddly terry model
# ~N matches due to filtering matches between a player with himself
def Results(population:list, matches: int, ELO: bool=False):
    def generateSTOCH(population: list, matches: int)->list:
        length = len(population)
        results = RNG.random(size=(matches, length, 3))
        return [[GetIndex(r[0], length), GetIndex(r[1], length),
                 bool(r[2] < EstProb(population[GetIndex(r[0], length)], population[GetIndex(r[1], length)], PlayerInitMode.CV))]
                for result in results for r in result]

    def generateELO(population: list, matches: int)->list:
        length = len(population)
        results = RNG.random(size=(matches, length, 3))
        return [[GetIndex(r[0], length), GetIndex(r[1], length),                                                # ?
                    bool(r[2] < EloProb(population[GetIndex(r[0], length)], population[GetIndex(r[1], length)], True))]
                for result in results for r in result]
    if ELO:
        return [item for item in generateELO(population, matches) if item[0] != item[1]]
    return [item for item in generateSTOCH(population, matches) if item[0] != item[1]]

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
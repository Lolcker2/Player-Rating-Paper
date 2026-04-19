from math import exp, log as ln
from numpy.random import default_rng
from Utils.Constants import *
from Utils.Population import *
from Utils.Player import Player


# Simulates the population of players, takes snapshots regularly.
def Iterate(_N: int, matches: int, snapshot:int = 1000):
    population = Populate(_N)
    results = Results(population, matches, True)
    for i in range(len(results)):
        result = results[i]

        population[result[0]], population[result[1]] = Update(population[result[0]], population[result[1]], result[2])

        if i % snapshot == 0:
            print(f"--- Snapshot @ {i} ---")
            for player in population:
                print(f"{player.hidden},{int(player.rating)}")
            print('\n')

    finalsnapshot = ""
    for player in sorted(population, key=lambda obj: obj.hidden):
        finalsnapshot += f"{player.hidden},{int(player.rating)}\n"
    with open("log", "w") as f:
        f.write(finalsnapshot)


if __name__ == '__main__':
    Iterate(10, 10, snapshot=10)
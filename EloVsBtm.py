from math import exp, log as ln
from numpy.random import default_rng
from Utils.Constants import *
from Utils.Population import *
from Utils.Player import Player


# Simulates the population of players, takes snapshots regularly.
def Itterate(_N: int, _matches: int, _snapshot:int = 1000):
    population = Populate(_N)
    results = Results(population, _matches, True)
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
    Itterate(10, 10, _snapshot=10)
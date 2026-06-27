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
def NaiveMatchmaking(_N: int, matches: int, snapshot:int = 1000):
    population = Populate(_N, PlayerInitMode.SIGMA)
    results = Results(population, matches)
    saveSnapshots(parseResults(population, results, snapshot, PlayerInitMode.SIGMA))


    # final rating snapshot
    finalsnapshot = ""
    for player in sorted(population, key=lambda obj: obj.hidden):
        finalsnapshot += f"{player.hidden},{int(player.rating)}\n"
    with open("log", "w") as f:
        f.write(finalsnapshot)

# Simulates the population of players all divided into brackets, takes snapshots regularly.
def BracketMatchmaking(_N: int, matches: int, bracketSize: int, snapshot:int = 1000):
    population = sorted(Populate(_N, PlayerInitMode.SIGMA), key=lambda obj: obj.hidden)
    finalPopulation = [] # an aggragate of all brackets

    # dividing the populations to brackets
    for i in range(0, _N, bracketSize):
        bracket = population[i: i + bracketSize]
        results = Results(bracket, matches)
        saveSnapshots(parseResults(bracket, results, snapshot, PlayerInitMode.SIGMA), suffix=f"[{(i+bracketSize) // bracketSize}]")
        finalPopulation.extend(bracket) # add bracket to the aggragate

    # final rating snapshot
    finalsnapshot = ""
    for player in sorted(finalPopulation, key=lambda obj: obj.hidden):
        finalsnapshot += f"{player.hidden},{int(player.rating)}\n"
    with open("log", "w") as f:
        f.write(finalsnapshot)

# add a snapshot style macro

# Loops though all results updating the population accordingly
# returns a list of snapshots
def parseResults(population: list, results: list, snapshot:int = 1000, model:PlayerInitMode = PlayerInitMode.SIGMA) -> list[str]:
    snapshot_num = 0
    snapshot_list = []

    for i in range(len(results)):
        result = results[i]

        if model == PlayerInitMode.SIGMA: # using std
            population[result[0]], population[result[1]] = smodel.Update(population[result[0]], population[result[1]], result[2])
        else: # using cv
            population[result[0]], population[result[1]] = cov.Update(population[result[0]], population[result[1]], result[2])
        
        # snapshot handling
        if i % snapshot == 0:
            snapshot_num += 1
            snapshot_list.append([f"{player.std_cv}, {player.std_cv / player.mu}" for player in sorted(population, key=lambda x: x.std_cv / x.mu)])
    
    # last snapshot
    snapshot_list.append([f"{player.std_cv}, {player.std_cv / player.mu}" for player in sorted(population, key=lambda x: x.std_cv / x.mu)])
    return snapshot_list

# save all snapshots to local files
def saveSnapshots(snap_list: list[str], suffix:str=""):
    for i in range(len(snap_list)):
        with open(f"Snapshots/Snapshot@{i+1}{suffix}", "w") as f:
            f.write('\n'.join(snap_list[i]))



if __name__ == '__main__':
    # snapshot_num = 0
    # NaiveMatchmaking(10, 10, snapshot=10)
    BracketMatchmaking(10, 10, 5, snapshot=10)


"""
write a macro for styling / deciding what goes into the snapshots

    def macro_print(func):
        def wrapper(*args, **kwargs):
            # Executes your function
            result = func(*args, **kwargs)
            # Accesses the variable from the function's local scope
            print(f"Variable 'num' is: {result}")
            return result
        return wrapper

    @macro_print
    def get_num():
        num = 100
        return num

    get_num()


"""
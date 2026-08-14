import Models.CoVModel as cov
import Models.SigmaModel as smodel
from itertools import combinations
from Models.PrevModels import EstProb, EloProb, Update as EloUpdate
from Utils.Player import Player, PlayerInitMode


ResultWeights = {"1-0": 1, "0-1": 0, "½-½": 0.5, "Â½-Â½": 0.5}

# float format
def ff(f):
    return f"{f:.2f}"

def getMatch(_data: list, _index: int, _match: list = False)->list:
    match, result = _match.split('|') if _match else _data[_index].split('|')
    p1, p2 = match.split("VS")
    return [int(p1), int(p2), int(result)]


# build hetroskedastic version with tailing cv between opponents?
# defines an epoch, simulates and evolves one player's rating
def historicalConvergence(data, ELO:bool=False):
    data = [getMatch([], 0, match) for match in data] # getting all the matches

    aggragate = ""   # aggragate of the results
    sigma_cv = 0.06 # ----
    epoch = data[-1]
    print(f"epoch: {epoch}")
    
    # fetching players form the epoch
    testedPlayer = Player(epoch[0], 1, sigma_cv)
    secondPlayer = Player(epoch[1], 1, sigma_cv)

    # lagged by one, meaning starts at the second and ends 1 loop after the last
    for i in range(len(data) - 2, 0, -1):
        result = data[i]
        
        # updating and repurposing players
        if ELO:
            testedPlayer, junk = EloUpdate(testedPlayer, secondPlayer, bool(result[2]))
        else:
            testedPlayer, junk = cov.Update(testedPlayer, secondPlayer, bool(result[2]))
            testedPlayer.std_cv = sigma_cv # assuming homoskedacity

        aggragate += f"Expected[{ff(testedPlayer.rating)}] vs Actual({result[0]})\n"
        secondPlayer.rePurpose(result[1], 1, sigma_cv)
    
    with open(f"Snapshots/HistoricalCon{' [Elo]' if ELO else ''}", "w") as f:
        f.write(aggragate)

# done
# build hetroskedastic version with tailing cv between opponents?

# Tests how accurate the elo and the stochastic formulas are at predicting the result of a match 
def predictiveTest(data: list):
    data = [getMatch([], 0, match) for match in data] # getting all the matches

    players = [Player(1, 1), Player(1, 1)]
    sigma_cv = 0.2 # ----
    aggragate = "" # aggragate of the results

    for match in data:
        [players[i].rePurpose(match[i], 1, sigma_cv) for i in range(len(players))]
        elo = EloProb(*players)
        stoch = EstProb(*players, PlayerInitMode.CV) # -----
        aggragate += f"E({elo}) vs S({(ff(stoch))}): ~{match[2]}~\n"
    
    with open(f"Snapshots/PredictiveTest", "w") as f:
        f.write(aggragate)


#-----------------------------------------------------

def CardinalityTest(data: list):
    
    data = [entry.split(",") for entry in data]
    population = [Player(int(entry[1]), int(entry[0]), float(entry[2])) for entry in data]

    # get all pairs of players
    pairs = list(combinations(set(population), 2))

    aggragate = "" # aggragate of the results

    for players in pairs:
        elo = EloProb(*players)
        stoch = EstProb(*players, PlayerInitMode.CV) # -----
        aggragate += f"E({elo}) vs S({(ff(stoch))}): ~{match[2]}~\n"

    with open(f"Snapshots/CardTest", "w") as f:
        f.write(aggragate)


if __name__ == '__main__':
    filename = 'carlsen magnus-unified_matches'
    # data = open(r'Cache/' + filename + '.txt', "r").read().split('\n')
    data = open(r"./log", "r").read().split('\n')
    # print(data)
    CardinalityTest(data)
import Models.CoVModel as cov
import Models.SigmaModel as smodel
from Models.PrevModels import EstProb, EloProb
from Utils.Player import Player, PlayerInitMode


ResultWeights = {"1-0": 1, "0-1": 0, "½-½": 0.5, "Â½-Â½": 0.5}

# float format
def ff(f):
    return f"{f:.2f}"

def reOrient(_match: list, _name: str):
    if _match[1][0] == _name:
        return [_match[1], _match[0], -1 * _match[2] + 1] 
    return  _match

def getMatch(_data: list, _index: int, _match: list = False)->list:
    match, result = _match.split('|') if _match else _data[_index].split('|')
    p1, p2 = [i.split(',') for i in match.split("VS")]
    p1[1], p2[1] = int(p1[1]), int(p2[1])
    p2[0] = p2[0].lstrip()
    return [p1, p2, ResultWeights[result.strip()]]



# build hetroskedastic version with tailing cv between opponents?

# defines an epoch, simulates and evolves one player's rating
def historicalConvergence(data):
    # filtering all draws
    data = [reOrient(getMatch([], 0, match), "Magnus Carlsen") for match in data] # reOrienting all matches
    data = [match for match in data if float.is_integer(float(match[2]))] # filtering out draws

    aggragate = ""   # aggragate of the results
    sigma_cv = 0.06 # ----
    epoch = data[1]
    
    # fetching players form the epoch
    testedPlayer = Player(epoch[0][1], 1, sigma_cv)
    secondPlayer = Player(epoch[1][1], 1, sigma_cv)

    # lagged by one, meaning starts at the second and ends 1 loop after the last
    for i in range(len(data) - 2, -2, -1):
        result = data[i]
        
        # updating and repurposing players
        testedPlayer, junk = cov.Update(testedPlayer, secondPlayer, bool(result[2]))
        testedPlayer.std_cv = sigma_cv # assuming homoskedacity

        aggragate += f"E[{ff(testedPlayer.rating)}] vs A({result[0][1]})\n"
        secondPlayer.rePurpose(result[1][1], 1, sigma_cv)
    
    with open(f"Snapshots/HistoricalCon", "w") as f:
        f.write(aggragate)

# done
# build hetroskedastic version with tailing cv between opponents?

# Tests how accurate the elo and the stochastic formulas are at predicting the result of a match 
def predictiveTest(data):
    data = [reOrient(getMatch([], 0, match), "Magnus Carlsen") for match in data] # reOrienting all matches
    data = [match for match in data if float.is_integer(float(match[2]))] # filtering out draws

    players = [Player(1, 1), Player(1, 1)]
    sigma_cv = 0.06 # ----
    aggragate = "" # aggragate of the results

    for match in data:
        [players[i].rePurpose(match[i][1], 1, sigma_cv) for i in range(len(players))]
        elo = EloProb(*players)
        stoch = EstProb(*players, PlayerInitMode.CV)
        aggragate += f"E({elo}) vs S({(ff(stoch))}): ~{match[2]}~\n"
    
    with open(f"Snapshots/PredictiveTest", "w") as f:
        f.write(aggragate)

if __name__ == '__main__':
    filename = 'Magnus Carlsen-100_matches'
    data = open(r'Cache/' + filename + '.txt', "r").read().split('\n')
    print(data)

    #historicalConvergence(data)
    predictiveTest(data)

"""
    Magnus Carlsen, 3338 VS Alireza Firouzja, 3287 | ½-½
    Magnus Carlsen, 3328 VS Alireza Firouzja, 3297 | ½-½
    Magnus Carlsen, 3334 VS Alireza Firouzja, 3291 | ½-½
    Magnus Carlsen, 3206 VS Alireza Firouzja, 3303 | ½-½

    3338 3287 |+10 -10
    3328 3297 |-6 +6
    3334 3291 |+128 -12
    3206 3303 |
"""
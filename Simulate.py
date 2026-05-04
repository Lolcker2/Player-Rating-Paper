import Models.CoVModel as cov
import Models.SigmaModel as smodel
from Models.PrevModels import EstProb, EloProb
from Utils.Player import Player, PlayerInitMode


filename = 'Magnus Carlsen-100_matches'
data = open(r'Cache/'+filename+'.txt', "r").read().split('\n')
# print(data)

ResultWeights = {"1-0": 1, "½-½": 0, "0-1": -1, "Â½-Â½": 0}

def reOrient(_match: list, _name: str):
    if _match[1][0] == _name:
        return [_match[1], _match[0], -1 * _match[2]]
    return  _match

def getMatch(_data: list, _index: int, _match: list = False)->list:
    match, result = _match.split('|') if _match else _data[_index].split('|')
    p1, p2 = [i.split(',') for i in match.split("VS")]
    p1[1], p2[1] = int(p1[1]), int(p2[1])
    p2[0] = p2[0].lstrip()
    return [p1, p2, ResultWeights[result.strip()]]

#print(getMatch(data, 0))



def predictiveTest(data):
    players = [Player(1, 1), Player(1, 1)]
    
    sigma_cv = 0.1
    for match in data:
        result = reOrient(getMatch([], 0, match), "Magnus Carlsen")
        [players[i].rePurpose(result[i][1], 1, sigma_cv) for i in range(len(players))]
        elo = EloProb(*players)
        stoch = EstProb(*players, PlayerInitMode.CV)
        print(stoch)

predictiveTest(data)

"""
divide into 2 parts:
    predictive elo vs stoch on historical data
    convergance - epoch + evolution


todo: find where i use the model and outsource it to a standalone file
note look at Model and Model2 see if there's anything useful.

loop -> getMatch
-> reOrient -> feed model
"""
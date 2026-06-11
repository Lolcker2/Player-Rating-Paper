import Models.CoVModel as cov
import Models.SigmaModel as smodel
from Models.PrevModels import EstProb, EloProb
from Utils.Player import Player, PlayerInitMode


filename = 'Magnus Carlsen-100_matches'
data = open(r'Cache/'+filename+'.txt', "r").read().split('\n')
# print(data)

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

#print(getMatch(data, 0))


# build hetroskedastic version with tailing cv between opponents?
def historicalConvergence(data):
    # filtering all draws
    data = [reOrient(getMatch([], 0, match), "Magnus Carlsen") for match in data] # reOrienting all matches
    data = [match for match in data if float.is_integer(float(match[2]))] # filtering out draws

    sigma_cv = 0.06
    epoch = data[1]
    print(f"epoch {epoch}")
    testedPlayer = Player(epoch[0][1], 1, sigma_cv)
    secondPlayer = Player(epoch[1][1], 1, sigma_cv)

    # lagged by one meaning starts at the second and ends 1 after the last
    for i in range(len(data) - 2, -2, -1):
        result = data[i]
        
        # updating and repurposing players
        testedPlayer, junk = cov.Update(testedPlayer, secondPlayer, bool(result[2]))
        testedPlayer.std_cv = sigma_cv # assuming homoskedacity

        print(f"E[{ff(testedPlayer.rating)}] vs A({result[0][1]})")
        secondPlayer.rePurpose(result[1][1], 1, sigma_cv)

# done
# build hetroskedastic version with tailing cv between opponents?
def predictiveTest(data):
    players = [Player(1, 1), Player(1, 1)]
    sigma_cv = 0.06

    for match in data:
        result = reOrient(getMatch([], 0, match), "Magnus Carlsen")
        [players[i].rePurpose(result[i][1], 1, sigma_cv) for i in range(len(players))]
        elo = EloProb(*players)
        stoch = EstProb(*players, PlayerInitMode.CV)
        print(f"E({elo}) vs S({(ff(stoch))}): ~{result[2]}~")

historicalConvergence(data)

"""
divide into 2 parts:
    predictive elo vs stoch on historical data
    convergance - epoch + evolution


todo: find where i use the model and outsource it to a standalone file
note look at Model and Model2 see if there's anything useful.

loop -> getMatch
-> reOrient -> feed model








Magnus Carlsen, 3338 VS Alireza Firouzja, 3287 | ½-½
Magnus Carlsen, 3328 VS Alireza Firouzja, 3297 | ½-½
Magnus Carlsen, 3334 VS Alireza Firouzja, 3291 | ½-½
Magnus Carlsen, 3206 VS Alireza Firouzja, 3303 | ½-½

3338 3287 |+10 -10
3328 3297 |-6 +6
3334 3291 |+128 -12
3206 3303 |



"""
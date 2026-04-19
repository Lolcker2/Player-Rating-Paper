

filename = 'Magnus Carlsen-100_matches'
data = open(r'Cache/'+filename+'.txt', "r").read().split('\n')
print(data)

ResultWeights = {"1-0": 1, "½-½": 0, "0-1": -1}

def reOrient(match: list, name: str):
    if _match[1][0] == _name:
        return [_match[1], _match[0], -1 * _match[2]]
    return  _match

def getMatch(_data: list, _index: int)->list:
    match, result = _data[_index].split('|')
    p1, p2 = [i.split(',') for i in match.split("VS")]
    p1[1], p2[1] = int(p1[1]), int(p2[1])
    p2[0] = p2[0].lstrip()
    return [p1, p2, ResultWeights[result.strip()]]

print(getMatch(data, 0))




"""
todo: find where i use the model and outsource it to a standalone file
note look at Model and Model2 see if there's anything useful.

loop -> getMatch
-> reOrient -> feed model
"""
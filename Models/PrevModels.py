from math import exp, log as ln

def EloProb(_a: Player, _b: Player, _hidden:bool=False)->float:
    num = round(1 / (1 + exp((_b.hidden - _a.hidden) / SCALAR)), 2) if _hidden else (
        round(1 / (1 + exp((_b.rating - _a.rating) / SCALAR)), 2))
    return num

def BTMProb(_a: Player, _b: Player, _hidden:bool=False)->float:
    a = GetStr(_a.hidden) if _hidden else GetStr(_a.rating)
    b = GetStr(_b.hidden) if _hidden else GetStr(_b.rating)
    num = round(a/(a + b), 2)
    return num

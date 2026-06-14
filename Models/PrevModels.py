from math import sqrt, exp, log as ln
from scipy.stats import norm
from Utils.Constants import KAPPA, SCALAR
from Utils.Player import Player, PlayerInitMode

# Damping function
def Damp(num: float, utility: int):
    def sgn(x):
        return 2*x - 1
    return utility - sgn(utility) * (32/3) * pow(num, 3) + sgn(utility) * 16 * pow(num, 2) - sgn(utility) * (19/3) * num

# Stochastic probability formula
def EstProb(player_a: Player, player_b: Player, init_mode: PlayerInitMode = PlayerInitMode.NONE)->float:
    if init_mode == PlayerInitMode.SIGMA:
        return norm.cdf((player_a.mu - player_b.mu) / sqrt(player_a.std_cv ** 2 + player_b.std_cv ** 2))
    return norm.cdf((player_a.mu - player_b.mu) / sqrt((player_a.std_cv*player_a.mu) ** 2 + (player_b.std_cv*player_b.mu) ** 2))

# Universal delta rating formula k(u_a - p(a > b))
def DeltaRating(player_a: Player, player_b: Player, utility:bool, probability=0.0) -> float:
    return KAPPA * (int(utility) - EloProb(player_a, player_b)) if probability == 0 else KAPPA * (int(utility) - probability)

# Elo updating formula
def Update(player_a: Player, player_b: Player, utility: bool):
    prob = EloProb(player_a, player_b)
    delta = DeltaRating(player_a, player_b, utility, prob)
    return Player(player_a.rating + delta, player_a.hidden), Player(player_b.rating - delta, player_b.hidden)

# Returns the strengh score of a player
def GetStr(num: float)->float:
    return exp(num / SCALAR)

# Elo probability formula
def EloProb(player_a: Player, player_b: Player, is_hidden:bool=False)->float:
    if is_hidden:
        return round(1 / (1 + exp((player_b.TrueERating(True) - player_a.TrueERating(True)) / SCALAR)), 2)
    return round(1 / (1 + exp((player_b.TrueERating() - player_a.TrueERating()) / SCALAR)), 2)

# Btm probability formula
def BTMProb(player_a: Player, player_b: Player, is_hidden:bool=False)->float:
    a = GetStr(player_a.hidden) if is_hidden else GetStr(player_a.rating)
    b = GetStr(player_b.hidden) if is_hidden else GetStr(player_b.rating)
    num = round(a/(a + b), 2)
    return num

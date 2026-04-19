from math import sqrt, exp, log as ln
from scipy.stats import norm
from Models.PrevModels import EloProb, EstProb, DeltaRating, Damp, GetStr
from Utils.Player import Player



# calculate the new cv based on the third formula and clamping its minimum to 0.15
def NewCv(_cv: float, _mu: float, utility: int, probability: float) -> float:
    return max(0.15, _cv + (ETA * Damp(abs(utility - probability), utility) - GAMMA * _cv))

# updating player's delta and cvs based on their match result
def Update(player_a: Player, player_b: Player, utility: bool):
    prob = EstProb(player_a, player_b)
    delta = DeltaRating(player_a, player_b, utility, prob)
    cvs = [NewCv(player_a.cv, player_a.mu, utility, prob), NewCv(player_b.cv, player_b.mu, not utility, 1 - prob)]
    return (Player(player_a.rating + delta, player_a.hidden, cvs[0]),
            Player(player_b.rating - delta, player_b.hidden, cvs[1]))





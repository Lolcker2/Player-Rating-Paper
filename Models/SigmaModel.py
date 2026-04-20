from math import sqrt, exp, log as ln
from scipy.stats import norm
from Utils.Player import Player
from Models.PrevModels import EloProb, EstProb, DeltaRating, Damp, GetStr


# calculate the new sigma based on the third formula
def NewSigma(sigma: float, utility: int, probability: float) -> float:
    return sigma + (ETA * Damp(abs(utility - probability), utility) - GAMMA * sigma)

# updating player's delta and sigmas based on their match result
def Update(player_a: Player, player_b: Player, utility: bool):
    probability= EstProb(player_a, player_b, PlayerInitMode.SIGMA)
    delta = DeltaRating(player_a, player_b, utility, probability)
    sigmas = [NewSigma(player_a.sigma, utility, probability), NewSigma(player_b.sigma, not utility, 1 - probability)]
    return (Player(player_a.rating + delta, player_a.hidden, sigmas[0]),
            Player(player_b.rating - delta, player_b.hidden, sigmas[1]))



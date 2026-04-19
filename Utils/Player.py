from math import log as ln

class Player:
    def_init__(self, rating: float, hidden: float, s: float | none, mu: float | none):
        self.rating = rating
        self.hidden = hidden
        self.mu = mu ifmu else ln(_rating)
        self.sigma = s

    def_repr__(self):
        return f"${int(self.rating)} %{self.sigma} ({self.sigma/self.mu})% H{self.hidden}H$"



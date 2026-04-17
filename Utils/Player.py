class Player:
    def __init__(self, _rating: float, _hidden: float, _s: float = 0.0, _mu:float = 0.0):
        self.rating = _rating
        self.hidden = _hidden

        if _s:
            self.mu = ln(_rating) if _mu == 0.0 else _mu
            self.sigma = _s

    def __repr__(self):
        return f"${int(self.rating)} %{self.sigma} ({self.sigma/self.mu})% H{self.hidden}H$"



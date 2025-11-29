class State:
    def __init__(self, valores):
        self.valores = valores

    def __eq__(self, other):
        return self.valores == other.valores

    def __hash__(self):
        return hash(tuple(self.valores))

    def __repr__(self):
        return f"State({self.valores})"

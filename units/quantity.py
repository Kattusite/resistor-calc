
class Quantity():
    """A concrete measurement in given units.

    e.g. 50m, 100sec, 100kW
    """

    def __init__(self, qty, unit):
        self.qty = qty
        self.unit = unit

    def __str__(self):
        return self.unit.format(self.qty)

    def __repr__(self):
        return f"Quantity({qty}, {self.unit.name})"

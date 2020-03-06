from .unit import Unit
from .const import unitNames

class Units():
    """A collection of common units as a collection of Unit objects"""
    pass

# Dynamically create units for all units defined in const.py, as if we ran:
# Units.newtons = Unit("N")
# Units.volts   = Unit("V")
# Units.amps    = Unit("A")
# ...
for abbr, name in unitNames.items():
    setattr(Units, name.lower(), Unit(abbr))

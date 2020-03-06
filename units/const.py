# TODO: Some units can't be negative (ohms, seconds, etc.)
# should I explicitly prevent negative numbers?
# I think no -- maybe we'd like to compute an offset (e.g. R1 - R2) and
# negative numbers would be convenient.
# It should probably be caller's job to check for negativity if it matters to
# them (i.e. in Resistor)

unitNames = {
    "Ω": "Ohms",
    "A": "Amps",
    "V": "Volts",
    "W": "Watts",
    "m": "Meters",
    "s": "Seconds",
    "N": "Newtons",
}

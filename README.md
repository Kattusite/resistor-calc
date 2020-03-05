# resistor-calc
 Useful operations on electrical resistors

## Testing

To run the preliminary unit tests, run:

```bash
python -m resistor
python -m toolkit
python resistor/colors.py
```

## Quickstart

```python
from resistor import Resistor

a = Resistor(100) # a 100 ohm resistor
b = Resistor(10)  # a  10 ohm resistor

print(a.resistance(), b.resistance())

c = a + b # two resistors in series
d = a | b # two resistors in parallel

print(c.schematic(), d.schematic(), sep="\n\n")

e = a * 4    # 4 copies of a in series
f = a >> 4   # 4 copies of a in parallel
```

```python
from toolkit import Toolkit

# Define the primitive resistors available
resistances = [
  2200, 4700, 10_000, 22_000, 47_000, 
  100_000, 220_000, 470_000, 1_000_000
]
tk = Toolkit(resistances)

# find all combinations of 4 primitive resistors
tk.brute_force(4) 

r150_000 = tk.closest(150_000, n=4))[0]
print(r150_000.schematic())
```

## Code Structure

### Resistor
The `resistor` module defines the `Resistor` class, which represents an electrical resistor.
Electrical resistors can either be single primitive resistors, or composite resistors consisting of many such primitives (or even other composites). 

Resistors automatically track their current equivalent resistance and can be combined with other resistors in parallel or series. 

Resistors can print out a circuit schematic of their internal structure, a summary of their properties, and a 4- or 5-band schematic of the resistor's color bands (requires ANSI support).

### Toolkit
The `toolkit` module defines the `Toolkit` class, which represents a toolkit of primitive resistors, which can be combined to create resistors of an arbitrary equivalent resistance. 

The class defines a number of methods for finding the closest that the provided resistors can get to a target equivalent resistance, in the smallest number of resistors. 

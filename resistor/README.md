# resistor

The `resistor` module represents an electrical resistor in the `Resistor` class.
These resistors can be either _primitive_ resistors (a single electrical component)
or _composite_ resistors, composed of several other resistors (either primitive or composite)
connected together in series or in parallel, or any nested combination of the two.

## API

<!-- TODO: Describe API once it is finalized.

Proposed API:

  General TODOs:
  * Standardize camelCase vs snake_case
  * Decide on a naming convention for string observers that makes it clear
    they return strings without being overly verbose
    - note difference btwn 'to' and 'as': https://softwareengineering.stackexchange.com/questions/352157/whats-the-difference-between-to-and-as-method-name-prefixes
    - perhaps asAlgebraic, asSchematic, asColorCode
    - perhaps algebraicStr, schematicStr, colorCodeStr
    - perhaps algebraicString, ...
  * Make Resistor immutable
  * Electrical Observers should allow for units to be specified,
    or provide some way to convert/format units (e.g. string functions for units)
    - in fact, maybe just have a class for SI units like:
    ```
      watt = SI("W")
      watt.string(0.001) == "1mW"
      watt.string(1000)  == "1kW" (or "1KW") (I prefer small k)
    ```

  ## Creators (Operations)
  r.series(s):    Return new composite resistor of r in series with s
  r.__add__(s):

  r.__mult__(n):  Return new composite resistor of n copies of r in series
  r.__rmult__(n):

  r.parallel(s):  Return new composite resistor of r in parallel with s
  r.__or__(s):

  r.__rshift__(n): Return new composite resistor of n copies of r in parallel
  r.__rrshift__(n):

  r.toPrimitive():  Return a new primitive resistor with equal resistance.
  r.flatten()
   -- unsure about name - toPrimitive, flatten, both, neither?
   -- prefer toPrimitive right now b/c it is clear + unambiguous
   -- (what is being 'flattened?')

  r.clamp():       Return a new resistor with r's top 3 sigfigs of resistance
   -- e.g. 48_305.262 ==> 48_300
   -- unsure about name (clamp seems to imply mutation -- 'clamped'?)

  r.__trunc__():    Unsure - likely variants of clamp() respecting the semantics of ceil,floor,etc
  r.__round__():
  r.__ceil__():
  r.__floor__():

  r.__invert__():   Return a new composite resistor, swapping all series/parallel connections
    -- Unsure about this - it seems totally impractical

  # Observers (Comparison)
  r.__gt__(s)     Return True if r.ohms() > s.ohms()
  r.__lt__(s)     Return True if r.ohms() < s.ohms()
  r.__ge__(s)     Return True if r.ohms() >= s.ohms()
  r.__le__(s)     Return True if r.ohms() <= s.ohms()
  r.__eq__(s)     Return True if r.ohms() == s.ohms()
    -- Not at all sure about this one.
    -- Intuitively, should be equal if have all same primitives in the same
       (or equivalent) arrangement.
    -- But must make sure adding a more restrictive definition won't break
       sorting order or anything in Toolkit
  r.__hash__()   Return a hash of r
    -- Should include hashes of parents.

  # Observers (Boolean)
  r.isPrimitive(): Return True if r is a primitive resistor

  # Observers (Numerical)
  r.ohms():        Return the number of ohms of equivalent resistance
  r.depth():       Return the number of resistors on the longest internal path
  r.breadth():     Return the number of resistors in the widest parallel branch
  r.tolerance():   Return the tolerance, in percentage points
  r.minOhms():     Return the lowest tolerable number of ohms.
  r.maxOhms():     Return the highest tolerable number of ohms.
  r.ohmsRange():   Return (r.minOhms(), r.maxOhms())
  r.numPrimitives(): Return the number of internal primitive resistors


  # Observers (Electrical)
  r.current(V):   Return the current passing through r under voltage V
  r.voltage(I):   Return the voltage drop over r given a current I
  r.power(I):     Return the power dissipated by r under a current I
    -- what about r.power(V)?
  r.energy(I,t):  Return the heat produced by r under a current I for a time t

  r.resistivity(l,s): Return the resistivity of a given length/cross-section
  r.length(rho,s):    Return the length of a given resistivity/cross-section
    -- unsure about name - ambiguous with __len__
  r.crossSection(rho,l): Return the cross-section of a given resistivity and length

  r.wheatstone(r1,r2,r3):
    -- unsure exactly what a user would want it to compute

  # Observers (String)
  r.resistance():  Return a succinct string showing the equivalent resistance
  r.schematic():   Return a string showing a circuit diagram of internal resistors
  r.algebraic():   Return a string showing internal resistors in algebraic notation
  r.summary():     Return a succinct string summarizing properties
  r.primitive(): <(?) Return a string showing r as a primitive circuit component>
    -- unsure about name and proposed function
  r.colorCode():   Return a string textually representing the resistor's color code
    -- accept an optional argument to specify the format
    -- (1ascii, 2ascii, 3ascii, numbers, 2bitColor, 8bitColor, 24bitColor)
    -- (R/G/B , Rd/Gr , red/grn,  470e3,   0-15   ,   0-255  ,  0x123456 )
    -- accept another optional argument to specify whether to display just the
       color code, or the color code and graphical resistor body

  r.__str__():      <Unsure what this should return>
  r.__repr__():     <Unsure - likely some variant of <Resistor (100Ω) 9n:4d:5b>
    -- similar to summary()

  # Observers (Other)
  r.components():  Return a list of the internal primitive resistors
  r.structure():   Return a logical representation of r's internal structure
    -- Not sure about this one
    -- Do we want to allow callers to inspect the inner hierarchy of a Resistor?
    -- Hard to imagine a use case for this, but might help for extensibility
    -- Also, no way to inspect this unless provided explicitly, so if we exclude
       this function we'd better be sure the API provides everything a caller
       would ever need (unlikely we'll catch everything)
    -- No real harm in exposing this if we make sure internal structure is well
       designed








 -->

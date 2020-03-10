import math

##############################################################################
#                         Helper Functions
##############################################################################

def isInteger(x, tol=0.0001):
    """Returns true if the fractional part of an integer is less than a tolerance"""
    diff = x - round(x)
    return abs(diff) < tol

def magnitude(x):
    """Return the order of magnitude of x, as both an exponent and a power of 10"""
    e = math.floor(math.log10(x))
    return (e, 10 ** e)

def truncate(x, sigfigs=3):
    """Truncate x to the given number of sigfigs."""
    if x == 0:
        return 0

    exp, mag = magnitude(x)

    # Bring x to range [1, 10)
    x /= mag

    # Shift left by `sigfigs` digits
    scale = 10 ** (sigfigs-1)
    x *= scale

    # Truncate all trailing digits to the right.
    x = round(x)

    # Shift right by `sigfigs` digits
    x /= scale

    # Restore x to original range
    x *= mag

    # Fix precision errors
    # exp+1 of the sigfigs are integers. drop the fractional part
    if exp >= 0:
        x = round(x, ndigits=sigfigs-(exp+1))

    return x

class Property():
    """A particular physical property that can be measured.

    Properties can be either fundamental or derived.
    e.g. distance, time, force, energy, resistance, charge
    """

    TIME = "time"
    DISTANCE = "distance"
    # and so on...

    # TODO: Provide methods for composing derived properties
    # (ie. DISTANCE / TIME ==> VELOCITY)

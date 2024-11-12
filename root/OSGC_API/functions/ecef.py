import math
from decimal import Decimal, getcontext
from flask import abort
# set the precision to 30 decimal places
# using decimal for the precision
getcontext().prec = 30

# these are for the grs80 ellipsoid
a = Decimal('6378137.0')
flattening = Decimal('1') / Decimal('298.257222101')

e = Decimal(2 * flattening) - Decimal(flattening ** 2)

def latlon_to_ecef(lat, lon, alt=0):
    try:
        phi = Decimal(math.radians(float(lat)))
        lamb = Decimal(math.radians(float(lon)))
        h = Decimal(float(alt))
    except TypeError:
        abort(404, f"failed conversion of data types in ECEF conversion")

    N = a / Decimal(math.sqrt(1 - e**2 * Decimal(math.sin(phi))**2))

    X = (N + h) * Decimal(math.cos(phi)) * Decimal(math.cos(lamb))
    Y = (N + h) * Decimal(math.cos(phi)) * Decimal(math.sin(lamb))
    Z = ((1 - e**2) * N + h) * Decimal(math.sin(phi))

    return X, Y, Z

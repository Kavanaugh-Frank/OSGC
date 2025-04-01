import math
from decimal import Decimal, getcontext
from flask import abort


# set the precision to 30 decimal places
# using decimal for the precision
getcontext().prec = 30

# https://epsg.io/transform#s_srs=4326&t_srs=4978&x=39.9000000&y=-82.8800000

def latlon_to_ecef(lat, lon, alt=0):
    """
    Converts latitude, longitude, and altitude to Earth-Centered, Earth-Fixed (ECEF) coordinates.

    Parameters:
    lat (float or str): Latitude in degrees.
    lon (float or str): Longitude in degrees.
    alt (float or str, optional): Altitude in meters. Defaults to 0.

    Returns:
    tuple: A tuple containing the ECEF coordinates (X, Y, Z) in meters.

    Raises:
    TypeError: If there is a failure in converting the input data types.
    """

    # these are for the grs80 ellipsoid
    a = Decimal('6378137.0')
    b = Decimal('6356752.314140347')
    flattening = Decimal('1') / Decimal('298.257222100882711243')

    e = Decimal(2 * flattening) - Decimal(flattening ** 2)

    try:
        phi = Decimal(math.radians(float(lat)))
        lamb = Decimal(math.radians(float(lon)))
        h = Decimal(float(alt))
    except TypeError:
        abort(404, f"failed conversion of data types in ECEF conversion")

    sin_phi = Decimal(math.sin(phi))
    cos_phi = Decimal(math.cos(phi))
    cos_lamb = Decimal(math.cos(lamb))
    sin_lamb = Decimal(math.sin(lamb))

    N = a / Decimal(math.sqrt(1 - (e**2 * sin_phi**2)))

    X = (N + h) * cos_phi * cos_lamb
    Y = (N + h) * cos_phi * sin_lamb
    Z = ((1 - e**2) * N + h) * sin_phi

    return X, Y, Z

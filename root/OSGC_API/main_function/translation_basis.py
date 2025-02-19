import numpy as np
from decimal import Decimal
import pandas as pd
from helpers.ecef import latlon_to_ecef


# convert to the local tangent plane
# convert to ECEF first
# then worry about the offset
# the offset will subtracted to the X-Axis of the local tangent plane
def translation_basis(data, offset, gs_lat, gs_lon, gs_alt):
    """
    Transforms the given data from geodetic coordinates to a local tangent plane coordinate system
    based on a specified Glide Slope (GS) location and offset.

    Args:
        data (pd.DataFrame): A DataFrame containing the coordinates to be transformed.
        offset (float): The offset to be applied to the X-coordinate.
        gs_lat (float): Latitude of the Glide Slope (GS) in degrees.
        gs_lon (float): Longitude of the Glide Slope (GS) in degrees.
        gs_alt (float): Altitude of the Glide Slope (GS) in meters.

    Returns:
        str: The transformed data as a JSON string with orientation "values".
    """
    # finding Glide Slope (GS) in ECEF coordinates
    gs_x, gs_y, gs_z = latlon_to_ecef(gs_lat, gs_lon, gs_alt)

    # creating the Z-vector, which is GS - Origin, and normalizing it
    z_vector = np.array([gs_x, gs_y, gs_z])
    z_vector /= np.linalg.norm(z_vector)

    # creating the vector that represents the north pole, for finding the x vector
    north_x, north_y, north_z = latlon_to_ecef(90, 0, 0)

    # this vector is the North Pole - GS, and normalizing it
    north_vector = np.array([north_x - gs_x, north_y - gs_y, north_z - gs_z])

    # x_vector is the cross product of the north_vector and z_vector, and normalizing it
    x_vector = np.cross(north_vector, z_vector)
    x_vector /= np.linalg.norm(x_vector)

    # y_vector is the cross product of z_vector and x_vector, and normalizing it
    y_vector = np.cross(z_vector, x_vector)
    y_vector /= np.linalg.norm(y_vector)

    # construct the translation matrix
    translation_matrix = np.array([x_vector, y_vector, z_vector])

    # dot producting the translation matrix with the data
    data = data.applymap(lambda x: np.dot(translation_matrix, x))

    # Applying the offset to the X - Coordinate of each point
    data = data.applymap(lambda x: np.array([x[0] - Decimal(offset), x[1], x[2]]))

    # Return the data as a JSON string
    # return data.to_json(orient="values")
    return data


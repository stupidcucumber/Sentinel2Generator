import numpy as np

def convert_to_radians(geo_coordinate: float):
    '''
        This function can convert Longtitude and Latitude coordinates into radians.
    '''
    return geo_coordinate * np.pi / 180.0 


def convert_to_degrees(radian_coordinate: float):
    '''
        This function can convert degree coordinate into Geographical in range [1, 89].
    '''
    return radian_coordinate * 180.0 / np.pi


def get_earth_R_by_latitude(latitude: float):
    '''
        Accepts latitude in radians and returns desired radius of Earth.
    '''

    a = 6378
    e = 0.0818

    R = a * np.sqrt((1 - (2 * np.power(e, 2) - np.power(e, 4)) * np.power(np.sin(latitude), 2)) / (1 - e * e * np.sin(latitude) * np.sin(latitude)))

    return R


def get_box(center: tuple, radius: float):
    '''
        Function accepts center as (longtitude, latitude), radius in meters and angle in Celcius degrees.
        radius in kilometers.

        To see proper calculations for this function visit main README.md file.
    '''
    radian_center = convert_to_radians(center[0]), convert_to_radians(center[1])
    EARTH_RADIUS = get_earth_R_by_latitude(radian_center[1])

    min_max_latitude = []
    min_max_longtitude = []

    # Let's find min/max Latitude
    r = radius / EARTH_RADIUS
    min_max_latitude.extend([radian_center[1] - r, radian_center[1] + r])

    # Let's calculate min/max Longtitude
    delta_long = np.arcsin(np.sin(r) / np.cos(radian_center[1]))
    min_max_longtitude.extend([radian_center[0] - delta_long, radian_center[0] + delta_long])

    _start_point = [convert_to_degrees(min_max_longtitude[0]), convert_to_degrees(min_max_latitude[0])]
    _end_point = [convert_to_degrees(min_max_longtitude[1]), convert_to_degrees(min_max_latitude[1])]

    return [*_start_point, *_end_point]

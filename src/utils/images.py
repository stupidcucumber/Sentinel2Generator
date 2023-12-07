from . import coordinates
from ..core import grid
from sentinelhub import SHConfig
from ast import literal_eval


def extract_coordinates(line: str, radius: float=10) -> list[float,]:
    coords = literal_eval(line)

    if len(coords) == 2:
        coords = coordinates.get_box(radius=radius, center=coords)
    
    return coords


def instantiate_satellite_images(data_filename: str, data_config: dict, auth_config: dict) -> list[grid.SatelliteImage]:
    print('Instantiating satellite images...')
    with open(data_filename) as fdata:
        data = fdata.readlines()

    region_coordinates = []
    for line in data:
        coords = extract_coordinates(line, data_config['radius'])
        region_coordinates.append(coords)

    auth_config = SHConfig(
        instance_id = auth_config['instance_id'],
        sh_client_id = auth_config['client_id'],
        sh_client_secret = auth_config['client_secret'],
        sh_base_url = 'https://services.sentinel-hub.com',
        sh_token_url = 'https://services.sentinel-hub.com' + '/oauth/token'
    )

    satellite_images = []
    for coord in region_coordinates:
        # For each tuple of coordinates
        for interval in data_config['dates']:
            # For each time interval

            image = grid.SatelliteImage(
                tile_size=data_config['tile-size'],
                tile_resolution=data_config['tile-resolution'],
                coords=coord,
                time_interval=interval,
                config=auth_config
            )

            satellite_images.append(image)
        
    print('Instantiation has ended!')

    return satellite_images
from concurrent import futures
import grid
import argparse
from ast import literal_eval
import yaml, os, datetime
from sentinelhub import SHConfig


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--coordinates', type=literal_eval, required=True,
                        help='Coordinates of the region from which to take image.')
    parser.add_argument('-w', '--workers', type=int, default=4,
                        help='Default number of workers (threads).')
    parser.add_argument('-ts', '--tile-size', type=literal_eval, default=(2500, 2500),
                        help='Size in pixels of the tile.')
    parser.add_argument('-tr', '--tile-resolution', type=int, default=1,
                        help='Tile resolution. By default is 1, which means 1 meter is 1 pixel.')
    parser.add_argument('--start-date', type=str, required=True,
                        help='Start from which to take the photo in format: YYYY-MM-DD.')
    parser.add_argument('--end-date', type=str, required=True,
                        help='End date from which to take the photo in format: YYYY-MM-DD.')
    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Path to the configuration file with auth information.')
    parser.add_argument('-o', '--output', type=str, default='output',
                        help='The name of the folder where to save image.')
    
    return parser.parse_args()


class Downloader:
    def __init__(self, max_workers: int = 4, save_tiles: bool=True, config= None):
        self.workers = max_workers
        self.save_tiles = save_tiles

    def download(self, satellite_images: list[grid.SatelliteImage]):
        for image in satellite_images:
            # Iterates over the batch of SatelliteImage objects
            with futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                # Starts downloading images in parallel
                for row_index in range(image.size[0]):
                    for column_index in range(image.size[1]):
                        # Downloads cell
                        executor.submit(image.download_cell, row=row_index, column=column_index)


if __name__ == '__main__':
    args = parse_arguments()
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    with open(args.config) as config:
        bconfig = config.read()

    # instantiating images
    images = []
    auth = yaml.load(bconfig, yaml.Loader)['authorization']
    
    config = SHConfig(
        instance_id = auth['instance_id'],
        sh_client_id = auth['client_id'],
        sh_client_secret = auth['client_secret'],
        sh_base_url = 'https://services.sentinel-hub.com',
        sh_token_url = 'https://services.sentinel-hub.com' + '/oauth/token'
    )

    for coordinate in args.coordinates:
        image = grid.SatelliteImage(
            tile_size=args.tile_size,
            tile_resolution=args.tile_resolution,
            coords=coordinate,
            time_interval=(args.start_date, args.end_date),
            config=config
        )

        images.append(image)

    # Downloading images
    for image in images:
        with futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            size = image.size
            print('Start downloading image: ', image.coords)
            future_results = []
            for row_index in range(size[0]):
                for column_index in range(size[1]):
                    result = executor.submit(image.download_cell, row=row_index, column=column_index)
                    future_results.append(result)

            print('Waiting...')
            futures.wait(future_results)
            print('Images has been downloaded!')

    print('Start saving images...')
    for image in images:
        image_name = datetime.datetime.now().strftime('%d_%s.png')
        path = os.path.join(args.output, image_name)
        print('Saving image: ', image_name)
        image.save_tiles(folder=args.output)
        image.save(name=image_name)

    print('Done.') 
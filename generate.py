import argparse
import datetime
import os, yaml
from src import core
from src.utils import images


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Specify your configuration file, that contains info about user and where to store all data.')
    parser.add_argument('--coordinates', type=str, required=True,
                        help='This is the path to the text file with coordinates on each line. If there is only two values on the line ' + \
                            'than this is considered to be center coordinate of to be geenrated box (default radius = 10 km, taken from the' + \
                                'config file).')
    parser.add_argument('--output', type=str, default=datetime.datetime.now().strftime('%D_%s'),
                        help='Specify the folder where to store all data. If folder does not exist it will be created.')
    
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    
    if not os.path.exists(args.output):
        os.mkdir(args.output)

    with open(args.config) as config:
        _fconfig = config.read()

    satellite_config = yaml.load(_fconfig, yaml.Loader)
    auth_config = satellite_config['authorization']
    data_config = satellite_config['data']

    downloader = core.downloader.Downloader(
        data_config['workers']
    )

    satellite_images = images.instantiate_satellite_images(args.coordinates,
                                                           data_config=data_config,
                                                           auth_config=auth_config)
    
    print('Start to download images from the internet...')
    downloader.download(satellite_images=satellite_images)
    print('Download has finished!')

    print('Saving images to the folder: ', args.output)
    for satellite_image in satellite_images:
        folder_coords = str(satellite_image.coords)
        path_folder_coords = os.path.join(args.output, folder_coords)
        if not os.path.exists(path_folder_coords):
            os.mkdir(path_folder_coords)

        
        time_interval = str(satellite_image.time_interval)
        path_root_folder = os.path.join(path_folder_coords, time_interval) # Folder corresponding to the chosen satellite coordinates and time interval
        if not os.path.exists(path_root_folder):
            os.mkdir(path_root_folder)

        main_image_path = os.path.join(path_root_folder, 'satellite_image.png')
        print('Saving to the: ', path_root_folder)
        satellite_image.save_tiles(folder=path_root_folder)
        satellite_image.save(name=main_image_path)

    print('Images have been saved!')
    print('Done.')
    



     
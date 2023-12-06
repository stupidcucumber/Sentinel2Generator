import argparse
import datetime
import os


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', type=str, default='config.yaml',
                        help='Specify your configuration file, that contains info about user and where to store all data.')
    parser.add_argument('--output', type=str, default=datetime.datetime.now().strftime('%D_%s'),
                        help='Specify the folder where to store all data. If folder does not exist it will be created.')
    
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()


    if not os.path.exists(args.output):
        os.mkdir(args.output)

     
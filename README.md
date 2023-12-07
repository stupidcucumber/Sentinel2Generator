# About
This repository provides similar to the BatchProcessing API, which is available only for enterprise users on Sentinel Hub. It can be useful for researchers in field of Computer Vision, who don't want to put much effort into exploring geographical aspect of extracting satellite imaginery.

![Image of the satellite](./misc/satellite.jpg)

I am not neither guranteeing the same speed nor the same quality, but it can be sufficient for small projects or to generate dataset to test your models on Satellite Keypoints Matching, Satellite Image Classification, Satellite Object Detection.

# Implementation
The implementation is quite straightforward. Images are being divided into "tiles", which are then being requested from the Sentinel-Hub. After all requests are processed service collects tile into one image to save it. In the end we have high-resolution data with specified resolution and size.

## Usage
Before using this repository I reccomend initiating new environment via virtualenv, or using conda to do so. Then run the following command:
```
python -m pip install -r requirements.txt
```
After succesfull installation of all required packeges you can start setting up configuration file. In the root of this repository resides file named 'example_config.yaml' with two parts: 'authorization' and 'data'. 'authoriation' part is unique for each user and info to fill in can be found on your profile page on SentinelHub.

More interesting part of the config file is 'data'. There you can adjust the following settings:
- `workers` how many threads there will be to download images.
- `radius` this application downloads images from Sentinel2. But it's not convenient to always find exact coordinates. Considering that I implemented special creation of this bbox coordinates from the center you mentioned (Long, Lat). Therefore application will return the square image with side radius * 2 and the center of image will align with center you wrote in 'coordinates.txt'.
- `tile-size` size of the tile (Satellite Image is being divided into subimages), or the subimage.
- `tile-resolution` resolution of the subimage.
- `dates` from which time interval to take images.

For the usage you need a special text file named "coordinates.txt". There on each line you need to put either 2-value coordinate or 4-value coordinate. If 2-value coordinate was mentioned, program will take care of extracting region of about 20-by-20 km region (this is defaul, but can be changed in the config.yaml file under 'data' settings).

After creating 'coordinates.txt' you can start downloading images:
```
python generate.py --config example_config.yaml --coordinates coordinates.txt --output data
```
After application will end execution, you will see directory data at the root of this repository. There will reside folders with corresponding names of the square coordinates. In each such folder will be folders corresponding to the time-intervals of images from the corresponding square coordinates. Example:
```
data
├── [50.35491697962805, 30.435564291321768, 50.56367102037195, 30.615385708678232]
│   ├── [datetime.date(2023, 2, 10), datetime.date(2023, 2, 15)]
│   └── [datetime.date(2023, 5, 10), datetime.date(2023, 5, 15)]
└── [9.068993667787991, 55.88067983970848, 9.390786332212008, 56.06076016029154]
    ├── [datetime.date(2023, 2, 10), datetime.date(2023, 2, 15)]
    └── [datetime.date(2023, 5, 10), datetime.date(2023, 5, 15)]
```
Each leaf directory contains tiles with format ('x', '_', 'y', '.png') and the main image with name 'satellite_image.png'.

## Classes
Application has the folowing classes:

- `ImageCell` class intended to represent "cell" in our image grid. Every object essentially contains requests and after processing request it will contain our tile.
- `SatelliteImage` class contains all the tiles and provides high-level interface to download image, save whole image and save only tiles.
- `Downloader` class intended to download provided SatelliteImage. Its purpose is to incapsulate download of images.

# Example

This example was acquired by using the following command:

```
python src/core/downloader.py -c "[[30.205536, 50.372620, 30.480881, 50.561498]]" --start-date "2021-10-05" --end-date "2021-10-10" --tile-size "(2000, 2000)" --tile-resolution 2
```

After that we have the following picture 10000x10000:

![Example image](./misc/example.png)
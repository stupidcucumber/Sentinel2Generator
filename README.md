# About
This repository provides similar to the BatchProcessing API, which is available only for enterprise users on Sentinel Hub. It can be useful for researchers in field of Computer Vision, who don't want to put much effort into exploring geographical aspect of extracting satellite imaginery.

![Image of the satellite](./misc/satellite.jpg)

I am not neither guranteeing the same speed nor the same quality, but it can be sufficient for small projects or to generate dataset to test your models on Satellite Keypoints Matching, Satellite Image Classification, Satellite Object Detection.

# Implementation
The implementation is quite straightforward. Images are being divided into "tiles", which are then being requested from the Sentinel-Hub. After all requests are processed service collects tile into one image to save it. In the end we have high-resolution data with specified resolution and size.

## Usage


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
# About
This repository provides similar to the BatchProcessing API, which is available only for enterprise users on Sentinel Hub. I am not neither guranteeing the same speed nor the same quality, but it can be sufficient for small projects or to generate dataset to test your models on Satellite Keypoints Matching, Satellite Image Classification, Satellite Object Detection.

# Example

This example was acquired by using the following command:

```
python src/core/downloader.py -c "[[30.205536, 50.372620, 30.480881, 50.561498]]" --start-date "2021-10-05" --end-date "2021-10-10" --tile-size "(2000, 2000)" --tile-resolution 2
```

After that we have the following picture:
![Example image](./example.png)
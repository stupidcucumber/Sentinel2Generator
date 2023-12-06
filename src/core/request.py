from sentinelhub import SHConfig, SentinelHubRequest, DataCollection, MimeType, BBox, CRS, bbox_to_dimensions


def generate_request(bbox: tuple, size, timestamp: str, auth_config: SHConfig, **kwargs):
    evalscript = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
    """
    request_true_color = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=timestamp,
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=bbox,
        size=size,
        config=auth_config,
    )

    return request_true_color
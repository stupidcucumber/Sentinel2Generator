import cv2, os
from sentinelhub import BBox, CRS, bbox_to_dimensions
import request


class ImageCell:
    '''
        This class is for the tile in the Satellite Image. It represents some part of the image.
    If postprocess is false, than image will not be standartized! 
    
    '''
    def __init__(self, request, size: tuple, postprocess: bool = True):
        self.request = request
        self.size = size
        self.postprocess = postprocess

    def save(self, name):
        pass

    def _set_image(self, image):
        self.image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.image = cv2.resize(self.image, dsize=self.size)

    def request_image(self):
        request = self.request.get_data()
        print('Request: ', request)
        image = request[0]
        if self.postprocess:
            self._set_image(image)
        else:
            self.image = image


class SatelliteImage:
    '''
        This class represents the whole image. It has the specified size at the time of the creation
    and the specified resolution.
        Restrictions:
        - The tile_size must be strictly divisor of size of the satellite image, otherwise trunction is
        applied, which means area will be shrinked.
    '''
    def __init__(self, tile_size: tuple, tile_resolution: float, coords: tuple, time_interval: tuple, config=None):
        self.tile_size = tile_size
        self.tile_resolution = tile_resolution
        self.coords = coords

        self.time_interval = time_interval
        self.grid = []

        self._create_grid(config=config)

    def _create_grid(self, config=None):
        '''
            Function creates grid of ImageCells with its own requests to SentinelHub. This dow not mean downloading images,
        but only assigning requests to the Cell.
        '''
        long_size = self.coords[2] - self.coords[0]
        lat_size = self.coords[3] - self.coords[1]

        bbox = BBox(self.coords, crs=CRS.WGS84)
        size = bbox_to_dimensions(bbox, resolution=self.tile_resolution)

        columns_number = int(size[0] / self.tile_size[0])
        rows_number = int(size[1] / self.tile_size[1])
        self.size = rows_number, columns_number
        self.bbox = bbox

        long_step = long_size / columns_number
        lat_step = lat_size / rows_number

        for row in range(rows_number):
            temp_row = []

            for column in range(columns_number):
                _start = self.coords[0] + column * long_step, self.coords[1] + row * lat_step
                _end = self.coords[0] + (column + 1) * long_step, self.coords[1] + (row + 1) * lat_step

                bbox = BBox([*_start, *_end], crs=CRS.WGS84)
                size = bbox_to_dimensions(bbox, resolution=self.tile_resolution)

                req = request.generate_request(
                    bbox=bbox, size=size,
                    timestamp=self.time_interval,
                    auth_config=config
                )
                
                cell = ImageCell(
                    request=req,
                    size=self.tile_size,
                    postprocess=True
                )

                temp_row.append(cell)

            self.grid.append(temp_row)

    def download_cell(self, row: int, column: int):
        '''
            Function downloads cell located at the position row, column.
        '''
        cell = self.grid[row][column]
        cell.request_image()

    def download(self):
        '''
            Function downloads the whole grid of cells. 
        '''
        for row in self.grid:
            for cell in row:
                cell.request_image()

    def save(self, name):
        '''
            Function concatenates all the tiles and saves them in the '.png' file with the given name.
        '''
        image = cv2.hconcat([cell.image for cell in self.grid[0]])

        for row in self.grid[1:]:
            _temp = cv2.hconcat([cell.image for cell in row])
            image = cv2.vconcat([_temp, image])

        cv2.imwrite(name, image)
            
    def load_tiles(self, path):
        pass

    def save_tiles(self, folder):
        '''
            Function saves tiles only with metadata about image, to recreate it.
        '''
        for row_index, row in enumerate(self.grid):
            for column_index, cell in enumerate(row):
                name = os.path.join(folder, '%d_%d.png' % (row_index, column_index))
                try:
                    cv2.imwrite(name, cell.image)
                except:
                    print('Warning: Image (row=%d, column=%d) is missing!' % (row_index, column_index))

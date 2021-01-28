import logging
import os
import zipfile

from configuration import configuration
from slugify import slugify

import library.util as util

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Cbr:
    def __init__(self, path):
        self.path_book = path;
        self.filename = util.get_name(os.path.basename(path));
        self.extension = util.get_extension(os.path.basename(path));

        self.title = self.filename;
        self.number_of_pages = 10;

        self.get_and_save_cover();

    def get_and_save_cover(self):
        with zipfile.ZipFile(self.path_book, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:
            images = [image for image in zip_file.namelist() if "." in image];

            extension = util.get_extension(os.path.basename(images[0]));
            self.path_cover = f"/{configuration['PATH_COVERS']}{slugify(self.filename)}{extension}";

            with open(self.path_cover[1::], "wb") as image:
                image.write(zip_file.read(images[0]));

    def get_page(self, page):
        with zipfile.ZipFile(self.path_book, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:
            images = [image for image in zip_file.namelist() if "." in image];

            extension = util.get_extension(os.path.basename(images[page]));
            name = f"{configuration['PATH_TEMP']}{slugify(self.filename)}-{page}{extension}";

            with open(name[1::], "wb") as image:
                image.write(zip_file.read(images[page]));

        return f"<img width='700px' src='{name}'>";

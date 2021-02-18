import logging
import os
import zipfile

from slugify import slugify

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Cbz:
    def __init__(self, id, filename, extension, path, size):
        self.id = id;
        self.filename = filename;
        self.extesion = extension;
        self.path = path;
        self.size = size;

        self.load();

    def load(self):
        self.title = self.filename;

        with zipfile.ZipFile(self.path, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:
            images = [image for image in zip_file.namelist() if "." in image];
            self.number_of_pages = len(images);

            extension = os.path.splitext(images[0])[1];
            self.cover = f"/static/covers/{slugify(self.filename)}{extension}";

            with open(self.cover[1::], "wb") as image:
                image.write(zip_file.read(images[0]));

    def get_page(self, page):
        with zipfile.ZipFile(self.path, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_file:
            images = [image for image in zip_file.namelist() if "." in image];

            extension = os.path.splitext(images[page])[1];
            name = f"/static/temp/{slugify(self.filename)}-{page}{extension}";

            with open(name[1::], "wb") as image:
                image.write(zip_file.read(images[page]));

        return f"<img class='img-fluid' loading='lazy' src='{name}'>";

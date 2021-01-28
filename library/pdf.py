import logging
import os

import fitz
from configuration import configuration
from slugify import slugify

import library.util as util

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Pdf:
    def __init__(self, path):
        self.path_book = path;
        self.filename = util.get_name(os.path.basename(path));
        self.extension = util.get_extension(os.path.basename(path));

        with fitz.open(self.path_book) as pdf_file:
            self.title = pdf_file.metadata["title"];
            self.number_of_pages = len(pdf_file);

        self.get_and_save_cover();

    def get_and_save_cover(self):
        self.path_cover = f"{configuration['PATH_COVERS']}{slugify(self.filename)}.png";

        with fitz.open(self.path_book) as pdf_file:
            page = pdf_file.loadPage(0);
            pix = page.getPixmap();
            pix.writeImage(self.path_cover);
            util.image_optimization(self.path_cover, True);

    def get_page(self, page):
        name = f"{configuration['PATH_TEMP']}{slugify(self.filename)}-{page}.png";

        if not os.path.exists(name[1::]):
            with fitz.open(self.path_book) as pdf_file:
                page = pdf_file.loadPage(page);
                pix = page.getPixmap();
                pix.pillowWrite(name[1::], optimize=True);
                util.image_optimization(name[1::]);

        return f"<img width='700px' src='{name}'>";

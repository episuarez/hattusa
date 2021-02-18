import logging
import os

import fitz
from PIL import Image, ImageEnhance
from slugify import slugify

from .book import Book

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Pdf(Book):

    def __init__(self, id, filename, extension, path, size):
        self.id = id;
        self.filename = filename;
        self.extesion = extension;
        self.path = path;
        self.size = size;

        self.load();

    def load(self):
        with fitz.open(self.path) as pdf_file:
            if "title" in pdf_file.metadata and pdf_file.metadata["title"] != "":
                self.title = str(pdf_file.metadata["title"]).encode("iso-8859-1").decode("utf-8");
            else:
                self.title = self.filename;

            self.number_of_pages = len(pdf_file);
            self.cover = f"static/covers/{slugify(self.filename)}.png";

            with fitz.open(self.path) as pdf_file:
                page = pdf_file.loadPage(0);
                pix = page.getPixmap();
                pix.writeImage(self.cover);

            img = Image.open(self.cover);
            img.resize((243, 300), Image.ANTIALIAS);
            img.save(self.cover, optimize=True, quality=80);

    def get_page(self, page):
        name = f"/static/temp/{slugify(self.filename)}-{page}.png";

        if not os.path.exists(name[1::]):
            with fitz.open(self.path) as pdf_file:
                page = pdf_file.loadPage(page);
                pix = page.getPixmap(matrix=fitz.Matrix(1.50, 1.50));
                pix.writeImage(name[1::]);

                img = Image.open(name[1::]);
                contrast = ImageEnhance.Contrast(img).enhance(2);
                contrast.save(name[1::]);

        return f"<img loading='lazy' src='{name}'>";

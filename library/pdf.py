import PyPDF2
import os
import logging

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Pdf:
    def __init__(self, path):
        self.path_book = path;
        self.filename = os.path.splitext(os.path.basename(path))[0];
        self.extension = os.path.splitext(os.path.basename(path))[1];

        with open(self.path_book, "rb") as pdf_file:
            pdf = PyPDF2.PdfFileReader(pdf_file);

            page = pdf.getPage(1);

            self.number_of_pages = pdf.getNumPages();

        self.get_and_save_cover();

    def get_and_save_cover(self):
        pass;

    def get_page(self, page):
        pass;

pdf = Pdf("books/aprendeml.pdf");

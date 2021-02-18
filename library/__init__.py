import logging
import os
import shutil

from slugify import slugify

from library.cbr import Cbr
from library.cbz import Cbz
from library.epub import Epub
from library.pdf import Pdf

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Library:
    def __init__(self):
        self.books = [];

        self._check_paths();
        self.load_books();

    def load_books(self):
        "Loading of book metadata"

        logging.info("Start of data loading of books");

        archives = [os.path.join(dp, a) for dp, dn, files in os.walk(self.pathBooks) for a in files];
        
        for book in archives:
            filename = os.path.splitext(os.path.basename(book))[0];
            extension = os.path.splitext(book)[1];
            path = os.path.dirname(os.path.realpath(book));
            size = str((os.path.getsize(book) / 1024) / 1024)[0:5];

            new_path = path + "/" + slugify(filename) + extension;
            os.rename(path + "/" + filename + extension, new_path);

            """
            if extension == ".epub":
                self.books.append(Epub(filename, extension, new_path));
            el"""
            if extension == ".pdf":
                self.books.append(Pdf(len(self.books), filename, extension, new_path, size));
            elif extension == ".cbz":
                self.books.append(Cbz(len(self.books), filename, extension, new_path, size));
            elif extension == ".cbr":
                self.books.append(Cbr(len(self.books), filename, extension, new_path, size));

        logging.info("End of data loading of books");

    def removes_covers(self):
        "Removes book covers"

        self._remove_all_files(self.pathCovers);

    def delete_cache(self):
        "Clear Cache"

        self._remove_all_files(self.pathTemp);

    def get_books(self):
        "Get the books in order"
        
        return sorted(self.books, key=lambda book: book.title);

    def get_page_book(self, id_book, page):
        "Get the page of a book"

        return self.books[id_book].get_page(page);

    def _check_paths(self):
        "Verification of the paths and that they are correct."

        self.pathBooks = os.getcwd() + "/books/";
        self.pathCovers = os.getcwd() + "/static/covers/";
        self.pathTemp = os.getcwd() + "/static/temp/";

        try:
            if not os.path.exists(self.pathBooks):
                os.mkdir(self.pathBooks);
            if not os.path.exists(self.pathCovers):
                os.mkdir(self.pathCovers);
            if not os.path.exists(self.pathTemp):
                os.mkdir(self.pathTemp);
        except Exception as error:
            logging.error(f"Cannot create the necessary paths for the operation of the application -> {error}");

    def _remove_all_files(self, directory):
        "Deletes all files in a directory"

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename);
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path);
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path);
            except Exception as error:
                logging.warning(f"Failed to delete -> {file_path}, {error}");


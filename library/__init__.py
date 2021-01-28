import logging
import os
import shutil

from configuration import configuration
from pony import orm

from library.epub import Epub
from library.pdf import Pdf
from library.cbz import Cbz
from library.cbr import Cbr

from .models.book import Book
from slugify import slugify
from .util import *

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Library:
    def __init__(self):
        self.pathBooks = os.getcwd() + configuration["PATH_BOOKS"];
        self.pathCovers = os.getcwd() + "/" + configuration["PATH_COVERS"];
        self.pathTemp = os.getcwd() + configuration["PATH_TEMP"];

        try:
            if not os.path.exists(self.pathBooks):
                os.mkdir(self.pathBooks);
            if not os.path.exists(self.pathCovers):
                os.mkdir(self.pathCovers);
            if not os.path.exists(self.pathTemp):
                os.mkdir(self.pathTemp);
        except Exception as error:
            logging.error(f"Cannot create the necessary paths for the operation of the application -> {error}");

        self.synchronization();

    def removes_covers(self):
        self._remove_all_files(self.pathCovers);

    def delete_cache(self):
        self._remove_all_files(self.pathTemp);

    @orm.db_session
    def synchronization(self):
        self.removes_covers();
        self.delete_cache();

        logging.info("Start of synchronization");
        books_files = [];

        for book in os.listdir(self.pathBooks):
            new_path = self.pathBooks + slugify(get_name(book)) + get_extension(book);

            if not os.path.exists(new_path):
                os.rename(self.pathBooks + book, new_path);

            logging.info(f"Book detected -> {book}");
            books_files.append(new_path);

        for book in self.get_books():
            if not book.path_book in books_files:
                logging.warning(f"Missing book -> {book.filename}");
                book = Book[book.id];
                book.remove_cover();
                book.delete();

        for book_name in books_files:
            if orm.count(book for book in Book if book.path_book == book_name) == 0:
                logging.info(f"Book added to the library -> {book_name}");
                self.add_book(book_name);

        logging.info("End of synchronization");

    @orm.db_session
    def add_book(self, name):
        extension = get_extension(name);
        
        if extension == ".epub":
            new_epub = Epub(name);
            try:
                new_book = Book(
                    title=new_epub.title,
                    path_book=new_epub.path_book,
                    path_cover=new_epub.path_cover,
                    filename=new_epub.filename,
                    extension=new_epub.extension,
                    number_of_pages=10
                );
            except Exception as error:
                logging.warning(f"Error when adding the new book -> {error}");
        elif extension == ".pdf":
            new_pdf = Pdf(name);
            try:
                new_book = Book(
                    title=new_pdf.title,
                    path_book=new_pdf.path_book,
                    path_cover=new_pdf.path_cover,
                    filename=new_pdf.filename,
                    extension=new_pdf.extension,
                    number_of_pages=new_pdf.number_of_pages
                );
            except Exception as error:
                logging.warning(f"Error when adding the new book -> {error}");
        elif extension == ".cbz":
            new_pdf = Cbz(name);
            try:
                new_book = Book(
                    title=new_pdf.title,
                    path_book=new_pdf.path_book,
                    path_cover=new_pdf.path_cover,
                    filename=new_pdf.filename,
                    extension=new_pdf.extension,
                    number_of_pages=new_pdf.number_of_pages
                );
            except Exception as error:
                logging.warning(f"Error when adding the new book -> {error}");
        elif extension == ".cbr":
            new_pdf = Cbr(name);
            try:
                new_book = Book(
                    title=new_pdf.title,
                    path_book=new_pdf.path_book,
                    path_cover=new_pdf.path_cover,
                    filename=new_pdf.filename,
                    extension=new_pdf.extension,
                    number_of_pages=new_pdf.number_of_pages
                );
            except Exception as error:
                logging.warning(f"Error when adding the new book -> {error}");

    @orm.db_session
    def get_books(self):
        return list(orm.select(book for book in Book).order_by(lambda: book.title));

    @orm.db_session
    def get_book_name(self, id_book):
        return list(orm.select(book.title for book in Book if book.id == id_book))[0];

    @orm.db_session
    def get_page_book(self, id_book, page):
        book = list(orm.select(book.path_book for book in Book if book.id == id_book))[0];

        extension = os.path.splitext(os.path.basename(book))[1];

        if extension == ".epub":
            return Epub(book).get_page(page);
        elif extension == ".pdf":
            return Pdf(book).get_page(page);
        elif extension == ".cbz":
            return Cbz(book).get_page(page);
        elif extension == ".cbr":
            return Cbr(book).get_page(page);

    def _remove_all_files(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename);
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path);
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path);
            except Exception as error:
                logging.warning(f"Failed to delete -> {file_path}, {error}");


import logging
import os

from configuration import configuration
from pony import orm

from library.epub import Epub

from .models.book import Book
from slugify import slugify
from .util import *

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="w");

class Library:
    def __init__(self):
        self.pathBooks = os.getcwd() + configuration["PATH_BOOKS"];
        self.pathCovers = os.getcwd() + "/" + configuration["PATH_COVERS"];

        try:
            if not os.path.exists(self.pathBooks):
                os.mkdir(self.pathBooks);
            if not os.path.exists(self.pathCovers):
                os.mkdir(self.pathCovers);
        except Exception as error:
            logging.error(f"Cannot create the necessary paths for the operation of the application -> {error}");

        self.sync_books();

    @orm.db_session
    def sync_books(self):
        logging.info("Start of synchronization");
        books_files = [];

        for book in os.listdir(self.pathBooks):
            new_path = self.pathBooks + slugify(get_name(book)) + get_extension(book);

            os.rename(self.pathBooks + book, new_path);

            logging.info(f"Book detected -> {book}");
            books_files.append(new_path);

        for book in self.get_books():
            if not book.path_book in books_files:
                logging.warning(f"Missing book -> {book.filename}");
                Book[book.id].delete();

        for book_name in books_files:
            if orm.count(book for book in Book if book.path_book == book_name) == 0:
                logging.info(f"Book added to the library -> {book_name}");
                self.add_book(book_name);

        logging.info("End of synchronization");

    @orm.db_session
    def add_book(self, name):
        _, extension = os.path.splitext(name);
        
        if extension == ".epub":
            new_epub = Epub(name);
            try:
                new_book = Book(
                    identifier=new_epub.identifier,
                    title=new_epub.title,
                    publisher=new_epub.publisher,
                    language=new_epub.language,
                    path_book=new_epub.path_book,
                    path_cover=new_epub.path_cover,
                    filename=new_epub.filename,
                    extension=new_epub.extension,
                    number_of_pages=10
                );
            except Exception as error:
                logging.warning(f"Error when adding the new book -> {error}");

    @orm.db_session
    def get_books(self):
        return list(orm.select(book for book in Book).order_by(lambda: book.title));

    @orm.db_session
    def get_page_book(self, id_book, page):
        book = list(orm.select(book.path_book for book in Book if book.id == id_book))[0];

        return Epub(book).get_page(page);


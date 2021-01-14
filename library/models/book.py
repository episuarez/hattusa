from database import db
from pony import orm
import os

class Book(db.Entity):
    identifier = orm.Required(orm.StrArray);
    title = orm.Required(str);
    publisher = orm.Required(str);
    language = orm.Required(str);
    path_book = orm.Required(str);
    path_cover = orm.Required(str);
    filename = orm.Required(str);
    extension = orm.Required(str);
    number_of_pages = orm.Required(int);

    @staticmethod
    def remove_cover():
        if os.path.exists(Book.path_cover):
            os.remove(Book.path_cover);

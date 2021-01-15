from database import db
from pony import orm
import os

class Book(db.Entity):
    identifier = orm.Required(orm.StrArray);
    title = orm.Required(str);
    creator = orm.Required(orm.StrArray);
    publisher = orm.Required(str);
    language = orm.Required(str);
    path_book = orm.Required(str);
    path_cover = orm.Required(str);
    filename = orm.Required(str);
    extension = orm.Required(str);
    number_of_pages = orm.Required(int);

    def remove_cover(self):
        if os.path.exists(self.path_cover):
            os.remove(self.path_cover);

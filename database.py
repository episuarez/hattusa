from pony import orm

db = orm.Database();
db.bind(provider='sqlite', filename='database.sqlite', create_db=True);

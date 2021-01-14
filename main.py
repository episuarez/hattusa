import threading

import webview
from flask import Flask, redirect, render_template, url_for

from configuration import configuration
from database import db
from library import Library
from library.epub import Epub

app = Flask(__name__);

db.generate_mapping(create_tables=True);

library = Library();

@app.route("/", defaults={"page": 1})
def index(page):
    return render_template("index.html", books=library.get_books());

@app.route("/sync", defaults={"page": 1})
def sync(page):
    library.sync_books();
    return redirect(url_for("index"));

@app.route("/viewer/<int:id_book>", defaults={"page": 1})
@app.route("/viewer/<int:id_book>/<int:page>")
def viewer(id_book, page):
    return render_template("viewer.html", id_book=id_book, page=page, content=library.get_page_book(id_book, page));

def launch_webserver():
    app.run(debug=configuration["DEBUG"]);

if configuration["MODE_DESKTOP"]:
    webserver = threading.Thread(target=launch_webserver, daemon=True);
    webserver.start();
    
    window = webview.create_window("Hattusa", "http://127.0.0.1:5000");
    webview.start(window);
else:
    launch_webserver();

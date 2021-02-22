from flask import Flask, redirect, render_template, request, url_for

from library import Library

app = Flask(__name__);

library = Library();

@app.after_request
def add_security_headers(response):
    response.headers['server'] = "Hattusa";

    response.headers['x-content-type-options'] = "nosniff";

    response.headers['Cache-Control'] = "no-cache";
    response.headers['Max-age'] = "0";

    return response

@app.route("/", defaults={"directory": ""})
@app.route("/<path:directory>")
def index(directory):
    path = directory;
    if "/" in path:
        path = f"/{path}";

    return render_template(
        "index.html",
        path=path,
        breadcrumb=library.get_breadcrumb(path),
        items=library.get_items(directory),
        dark_mode=request.cookies.get("dark_mode")
    );

@app.route("/synchronization")
def synchronization():
    library.synchronization();
    return redirect(url_for("index"));

@app.route("/removes_covers")
def removes_covers():
    library.removes_covers();
    return redirect(url_for("index"));

@app.route("/delete_cache")
def delete_cache():
    library.delete_cache();
    return redirect(url_for("index"));

@app.route("/viewer/<int:id_book>", defaults={"page": 1})
@app.route("/viewer/<int:id_book>/<int:page>")
def viewer(id_book, page):
    if id_book == None:
        return redirect(url_for("page_not_found"));

    return render_template(
        "viewer.html",
        id_book=id_book,
        title=library.books[id_book].title,
        page=page,
        content=library.get_page_book(id_book, page),
        dark_mode=request.cookies.get("dark_mode")
    );

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run();

from flask import Blueprint, render_template

log_book = Blueprint("log_book", __name__, url_prefix="/log-book")


@log_book.route("/new")
def new_log():
    return render_template("log_book/new.html")


@log_book.route("/")
def log_book_home():
    return render_template("log_book/index.html")

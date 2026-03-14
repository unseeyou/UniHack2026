from flask import Blueprint, render_template

log_book = Blueprint("log_book", __name__, url_prefix="log-book", template_folder="log_book")

@log_book.route("/new")
def new_log():
    return render_template("new.html", suburb="Chatswood", road_type="Quiet Street")
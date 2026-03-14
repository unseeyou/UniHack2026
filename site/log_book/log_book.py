from flask import Blueprint, render_template

log_book = Blueprint("log_book", __name__, url_prefix="/log-book")


@log_book.route("/new")
def new_log():
    return render_template(
        "log_book/new.html", suburb="Chatswood", road_type="Quiet Street"
    )

from flask import send_file, render_template

from constants import app
from database.base import db
from api.api import api
from celery_app import celery_init_app
from log_book.log_book import log_book


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manifest.json")
def serve_manifest():
    return send_file("manifest.json", mimetype="application/manifest+json")


@app.route("/sw.js")
def serve_sw():
    return send_file("static/js/sw.js", mimetype="application/javascript")


if __name__ == "__main__":
    app.register_blueprint(api)
    app.register_blueprint(log_book)
    db.init_app(app)
    celery_init_app(app)

    with app.app_context():
        db.create_all()

    app.run(
        debug=True,
        host="0.0.0.0",
    )  # ssl_context='adhoc')

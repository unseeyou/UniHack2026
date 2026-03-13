from constants import app
from database.base import db
from flask import send_file, render_template


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
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="localhost")

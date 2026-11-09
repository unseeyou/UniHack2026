from waitress import serve

from app import app, db, api, log_book

if __name__ == "__main__":
    app.register_blueprint(api)
    app.register_blueprint(log_book)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()
    print("serving app")
    serve(app, host="0.0.0.0", port=8080)  # pye change this later
    print("serving app")

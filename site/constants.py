from flask import Flask


class CustomApp(Flask):
    def __init__(self, *args, **kwargs):
        super(CustomApp, self).__init__(*args, **kwargs)
        self.logger.setLevel("DEBUG")
        self.logger.debug("initializing app")

        self.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/sqlite.db"

        self.config["CELERY"] = {
            "broker_url": "db+sqlite:///../database/sqlite.db",
            "backend_url": "db+sqlite:///../database/sqlite.db",
        }


app = CustomApp("app")

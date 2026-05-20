from flask import Flask
from zoneinfo import ZoneInfo


class CustomApp(Flask):
    def __init__(self, *args, **kwargs):
        super(CustomApp, self).__init__(*args, **kwargs)
        self.logger.setLevel("DEBUG")
        self.logger.debug("initializing app")

        self.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/sqlite.db"

        # Flask-Security configurations
        self.config["SECRET_KEY"] = (
            "super-secret-key"  # In a real app, use an environment variable
        )
        self.config["SECURITY_PASSWORD_SALT"] = "super-secret-salt"
        self.config["SECURITY_REGISTERABLE"] = True
        self.config["SECURITY_SEND_REGISTER_EMAIL"] = False
        self.config["SECURITY_RECOVERABLE"] = True
        self.config["SECURITY_TRACKABLE"] = True
        self.config["SECURITY_PASSWORD_HASH"] = "bcrypt"

        self.config["CELERY"] = {
            "broker_url": "redis://localhost:6379/0",
            "backend_url": "redis://localhost:6379/0",
        }


app = CustomApp("app")


@app.template_filter("sydney_tz")
def sydney_tz(value):
    if value is None:
        return ""
    # Assume the database time is UTC
    utc_time = value.replace(tzinfo=ZoneInfo("UTC"))
    return utc_time.astimezone(ZoneInfo("Australia/Sydney"))

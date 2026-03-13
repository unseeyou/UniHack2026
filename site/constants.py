from flask import Flask
from database.db_cmds import Database


class CustomApp(Flask):
    def __init__(self, *args, **kwargs):
        super(CustomApp, self).__init__(*args, **kwargs)
        self.logger.setLevel("DEBUG")
        self.database: Database = Database()
        self.logger.debug("initializing app")


app = CustomApp("app")

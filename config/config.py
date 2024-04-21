import os
from configparser import ConfigParser


class Configuration:
    def __init__(self):
        self.config_path = "./config/app.cfg"
        self.config = None

        self.scheme = None
        self.host = None
        self.port = None
        self.base_url = None
        self.db_name = None
        self.db_echo = True

        self.secret_key = None
        self.algorithm = None
        self.access_token_expire_minutes = None

        self.CORS_ORIGINS = None

        self.tickets = None

        self.initialize()

    def load_config(self):
        self.config = ConfigParser()
        self.config.read(self.config_path)

    def initialize(self):
        self.load_config()

        self.scheme = self.config["dev-server"]["scheme"]
        self.host = self.config["dev-server"]["host"]
        self.port = self.config["dev-server"]["port"]
        self.base_url = f"{self.scheme}://{self.host}:{self.port}"
        self.db_name = self.config["db"]["db_name"]

        self.secret_key = self.config["jwt"]["secret_key"]
        self.algorithm = self.config["jwt"]["algorithm"]
        self.access_token_expire_minutes = self.config["jwt"][
            "access_token_expire_minutes"
        ]

        self.CORS_ORIGINS = self.config["CORS"]["allow_origin"]

        self.tickets = int(self.config["core"]["tickets"])

        if self.config["environment"]["env"] == "prod" or os.getenv("ENV") == "prod":
            self.db_echo = False
            self.host = self.config["prod-server"]["host"]
            self.port = self.config["prod-server"]["port"]
            self.base_url = f"{self.scheme}://{self.host}:{self.port}"

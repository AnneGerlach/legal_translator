"""
Configuration of .env variables and logging, as well as other settings constants
"""
import os.path
from enum import Enum
from functools import lru_cache
from pathlib import Path

import toml
from pydantic import BaseModel, ValidationError, validator, model_validator

from pydantic_settings import BaseSettings, SettingsConfigDict

APP_NAME = "legal translator"
DESCRIPTION = "legal translator!"
CONTACT_PERSON = "Anne Gerlach"
CONTACT_EMAIL = "annegerlach94@gmx.de"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = os.path.join(BASE_DIR, "src")
DEPLOYMENT_DIR = os.path.join(BASE_DIR, "deployment")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

with open(BASE_DIR / "pyproject.toml", "r") as f:
    version = toml.loads(f.read())["project"]["version"]

VERSION = version


LOGGER_NAME = f"{APP_NAME}log"
LOG_FILE_NAME = f"{APP_NAME}.log"


class DeployEnvironments(Enum):
    DEV = "DEV"
    LOCAL = "LOCAL"
    STAGE = "STAGE"
    PRODUCTION = "PROD"
    TESTING = "TEST"


REMOTE_ENVIRONMENTS = [DeployEnvironments.DEV,
                       DeployEnvironments.STAGE,
                       DeployEnvironments.PRODUCTION]


class Settings(BaseSettings):
    """
    read env variables, cast and validate them.
    variable names are case insensitive.
    """
    deploy_environment: DeployEnvironments = DeployEnvironments.LOCAL
    gcp_project_number: str = ""
    db_user: str = ""  # only relevant for remote deployment
    db_password: str = ""  # only relevant for remote deployment
    db_host: str = "localhost"
    db_port: int = 27017  # only relevant for local deployment
    db_name: str = ""
    db_collection: str = "legal_translations"
    openai_api_key: str = ""
    model_config = SettingsConfigDict(env_file=os.path.join(DEPLOYMENT_DIR, ".env"))

    def is_deployed_remotely(self):
        return self.deploy_environment in REMOTE_ENVIRONMENTS

    def is_deployed_locally(self):
        return not self.is_deployed_remotely()

    @model_validator(mode="after")
    def check_not_localhost_for_remote_deployment(self):  # noqa: N805
        if self.deploy_environment in REMOTE_ENVIRONMENTS \
                and self.db_host == "localhost":
            raise ValidationError(f"This env variable must be changed when deploying remotely! "
                                  f"(value: {self.db_host})")
        return self

    def mdb_connection_string(self):
        if self.is_deployed_locally():  # no auth for the local database
            return f"mongodb://{self.db_host}:{self.db_port}"

        return (f"mongodb+srv://{self.db_user}:{self.db_password}@{self.db_host}"
                f"/?retryWrites=true&w=majority")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    logs_file_name: str = LOG_FILE_NAME  # can be overwritten when initialising the model

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "file_formatter": {
            "class": "logging.Formatter",
            "format": "%(asctime)s\t%(levelname)s\t%(filename)s\t%(message)s",
            "datefmt": "%d %b %y %H:%M:%S"
        }
    }
    handlers: dict = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
            "stream": "ext://sys.stdout"
            # "stream": "ext://sys.stderr",
        },
    }

    loggers: dict = {
        LOGGER_NAME: {"handlers": ["console", "file"], "level": "DEBUG"},
    }

    # allows using logging.info() (or debug, warning etc)
    # instead of having to get the logger each time
    root: dict = {
        "level": "DEBUG",
        "handlers": ["file"]
    }

    def __init__(self, logs_file_name: str = "", **kwargs):
        logs_file_name = logs_file_name or LOG_FILE_NAME
        super(LogConfig, self).__init__(logs_file_name=logs_file_name, **kwargs)
        if not os.path.exists(LOGS_DIR):
            os.mkdir(LOGS_DIR)
        self.handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file_formatter",
            "level": "DEBUG",
            "filename": os.path.join(LOGS_DIR, self.logs_file_name),
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 4
        }

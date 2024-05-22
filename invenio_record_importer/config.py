#! /usr/bin/env python

"""Importer configuration.

Allows setting configuration variables either through the Flask application
configuration or through environment variables. Also provides sane defaults
where applicable. Flask configuration variables take precedence over
environment variables.
"""

import os
from pathlib import Path


class ImporterConfig:

    def __init__(self, app):
        # FIXME: Change these names to begin with RECORD_IMPORTER_
        # instead of MIGRATION_
        if app.config.get("MIGRATION_SERVER_DATA_DIR"):
            DATA_DIR = Path(app.config.get("MIGRATION_SERVER_DATA_DIR"))
        elif os.getenv("MIGRATION_SERVER_DATA_DIR"):
            DATA_DIR = Path(os.getenv["MIGRATION_SERVER_DATA_DIR"])
        else:
            DATA_DIR = Path(Path(__file__).parents[2], "kcr-untracked-files")
        self.MIGRATION_SERVER_DATA_DIR = DATA_DIR

        if app.config.get("MIGRATION_SERVER_FILES_LOCATION"):
            FILES_LOCATION = Path(
                app.config.get("MIGRATION_SERVER_FILES_LOCATION")
            )
        if os.getenv("MIGRATION_SERVER_FILES_LOCATION"):
            FILES_LOCATION = Path(
                os.environ["MIGRATION_SERVER_FILES_LOCATION"]
            )
        else:
            FILES_LOCATION = DATA_DIR / "humcore"
        self.MIGRATION_SERVER_FILES_LOCATION = FILES_LOCATION

        if app.config.get("MIGRATION_SERVER_DOMAIN"):
            SERVER_DOMAIN = app.config.get("MIGRATION_SERVER_DOMAIN")
        else:
            SERVER_DOMAIN = os.getenv(
                "MIGRATION_SERVER_DOMAIN", "localhost: 5000"
            )
        self.MIGRATION_SERVER_DOMAIN = SERVER_DOMAIN

        if app.config.get("MIGRATION_SERVER_PROTOCOL"):
            SERVER_PROTOCOL = app.config.get("MIGRATION_SERVER_PROTOCOL")
        else:
            SERVER_PROTOCOL = os.getenv("MIGRATION_SERVER_PROTOCOL", "https")
        self.MIGRATION_SERVER_PROTOCOL = SERVER_PROTOCOL

        if app.config.get("MIGRATION_API_TOKEN"):
            self.API_TOKEN = app.config.get("MIGRATION_API_TOKEN")
        elif os.getenv("MIGRATION_API_TOKEN"):
            self.API_TOKEN = os.getenv("MIGRATION_API_TOKEN")
        else:
            raise ValueError("Missing config value: MIGRATION_API_TOKEN")

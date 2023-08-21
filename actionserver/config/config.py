import configparser
import json
import logging
import os
from types import SimpleNamespace


class Config:
    settings_path = os.environ.get("ACTION_SETTINGS_PATH")

    def __init__(self):
        try:
            data = open(self.settings_path).read()
            self.settings = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        except Exception as e:
            print(e)

    def get_loglevel(self):
        parser = configparser.ConfigParser()
        parser.read(self.settings.log.verbosity)
        logleveldict = {
            'info': logging.INFO,
            'debug': logging.DEBUG,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
            'warning': logging.WARNING
        }
        loglevel = logleveldict.get(self.settings.log.verbosity, logging.ERROR)
        return loglevel

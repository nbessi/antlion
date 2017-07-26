# -*- coding: utf-8 -*-
import os
from os.path import expanduser
from pathlib import Path
import configparser


class ConfigurationError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)


def get_config():
    home = expanduser("~")
    config_file_candidates = [
        Path('/etc', 'antlion.ini'),
        Path(home, 'antlion.ini'),
    ]

    env_path = os.environ.get('ANTLION_CONFIG_PATH')
    if env_path:
        config_file_candidates.insert(0, Path(env_path))

    config_path = None
    for path in config_file_candidates:
        if path.exists():
            config_path = path
    if not config_path:
        raise ConfigurationError(
            ("Configuration file not found you should either "
             "set the ANTLION_CONFIG_PATH variable or "
             "create a file in one of the following location: {}").format(
                 "\n".join(str(x) for x in config_file_candidates))
        )

    config = configparser.ConfigParser()
    config.read(config_path)
    if 'antlion' not in config:
        raise ConfigurationError("Section [antlion] is not in config file")
    if not config.has_option('antlion', 'endpoint'):
        raise ConfigurationError(
            "'endpoint' option is mandatory in antlion section"
        )
    return config

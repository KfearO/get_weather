from get_weather_classes import *
import tempfile
import os.path
import json
import logging
from logging.handlers import RotatingFileHandler


def get_weather_logger():
    try:
        with open("my_config.json", "r") as config_params:
            config_json = json.load(config_params)
        log_level = config_json["log_parameters"]["log_level"]
        log_size_kb = config_json["log_parameters"]["log_size_KB"]
        log_file_path = config_json["log_parameters"]["log_file_path"]
        log_file_name = config_json["log_parameters"]["log_file_name"]
        backup_logs = config_json["log_parameters"]["backup_logs"]
        if not os.path.isdir(log_file_path):
            raise GetWeatherException(10, "No such directory: '" + log_file_path + "' check your config file")
    except FileNotFoundError or KeyError as err:
        if err is KeyError:
            raise err
        log_level = "INFO"
        log_size_kb = 23
        log_file_path = tempfile.gettempdir()
        log_file_name = "temp_get_weather.log"
        backup_logs = 9

    log_format = logging.Formatter('%(asctime)s.%(msecs)03d|%(levelname)s|%(threadName)s|%(funcName)s()|%(message)s',
                                   '%d/%m/%Y %H:%M:%S')
    log_handler = RotatingFileHandler(filename=os.path.join(log_file_path, log_file_name), mode='a',
                                      maxBytes=log_size_kb * 1024, backupCount=backup_logs, encoding='utf_8')
    log_handler.setFormatter(log_format)
    log_handler.setLevel(log_level)

    get_weather_logging = logging.getLogger('logger')
    get_weather_logging.setLevel(log_level)
    get_weather_logging.addHandler(log_handler)

    return get_weather_logging

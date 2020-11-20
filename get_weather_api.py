from get_weather_classes import *
import urllib.request
import urllib.parse
import tempfile
import os.path
import json
import logging
from logging.handlers import RotatingFileHandler
from cryptography.fernet import Fernet


# This function is for encrypting 'appid' when writing the url to the log.
# *** The key to decrypt isn't saved ***
def encrypt_appid(url_values, api_url_partial):
    url_values["appid"] = Fernet(Fernet.generate_key()).encrypt(url_values["appid"].encode())
    return api_url_partial + urllib.parse.urlencode(url_values)


def get_weather_logger(logger_config_file="my_config.json"):
    try:
        with open(logger_config_file, "r") as config_params:
            config_json = json.load(config_params)
        log_level = config_json["log_parameters"]["log_level"]
        log_size_kb = config_json["log_parameters"]["log_size_KB"]
        log_file_path = config_json["log_parameters"]["log_file_path"]
        log_file_name = config_json["log_parameters"]["log_file_name"]
        backup_logs = config_json["log_parameters"]["backup_logs"]
        if not os.path.isdir(log_file_path):
            raise GetWeatherException(31, "No such directory: '" + log_file_path + "' check your config file")
    except KeyError as err:
        raise GetWeatherException(32, "Missing key: " + err.__str__() + " in config file: '" + logger_config_file + "'")
    except FileNotFoundError:
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

    new_get_weather_logger = logging.getLogger('logger')
    new_get_weather_logger.setLevel(log_level)
    new_get_weather_logger.addHandler(log_handler)
    return new_get_weather_logger


get_weather_logging = get_weather_logger()


def get_weather_api(location, appid, logger=None):
    if logger is None:
        global get_weather_logging
    else:
        get_weather_logging = logger
    get_weather_logging.info("----- Start " +
                             logging.getLevelName(get_weather_logging.getEffectiveLevel()) + " -----")
    if type(location) is not Location:
        e = GetWeatherException(21, "Location type is mandatory")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e
    if location.city == "" or location.city is None:
        e = GetWeatherException(22, "city is mandatory. got None or empty string")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e
    if location.state == "":
        location.state = None
    if appid is None or appid == "":
        e = GetWeatherException(23, "appid is mandatory")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e

    if location.units == "" or location.units is None:
        get_weather_logging.info("units parameter is not defined, returned temperature would be in 'kelvin', "
                                 "wind speed in a metric unit")
        url_units = "kelvin"
    elif location.units.lower() != "imperial" and location.units.lower() != "metric" \
            and location.units.lower() != "kelvin":
        e = GetWeatherException(24, "units parameter can only be 'metric', 'imperial', 'kelvin' or 'None', got: '"
                                + str(location.units) + "'")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e
    else:
        url_units = location.units.lower()

    api_url_partial = "https://api.openweathermap.org/data/2.5/weather?"

    url_location_values = str(location.city)
    if location.state is not None:
        url_location_values = url_location_values + "," + str(location.state)

    url_values = {
        "q": url_location_values,
        "units": url_units.lower(),
        "appid": appid
    }

    url_values_encoded = urllib.parse.urlencode(url_values)
    api_url = api_url_partial + url_values_encoded

    try:
        get_weather_logging.info("Request:")
        get_weather_logging.debug(encrypt_appid(url_values, api_url_partial))  # Writing url to log - encrypted appid
        # get_weather_logging.debug(api_url)  # Writing url to log - *** NOT encrypted appid ***
        json_weather_data = json.load(urllib.request.urlopen(api_url))
    except Exception as e:
        if e.__str__() == "HTTP Error 404: Not Found":
            error_message = "No such location: '" + str(location) + "' or wrong API call"
        else:
            error_message = "Something went wrong: " + e.__str__()
        e = GetWeatherException(25, error_message)
        get_weather_logging.critical("exception:", exc_info=e)
        raise e

    get_weather_logging.info("Response:")
    get_weather_logging.debug(str(json_weather_data).encode(errors="ignore"))

    try:
        raw_humidity = json_weather_data["main"]["humidity"]
        raw_temperature = json_weather_data["main"]["temp"]
        raw_pressure = json_weather_data["main"]["pressure"]
        raw_wind_speed = json_weather_data["wind"]["speed"]
        raw_wind_direction = json_weather_data["wind"]["deg"]
        raw_cloud_cover = json_weather_data["clouds"]["all"]
    except KeyError as e:
        e = GetWeatherException(26, "Failed to parse data: " + e.__str__() + " no such key")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e

    raw_precipitations_type = None
    try:
        raw_precipitation_snow = json_weather_data["snow"]["1h"]
    except KeyError:
        try:
            raw_precipitation = json_weather_data["rain"]["1h"]
            raw_precipitations_type = "rain"
        except KeyError:
            get_weather_logging.warning("json has no precipitation data, setting 'raw_precipitation = \"(0)\"'")
            raw_precipitation = "(0)"
    else:
        raw_precipitation = raw_precipitation_snow
        raw_precipitations_type = "snow"

    try:
        if location.state is None:
            location = Location(location.city, "(" + str(json_weather_data["sys"]["country"]) + ")", location.units)
            get_weather_logging.warning("City is located at: " + str(location.state)
                                        + " according to 'openweathermap.org' response")
    except KeyError as e:
        get_weather_logging.warning("Failed to locate State from 'openweathermap.org' response" + e.__str__())
        location = Location(location.city, "(** Unknown State **)")

    get_weather_logging.debug(msg="\n" + Weather(raw_humidity, raw_temperature, raw_pressure, raw_wind_speed,
                                                 raw_wind_direction, raw_cloud_cover, raw_precipitation))

    get_weather_logging.info("----- End -----")
    return Weather(raw_humidity, raw_temperature, raw_pressure, raw_wind_speed,
                   raw_wind_direction, raw_cloud_cover, raw_precipitation, raw_precipitations_type), location

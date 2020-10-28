from get_weather_classes import *
import os.path
import json
import urllib.request
import urllib.parse
import logging
from logging.handlers import RotatingFileHandler
from cryptography.fernet import Fernet

with open("config.json", "r") as c:
    config = json.load(c)
    log_level = config["log_parameters"]["log_level"]
    log_size_KB = config["log_parameters"]["log_size_KB"]
    log_file_path = config["log_parameters"]["log_file_path"]
    log_file_name = config["log_parameters"]["log_file_name"]
    backup_logs = config["log_parameters"]["backup_logs"]

log_format = logging.Formatter('%(asctime)s.%(msecs)03d|%(levelname)s|%(threadName)s|%(funcName)s()|%(message)s',
                               '%d/%m/%Y %H:%M:%S')
log_handler = RotatingFileHandler(filename=os.path.join(log_file_path, log_file_name), mode='a',
                                  maxBytes=log_size_KB * 1024, backupCount=backup_logs, encoding='utf_8')
log_handler.setFormatter(log_format)
log_handler.setLevel(log_level)

get_weather_logging = logging.getLogger('logger')
get_weather_logging.setLevel(log_level)
get_weather_logging.addHandler(log_handler)


# This function is for encrypting 'appid' when writing the url to the log.
# *** The key to decrypt isn't saved ***
def encrypt_appid(url_values, api_url_partial):
    url_values["appid"] = Fernet(Fernet.generate_key()).encrypt(url_values["appid"].encode())
    return api_url_partial + urllib.parse.urlencode(url_values)


def get_weather_api(location, appid, units="_metric"):
    get_weather_logging.info("----- Start " + str(log_level) + " -----")
    if type(location) is not Location:
        e = GetWeatherException(11, "Location type is mandatory")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e
    if location.city == "":
        e = GetWeatherException(12, "city is mandatory. got empty string")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e
    if location.state == "":
        location.state = None
    if appid is None or appid == "":
        e = GetWeatherException(13, "appid is mandatory")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e
    if units == "_metric" or units == "" or units is None:
        get_weather_logging.info("units parameter is not defined, using 'metric' as default")
        units = "metric"
    else:
        if units.lower() != "imperial" and units.lower() != "metric":
            e = GetWeatherException(14, "units parameter can only be 'metric' or 'imperial', got: '" + str(units) + "'")
            get_weather_logging.critical("exception:", exc_info=e)
            raise e

    api_url_partial = "https://api.openweathermap.org/data/2.5/weather?"

    url_location_values = str(location.city)
    if location.state is not None:
        url_location_values = url_location_values + "," + str(location.state)

    url_values = {
        "q": url_location_values,
        "units": units.lower(),
        "appid": appid
    }

    url_values_encoded = urllib.parse.urlencode(url_values)
    api_url = api_url_partial + url_values_encoded

    try:
        get_weather_logging.info("Request:")
        get_weather_logging.debug(encrypt_appid(url_values, api_url_partial))    # Writing url to log - encrypted appid
        # get_weather_logging.debug(api_url)    # Writing url to log - *** NOT encrypted appid ***
        json_weather_data = json.load(urllib.request.urlopen(api_url))
    except Exception as e:
        if e.__str__() == "HTTP Error 404: Not Found":
            error_message = "No such location: '" + str(location) + "' or wrong API call"
        else:
            error_message = "Something went wrong: " + e.__str__()
        e = GetWeatherException(15, error_message)
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
        e = GetWeatherException(15, "Failed to parse data: " + e.__str__() + " no such key")
        get_weather_logging.critical("exception:", exc_info=e)
        raise e

    try:
        raw_precipitation = json_weather_data["rain"]["1h"]
    except KeyError:
        get_weather_logging.warning("json has no precipitation data, setting 'raw_precipitation = \"(0)\"'")
        raw_precipitation = "(0)"

    try:
        if location.state is None:
            location = Location(location.city, "(" + str(json_weather_data["sys"]["country"]) + ")")
            get_weather_logging.warning("City is located at: " + str(location.state) + " according to json")
    except KeyError as e:
        get_weather_logging.warning("Failed to locate city State from json" + e.__str__())
        location = Location(location.city, "(** Unknown State **)")

    get_weather_logging.debug(msg="\n" + Weather(raw_humidity, raw_temperature, raw_pressure, raw_wind_speed,
                                                 raw_wind_direction, raw_cloud_cover, raw_precipitation))

    get_weather_logging.info("----- End -----")
    return Weather(raw_humidity, raw_temperature, raw_pressure, raw_wind_speed,
                   raw_wind_direction, raw_cloud_cover, raw_precipitation), location

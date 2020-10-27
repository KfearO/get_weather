import json
from get_weather_api import get_weather_api
from get_weather_classes import GetWeatherException, Location
import concurrent.futures
"""
A Short demonstration program to showcase how to use the get_weather_api()
Notice the differences in each function call
Also pay attention to the 'my_config.json' reading, which is a private file,
a public demo file exist in the project - 'config.json' 
"""


def get_current_weather(check_location, private_api_key, units=None):
    current_weather, check_location = get_weather_api(check_location, private_api_key, units)
    print(check_location + "\n" + current_weather + "\n")


if __name__ == "__main__":
    try:
        with open("my_config.json", "r") as c:
            api_key = json.load(c)["application_parameters"]["api_key"]
            get_current_weather_thread = concurrent.futures.ThreadPoolExecutor(4)
            get_current_weather_thread.submit(get_current_weather, Location("New York"), api_key, "imperial")
            get_current_weather_thread.submit(get_current_weather, Location("London", "Great Britain"), api_key)
            get_current_weather_thread.submit(get_current_weather, Location("paris", "fr"), api_key, "metric")
            get_current_weather_thread.submit(get_current_weather, Location("Tel-Aviv", "IL"), api_key)

    except GetWeatherException as e:
        print(e.__str__() + "\n")
        raise e

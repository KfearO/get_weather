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


def run_get_weather_api(locations_list):
    results_list = []
    get_current_weather_thread = concurrent.futures.ThreadPoolExecutor(3)
    for each_location in locations_list:
        results_list.append(get_current_weather_thread.submit(get_weather_api, each_location[0], each_location[1]))
    return results_list


if __name__ == "__main__":
    with open("my_config.json", "r") as c:
        api_key = json.load(c)["application_parameters"]["api_key"]

    check_locations_list = [
        [Location("Tel-Aviv", "IL"), api_key],
        [Location("Tel-Aviv", "IL", "metric"), api_key],
        [Location("Tel-Aviv", "IL", "imperial"), api_key],
        [Location("Clear Creek", units="imperial"), api_key],
        [Location("Clear Creek", "CA", "imperial"), api_key],
        [Location("London", "Great Britain"), api_key],
        [Location("paris", "fr", "kelvin"), api_key],
        [Location("Canberra", "AUS"), api_key]
                       ]

    threading_results = run_get_weather_api(check_locations_list)
    concurrent.futures.wait(threading_results)
    for weather_results in threading_results:
        try:
            result_current_weather, result_location = weather_results.result()
            print(result_location + "\n" + result_current_weather.string_with_units(result_location.units) + "\n")
        except GetWeatherException as e:
            print(e + "\n")

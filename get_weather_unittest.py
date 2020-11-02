import unittest
import json
import os
from get_weather_classes import *
from get_weather_api import get_weather_api

config_file = "my_config.json"
test_config_file = "not_my_config.json"

with open(config_file, "r") as c:
    good_api_key = json.load(c)["application_parameters"]["api_key"]

good_location_and_units = Location("Giv‘atayim", "IL", "Metric")
good_location_units_metric = Location("Berlin", "DE", "imperial")
good_location_units_imperial = Location("mexico city", "mexico")
good_location_units_kelvin = Location("Rome", "Italy", "KELVIN")
good_location_units_empty_string = Location("sydney", "aus", "")
city_with_hyphen_state_full_name = Location("Tel-Aviv", "Israel")
city_only_location = Location("London")
city_only_location_with_space = Location("New York")
city_only_location_state_empty_string = Location("Madrid", "")
city_with_special_char = Location("La Cañada Flintridge")

good_location_units_wrong = Location("Canberra", "au", "metrical")
incorrect_type_location = "Munich"
city_empty_string_location = Location("", "US")
city_with_incorrect_state = Location("Paris", "IL")
empty_string_api_key = ""
city_with_equal_char = Location("Tel=Aviv", "IL")
unauthorised_api_key = "NoSuchApiKey"


def print_results(weather, location):
    print("Expected: ", Weather, Location)
    print("Got:      ", type(weather), type(location))
    print(location + "\n" + weather.string_with_units(location.units))


class TestGetWeather(unittest.TestCase):
    def test_all_positive(self):
        (weather, location) = get_weather_api(location=good_location_and_units, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_units_metric(self):
        (weather, location) = get_weather_api(location=good_location_units_metric, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_units_imperial(self):
        (weather, location) = get_weather_api(location=good_location_units_imperial, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_units_kelvin(self):
        (weather, location) = get_weather_api(location=good_location_units_kelvin, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_units_empty_string(self):
        (weather, location) = get_weather_api(location=good_location_units_empty_string, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_city_with_hyphen_state_full_name(self):
        (weather, location) = get_weather_api(location=city_with_hyphen_state_full_name, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_city_only_location(self):
        (weather, location) = get_weather_api(location=city_only_location, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_city_only_with_space(self):
        (weather, location) = get_weather_api(location=city_only_location_with_space, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_city_only_with_special_char(self):
        (weather, location) = get_weather_api(location=city_with_special_char, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_city_only_location_state_empty_string(self):
        (weather, location) = get_weather_api(location=city_only_location_state_empty_string, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_no_config_json(self):
        os.rename(config_file, test_config_file)
        (weather, location) = get_weather_api(location=city_only_location_state_empty_string, appid=good_api_key)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)
        os.rename(test_config_file, config_file)

    def test_incorrect_type_location(self):
        with self.assertRaises(GetWeatherException):
            get_weather_api(location=incorrect_type_location, appid=good_api_key)

    def test_city_empty_string_location(self):
        with self.assertRaises(GetWeatherException):
            get_weather_api(location=city_empty_string_location, appid=good_api_key)

    def test_incorrect_state(self):
        with self.assertRaises(GetWeatherException):
            get_weather_api(location=city_with_incorrect_state, appid=good_api_key)

    def test_empty_api_key(self):
        with self.assertRaises(GetWeatherException):
            get_weather_api(location=good_location_and_units, appid=empty_string_api_key)

    def test_units_wrong(self):
        with self.assertRaises(GetWeatherException):
            get_weather_api(location=good_location_units_wrong, appid=good_api_key)

    def test_unknown_location(self):
        with self.assertRaises(GetWeatherException):
            get_weather_api(location=city_with_equal_char, appid=good_api_key)

    def test_unauthorised_api_key(self):
        with self.assertRaises(GetWeatherException):
            get_weather_api(location=city_with_equal_char, appid=unauthorised_api_key)


if __name__ == '__main__':
    unittest.main()

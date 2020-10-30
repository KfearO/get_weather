import unittest
import json
from get_weather_classes import *
from get_weather_api import get_weather_api

with open("my_config.json", "r") as c:
    good_api_key = json.load(c)["application_parameters"]["api_key"]

good_location_no_units = Location("Giv‘atayim", "IL")
good_location_units_metric = Location("Berlin", "DE", "Metric")
good_location_units_imperial = Location("mexico city", "mexico", "imperial")
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
    print(location + "\n" + weather)


class TestGetWeather(unittest.TestCase):
    def test_all_positive_units_none(self):
        (weather, location) = get_weather_api(location=good_location_no_units, appid=good_api_key)
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
            get_weather_api(location=good_location_no_units, appid=empty_string_api_key)

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

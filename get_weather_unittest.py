import unittest
import json
from get_current_weather import get_current_weather
from get_weather_classes import *
from get_weather_api import get_weather_api

with open("my_config.json", "r") as c:
    good_api_key = json.load(c)["application_parameters"]["api_key"]

good_location = Location("Giv‘atayim", "IL")
city_with_hyphen_state_full_name = Location("Tel-Aviv", "Israel")
city_only_location = Location("London")
city_only_location_with_space = Location("New York")
city_with_special_char = Location("La Cañada Flintridge")
units_metric = "metric"
units_imperial = "imperial"

incorrect_type_location = "Munich"
city_empty_string_location = Location("", "US")
city_with_incorrect_state = Location("Paris", "IL")
empty_string_api_key = ""
units_wrong = "metrical"
units_empty_string = ""
city_with_equal_char = Location("Tel=Aviv", "IL")
unauthorised_api_key = "NoSuchApiKey"


class TestGetWeather(unittest.TestCase):
    def test_all_positive_units_none(self):
        (weather, location) = get_weather_api(location=good_location, appid=good_api_key, units=None)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print("Expected: ", Weather, Location)
        print("Got:      ", type(weather), type(location))

    def test_units_metric(self):
        self.assertFalse(
            get_current_weather(
                private_api_key=good_api_key,
                check_location=good_location,
                units=units_metric
            )
        )

    def test_units_imperial(self):
        self.assertFalse(
            get_current_weather(
                private_api_key=good_api_key,
                check_location=good_location,
                units=units_imperial
            )
        )

    def test_units_empty_string(self):
        self.assertFalse(
            get_current_weather(
                private_api_key=good_api_key,
                check_location=good_location,
                units=units_empty_string
            )
        )

    def test_city_with_hyphen_state_full_name(self):
        self.assertFalse(
            get_current_weather(
                private_api_key=good_api_key,
                check_location=city_with_hyphen_state_full_name
            )
        )

    def test_city_only_location(self):
        self.assertFalse(
            get_current_weather(
                private_api_key=good_api_key,
                check_location=city_only_location
            )
        )

    def test_city_only_with_space(self):
        self.assertFalse(
            get_current_weather(
                private_api_key=good_api_key,
                check_location=city_only_location_with_space
            )
        )

    def test_city_only_with_special_char(self):
        self.assertFalse(
            get_current_weather(
                private_api_key=good_api_key,
                check_location=city_with_special_char
            )
        )

    def test_incorrect_type_location(self):
        with self.assertRaises(GetWeatherException):
            get_current_weather(
                private_api_key=good_api_key,
                check_location=incorrect_type_location
            )

    def test_city_empty_string_location(self):
        with self.assertRaises(GetWeatherException):
            get_current_weather(
                private_api_key=good_api_key,
                check_location=city_empty_string_location
            )

    def test_incorrect_state(self):
        with self.assertRaises(GetWeatherException):
            get_current_weather(
                private_api_key=good_api_key,
                check_location=city_with_incorrect_state
            )

    def test_empty_api_key(self):
        with self.assertRaises(GetWeatherException):
            get_current_weather(
                private_api_key=empty_string_api_key,
                check_location=good_location
            )

    def test_units_wrong(self):
        with self.assertRaises(GetWeatherException):
            get_current_weather(
                private_api_key=good_api_key,
                check_location=good_location,
                units=units_wrong
            )

    def test_unknown_location(self):
        with self.assertRaises(GetWeatherException):
            get_current_weather(
                private_api_key=good_api_key,
                check_location=city_with_equal_char
            )

    def test_unauthorised_api_key(self):
        with self.assertRaises(GetWeatherException):
            get_current_weather(
                private_api_key=unauthorised_api_key,
                check_location=good_location
            )


if __name__ == '__main__':
    unittest.main()

import unittest
from get_weather_api import *


config_file = "my_config.json"
test_config_file = "not_my_config.json"

with open(config_file, "r") as c:
    good_api_key = json.load(c)["application_parameters"]["api_key"]

good_location_and_units = Location("Giv‘atayim", "IL", "Metric")
good_location_units_none = Location("Berlin", "DE")
good_location_units_imperial = Location("mexico city", "mexico", "Imperial")
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
city_none_location = Location(city=None, state="RU")
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

    def test_units_none(self):
        (weather, location) = get_weather_api(location=good_location_units_none, appid=good_api_key)
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
        test_logger = get_weather_logger("no.such_file")
        (weather, location) = get_weather_api(location=city_only_location_state_empty_string, appid=good_api_key,
                                              logger=test_logger)
        self.assertEqual((type(weather), type(location)), (Weather, Location))
        print_results(weather, location)

    def test_incorrect_log_file_path_in_jason(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_logger("incorrect_log_file_path.json")
        print(e.exception.__str__())

    def test_bad_key_in_jason(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_logger("bad_key.json")
        print(e.exception.__str__())

    def test_incorrect_type_location(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_api(location=incorrect_type_location, appid=good_api_key)
        print(e.exception.__str__())

    def test_city_empty_string_location(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_api(location=city_empty_string_location, appid=good_api_key)
        print(e.exception.__str__())

    def test_city_none_location(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_api(location=city_none_location, appid=good_api_key)
        print(e.exception.__str__())

    def test_incorrect_state(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_api(location=city_with_incorrect_state, appid=good_api_key)
        print(e.exception.__str__())

    def test_empty_api_key(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_api(location=good_location_and_units, appid=empty_string_api_key)
        print(e.exception.__str__())

    def test_units_wrong(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_api(location=good_location_units_wrong, appid=good_api_key)
        print(e.exception.__str__())

    def test_unknown_location(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_api(location=city_with_equal_char, appid=good_api_key)
        print(e.exception.__str__())

    def test_unauthorised_api_key(self):
        with self.assertRaises(GetWeatherException) as e:
            get_weather_api(location=good_location_units_none, appid=unauthorised_api_key)
        print(e.exception.__str__())

    def test_Location_string_with_wrong_units(self):
        (weather, location) = get_weather_api(location=good_location_and_units, appid=good_api_key)
        with self.assertRaises(GetWeatherException) as e:
            weather.string_with_units(units="incorrect_units")
        print(e.exception.__str__())


if __name__ == '__main__':
    unittest.main()

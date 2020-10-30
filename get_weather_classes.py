class GetWeatherException(Exception):
    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

    def __str__(self):
        return "Error: " + str(self.error_code) + ", " + self.error_message

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)


class Location:
    def __init__(self, city, state=None):
        self.city = city
        self.state = state

    def __str__(self):
        if self.state is None:
            return str(self.city + ", " + "")
        else:
            return str(self.city + ", " + self.state)

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)


class Weather:
    def __init__(self, humidity, air_temperature, air_pressure,
                 wind_speed, wind_direction, cloud_cover, precipitations):
        self.humidity = humidity
        self.air_temperature = air_temperature
        self.air_pressure = air_pressure
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.cloud_cover = cloud_cover
        self.precipitations = precipitations

    def __str__(self):
        return \
            "Temperature: " + str(self.air_temperature) + ", " + \
            "Humidity: " + str(self.humidity) + ", " + \
            "Air Pressure: " + str(self.air_pressure) + ", " + \
            "Wind Speed: " + str(self.wind_speed) + ", " + \
            "Wind Direction: " + str(self.wind_direction) + ", " + \
            "Cloud Cover: " + str(self.cloud_cover) + ", " + \
            "Precipitations: " + str(self.precipitations)

    def string_with_units(self, units=None):
        if units is None:
            return self.__str__()

        if units.lower() == "metric":
            air_temperature_unit = " C, "
            wind_speed_unit = " Meters/Seconds, "
        elif units.lower() == "imperial":
            air_temperature_unit = " F, "
            wind_speed_unit = " Miles/Hour, "
        else:
            raise GetWeatherException(21, "units can be either 'metric' or 'imperial'")

        humidity_unit = " %, "
        air_pressure_unit = " mb, "
        wind_direction_unit = " deg. "
        cloud_cover_unit = " %, "
        precipitations = " mm/h"

        return \
            "Temperature: " + str(self.air_temperature) + air_temperature_unit + \
            "Humidity: " + str(self.humidity) + humidity_unit + \
            "Air Pressure: " + str(self.air_pressure) + air_pressure_unit + \
            "Wind Speed: " + str(self.wind_speed) + wind_speed_unit + \
            "Wind Direction: " + str(self.wind_direction) + wind_direction_unit + \
            "Cloud Cover: " + str(self.cloud_cover) + cloud_cover_unit + \
            "Precipitations: " + str(self.precipitations) + precipitations

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

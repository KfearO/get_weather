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
                 wind_speed, wind_direction, cloud_cover, precipitation):
        self.humidity = humidity
        self.air_temperature = air_temperature
        self.air_pressure = air_pressure
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.cloud_cover = cloud_cover
        self.precipitation = precipitation

    def __str__(self):
        return \
            "Temperature: " + str(self.air_temperature) + "\n" + \
            "Humidity: " + str(self.humidity) + "\n" + \
            "Air Pressure: " + str(self.air_pressure) + "\n" + \
            "Wind Speed: " + str(self.wind_speed) + "\n" + \
            "Wind Direction: " + str(self.wind_direction) + "\n" + \
            "Cloud Cover: " + str(self.cloud_cover) + "\n" + \
            "Precipitation: " + str(self.precipitation)

    def __add__(self, other):
        return str(self) + str(other)

    def __radd__(self, other):
        return str(other) + str(self)

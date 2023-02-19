# get_weather

Demo project

Python3 (3.9) library for obtaining the current weather in a particular location.  


1.  The library is using 'openweathermap.org' API to obtain the current weather in a particular location  

        The library returns a 'weather object'  
        rather then json data that would be returned from using 'openweathermap.org' API directly  
2. Location is constructed out of one (at least city) or two (city, state) parameters  
3. The default returned temperature will be in 'kelvin' if you don't provide it  
or 'metric' or 'imperial' units if you provide it at your function call.  
2.  You must have an API key (appid). Obtaining appid by registering to openweathermap.org.  
3.  The library has a log that needs be configured, configuration file: 'config.json' rename it to 'my_config.json'.  
4.  The library contains a demonstration program (get_weather_demo.py) that shows the way to use it.  
  
In the demonstration program (get_weather_demo.py):  
1.  Notice the differences in each Location object, you can learn the possibilities.  
2.  Also pay attention to the 'my_config.json' reading, which is a private file that needs to be created  
Or change the program to call the 'config.json' file  

## Be advised:  
**The library is provided as-is**  
**I have no obligations and/or responsibility regarding accuracy of the weather data that will be returned and/or provided.**  

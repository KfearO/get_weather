# get_weather

A Python3 library for obtaining the current weather in a particular location.
1.  The library is using 'openweathermap.org' API to obtain the current weather in a particular location  
Location is constructed out of one (at least city) or two (city, state) parameters  
The default returned values will be in 'metric' units if you don't provide it  
or 'imperial' units if you provide it at your function call.  
2.  You must have an API key (appid), obtaining appid for free by registering to openweathermap.org  
3.  The library contains a short demonstration program (get_current_weather.py) that shows the way to use it  
4.  The library has a log that needs be configured, configuration file: 'config.json'  
  
In the short demonstration program (get_current_weather.py):  
1.  Notice the differences in each function call  
2.  Also pay attention to the 'my_config.json' reading, which is a private file that needs to be created  
Or change the program to call the 'config.json' file  

## Be advised:  
**The library is provided as-is**  
**Because the library is using 'openweathermap.org' API I have no obligations and/or responsibility regarding accuracy of the weather data that will be returned and/or provided.**  

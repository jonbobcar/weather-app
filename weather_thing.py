# weather_thing.py

from darksky.api import DarkSky
import csv
import time
import os.path
import weather_plotter as plt

API_KEY = '117eeede0b36be4e9adee42396747ac7'

darksky = DarkSky(API_KEY)

latitude = 47.209660
longitude = -122.425690
fcst = darksky.get_forecast(latitude, longitude)



line = {
    'now_temp':     fcst.currently.apparent_temperature,
    'now_icon':     fcst.currently.icon,
    'fcst_temp':    fcst.daily.data[0].temperature_high,
    'fcst_icon':    fcst.daily.data[0].icon,
    'year':         time.strftime('%Y'),
    'month':        time.strftime('%m'),
    'day':          time.strftime('%d'),
    'hour':         time.strftime('%H'),
    'minute':       time.strftime('%M'),
    'second':       time.strftime('%S'),
    'now_humi':     fcst.currently.humidity
}

file_name = 'data_weather_thing.csv'
file_exists = os.path.isfile(file_name)


with open(file_name, 'a') as f:
    fieldnames = ['year', 'month', 'day', 'hour', 'minute', 'second', 'now_temp',
                  'fcst_temp', 'now_icon', 'fcst_icon', 'now_humi']
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
        csv_writer.writeheader()
    csv_writer.writerow(line)

plt.plotweather(file_name)

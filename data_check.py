# data_check.py

import csv
import time
import datetime

# Open CSV data file
with open('data_weather_thing.csv', 'r') as f:
    csv_reader = csv.DictReader(f)
    csv_data = list(csv_reader)

line = csv_data[-1]
last_hour = line['hour']
current_time = time.localtime()
current_hour = datetime.datetime.strftime(datetime.datetime.today(), '%H')
full_time = datetime.datetime.strftime(datetime.datetime.today(), '%D %H:%M')

if last_hour != current_hour:
    import weather_thing
else:
    pass

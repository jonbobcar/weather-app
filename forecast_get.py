import urllib.request
import json
import csv
import datetime
import os

with urllib.request.urlopen("https://api.weather.gov/gridpoints/SEW/117,49/forecast") as url:
    data = json.loads(url.read().decode())

filename = "3_day_fcst.csv"
file_exists = os.path.isfile(filename)
fieldnames = ["now_time",
              "fcst_date",
              "name_high",
              "day_detail",
              "high",
              "name_low",
              "night_detail",
              "low"]

now_time = datetime.datetime.strftime(
    datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
fcst_date = datetime.datetime.strftime(
    datetime.datetime.today() + datetime.timedelta(days=3), "%Y-%m-%d")
high = data["properties"]["periods"][6]["temperature"]
low = data["properties"]["periods"][7]["temperature"]
name_high = data["properties"]["periods"][6]["name"]
name_low = data["properties"]["periods"][7]["name"]
day_detail = data["properties"]["periods"][6]["shortForecast"]
night_detail = data["properties"]["periods"][7]["shortForecast"]

write_line = {"now_time":       now_time,
              "fcst_date":      fcst_date,
              "name_high":      name_high,
              "day_detail":     day_detail,
              "high":           high,
              "name_low":       name_low,
              "night_detail":   night_detail,
              "low":            low}

with open(filename, "a") as f:
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    if not file_exists:
        csv_writer.writeheader()
    csv_writer.writerow(write_line)

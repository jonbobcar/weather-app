# weather_plotter.py

import csv
import datetime
from bokeh.plotting import figure, output_file, save
import time
import math


def plotweather(file_name):

    # Open CSV data file
    with open(file_name, 'r') as f:
        csv_reader = csv.DictReader(f)
        csv_data = list(csv_reader)

    # Convert data from CSV file into lists
    year_data = []
    month_data = []
    day_data = []
    hour_data = []
    now_temp_data = []
    fcst_temp_data = []
    now_icon_data = []
    fcst_icon_data = []
    here_temp_data = []

    for line in csv_data:
        year_data.append(int(line['year']))
        month_data.append(int(line['month']))
        day_data.append(int(line['day']))
        hour_data.append(int(line['hour']))
        now_temp_data.append(float(line['now_temp']))
        fcst_temp_data.append(float(line['fcst_temp']))
        now_icon_data.append(line['now_icon'])
        fcst_icon_data.append(line['fcst_icon'])
        here_temp_data.append(line['here_temp'])

    # Remove forecast data from midnight to disconnect line on Bokeh plot each day
    for foo in range(len(hour_data)):
        # print(hour_data[foo])
        if hour_data[foo] == 0:
            fcst_temp_data[foo] = float('nan')

    # Convert data lists into preferred format for plotting
    date_conv = []
    day_str = []
    hour_str = []

    for hour in range(len(year_data)):
        date_time = datetime.datetime(year_data[hour], month_data[hour],
                                      day_data[hour], hour_data[hour])
        day_string = date_time.strftime('%m/%d/%Y')
        hour_string = date_time.strftime('%H:%M')
        day_str.append(day_string)
        hour_str.append(hour_string)
        date_time = time.mktime(date_time.timetuple())
        date_conv.append(int(date_time))

    # Plot data and save as HTML file
    file_output = 'weather_data.html'
    output_file(file_output)
    p = figure(
        title="Forecast Temperature vs. Reported Temperature",
        y_axis_label='Temperature (F)', y_range=[0, 100],
        # x_axis_type='datetime',
        # sizing_mode='stretch_width'
    )

    x_label_key = []
    x_label_val = []

    for lbl in range(len(date_conv)):
        if hour_str[lbl] in ('06:00', '12:00', '18:00'):
            x_label_key.append(date_conv[lbl])
            x_label_val.append(hour_str[lbl])
        elif hour_str[lbl] == '00:00':
            x_label_key.append(date_conv[lbl])
            x_label_val.append(day_str[lbl])

    x_labels = dict(zip(x_label_key, x_label_val))

    # Plot properties
    p.yaxis.ticker = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    p.xaxis.ticker = x_label_key
    p.xaxis.major_label_orientation = 3.14/3
    p.xaxis.major_label_overrides = x_labels
    p.below[0].formatter.use_scientific = False

    # p.circle(date_conv, now_temp_data, legend_label="Reported Temp.", line_width=2,
    #          fill_color='white', line_color='skyblue', size=6)
    # p.line(date_conv, fcst_temp_data, legend_label='Forecast Temp.', line_width=3,
    #        line_color='gray')
    # p.circle(date_conv, here_temp_data, legend_label='Garage Temp.', line_width=2,
    #          fill_color='white', line_color='brown', size=6)

    p.circle(date_conv, now_temp_data, legend_label="Reported Temp.", line_width=2,
             fill_color='white', line_color='skyblue', size=1)
    p.line(date_conv, fcst_temp_data, legend_label='Forecast Temp.', line_width=3,
           line_color='gray')
    p.circle(date_conv, here_temp_data, legend_label='Garage Temp.', line_width=2,
             fill_color='white', line_color='tomato', size=1)

    save(p, 'weather_data.html')


# plotweather('data_weather_thing.csv')

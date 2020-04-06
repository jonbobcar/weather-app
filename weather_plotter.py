# weather_plotter.py

import csv
import datetime
from bokeh.plotting import figure, output_file, save
from bokeh.models import tickers
import time


def plotweather(file_name):

    # Open CSV data file
    with open(file_name, 'r') as f:
        csv_reader = csv.DictReader(f)
        csv_data = list(csv_reader)

    # Convert data from CSV file into lists
    fcst_date_0_data = []
    # year_data = []
    # month_data = []
    # day_data = []
    # hour_data = []
    now_temp_data = []
    fcst_temp_0_data = []
    now_icon_data = []
    fcst_icon_0_data = []
    # here_temp_data = []
    fcst_temp_3_data = []
    fcst_date_3_data = []

    for line in csv_data:
        # year_data.append(int(line['year']))
        # month_data.append(int(line['month']))
        # day_data.append(int(line['day']))
        # hour_data.append(int(line['hour']))
        fcst_date_0_data.append(line['fcst_date_0'])
        now_temp_data.append(float(line['now_temp']))
        fcst_temp_0_data.append(float(line['fcst_temp_0']))
        now_icon_data.append(line['now_icon'])
        fcst_icon_0_data.append(line['fcst_icon_0'])
        # here_temp_data.append(line['here_temp'])
        fcst_temp_3_data.append(line['fcst_temp_3'])
        fcst_date_3_data.append(line['fcst_date_3'])


    # Remove forecast data from midnight to disconnect line on Bokeh plot each day
    for _ in fcst_date_0_data:
        # print(fcst_date_0_data[foo])
        if _ == 0:
            fcst_temp_0_data[_] = float('nan')

    # Convert data lists into preferred format for plotting
    date_conv = []
    day_str = []
    hour_str = []

    for hour in fcst_date_0_data:
        date_time = datetime.datetime.strptime(hour, '%Y-%m-%d %H:%M:%S')
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
        sizing_mode='stretch_width'
    )

    x_label_key = []
    x_label_val = []
    x_grids = []
    y_grids = [10, 20, 30, 40, 50, 60, 70, 80, 90]

    for lbl in range(len(date_conv)):
        if hour_str[lbl] in ('06:00', '12:00', '18:00'):
            x_label_key.append(date_conv[lbl])
            x_label_val.append(hour_str[lbl])
        elif hour_str[lbl] == '00:00':
            x_label_key.append(date_conv[lbl])
            x_label_val.append(day_str[lbl])
            x_grids.append(date_conv[lbl])

    x_labels = dict(zip(x_label_key, x_label_val))

    # Plot properties
    p.yaxis.ticker = y_grids
    p.xaxis.ticker = x_label_key
    p.xgrid.grid_line_dash = 'dotted'
    p.xaxis.major_label_orientation = 3.14/3
    p.xaxis.major_label_overrides = x_labels
    p.below[0].formatter.use_scientific = False
    p.xgrid.ticker = x_grids
    p.ygrid.ticker = y_grids

    p.circle(date_conv, now_temp_data, legend_label="Reported Temp.", line_width=2,
             fill_color='white', line_color='skyblue', size=4)
    p.line(date_conv, fcst_temp_0_data, legend_label='Forecast Temp.', line_width=3,
           line_color='gray')
    # p.circle(date_conv, here_temp_data, legend_label='Garage Temp.', line_width=2,
    #          fill_color='white', line_color='tomato', size=4)

    save(p, 'weather_data.html')


if __name__ == '__main__':
    plotweather('data_weather_thing.csv')

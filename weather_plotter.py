# weather_plotter.py

import csv
import datetime
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, LabelSet
import time


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

    for line in csv_data[-(24*30)::]:
        year_data.append(int(line['year']))
        month_data.append(int(line['month']))
        day_data.append(int(line['day']))
        hour_data.append(int(line['hour']))
        now_temp_data.append(float(line['now_temp']))
        fcst_temp_data.append(float(line['fcst_temp']))
        now_icon_data.append(line['now_icon'])
        fcst_icon_data.append(line['fcst_icon'])

    # Remove forecast data from midnight to disconnect line on Bokeh plot each day
    for _ in range(len(hour_data)):
        # print(hour_data[_])
        if hour_data[_] == 0:
            fcst_temp_data[_] = float('nan')

    file_name = "3_day_fcst.csv"

    with open(file_name, 'r') as f:
        csv_reader = csv.DictReader(f)
        csv_data = list(csv_reader)

    fcst_high_days = []
    fcst_low_days = []
    fcst_high_data = []
    fcst_low_data = []
    fcst_day_detail = []

    for line in csv_data[-33::]:
        split_date = [int(e) if e.isdigit() else e for e in line["fcst_date"].split('-')]
        fcst_high_days.append(split_date)
        fcst_low_days.append(split_date)
        fcst_high_data.append(int(line["high"]))
        fcst_low_data.append(int(line["low"]))
        fcst_day_detail.append(line["day_detail"])

    fcst_high_interval = []
    fcst_low_interval = []
    hourly_high_data = []
    hourly_low_data = []
    fcst_detail_interval = []

    for day in fcst_high_data:
        for _ in range(0,3):
            hourly_high_data.append(day)

    for day in fcst_low_data:
        for _ in range(0,3):
            hourly_low_data.append(day)

    for day in fcst_high_days:
        fcst_high_interval.append(
            time.mktime(datetime.datetime(day[0], day[1], day[2], 1).timetuple()))
        fcst_high_interval.append(
            time.mktime(datetime.datetime(day[0], day[1], day[2], 22, 59, 59).timetuple()))
        fcst_high_interval.append(float("nan"))
        fcst_detail_interval.append(time.mktime(datetime.datetime(day[0], day[1], day[2], 1).timetuple()))

    for day in fcst_low_days:
        fcst_low_interval.append(
            time.mktime(datetime.datetime(day[0], day[1], day[2], 1).timetuple()) + 43200)
        fcst_low_interval.append(
            time.mktime(datetime.datetime(day[0], day[1], day[2], 22, 59, 59).timetuple()) + 43200)
        fcst_low_interval.append(float("nan"))

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

    source = ColumnDataSource(data=dict(interval=[fcst_detail_interval],data=[fcst_high_data],detail=[fcst_day_detail]))

    day_labels = LabelSet(x="interval", y="data", text="detail", level="glyph",
                          x_offset=0, y_offset=0, source=source, render_mode="canvas")

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
             fill_color='white', line_color='gray', size=4)
    p.line(fcst_high_interval, hourly_high_data, line_width=3, line_color="orange",
           legend_label="3 Day High")
    p.line(fcst_low_interval, hourly_low_data, line_width=3, line_color="skyblue",
           legend_label="3 Day Low")
    p.add_layout(day_labels)
    p.scatter(x="interval", y="data", source=source, size=8)

    save(p, 'weather_data.html')


if __name__ == '__main__':
    plotweather('data_weather_thing.csv')

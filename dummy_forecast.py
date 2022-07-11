import forecast
import math
import utmconvert as utm
import numpy as np

# The purpose of this file is to create dummy weather data for tuning.


def dummy_create_weather_grid(grid_base, resolution, start_node, wind_angle, wind_speed, wave_angle, wave_height, current_angle, current_speed):
    print("Collecting weather data...")
    weather_grid = []
    for row in grid_base:
        for node in row:

            # time estimate can be made more accurate w. a proper speed estimator
            delta_x = abs(start_node.grid_index[0]-node.grid_index[0])
            delta_y = abs(start_node.grid_index[1]-node.grid_index[1])
            max_dist = max(delta_x, delta_y)

            # distance over speed (time) in hours
            time_scalar = (2500/0.514)/3600
            time_estimate_hours = int(time_scalar*max_dist)
            #print("Time estimate: ", time_estimate_hours)

            lat_utm = node.box_object.centroid.x
            long_utm = node.box_object.centroid.y
            long, lat = utm.utm_to_lat_lon('33N', lat_utm, long_utm)

            wind_angle = wind_angle
            wind_speed = wind_speed
            wave_angle = wave_angle
            #print("Wave angle: ", wave_angle)

            wave_height = wave_height

            current_angle = current_angle
            current_speed = current_speed

            weather_grid.append(node)
            weather_grid.append(wind_angle)
            weather_grid.append(wind_speed)
            weather_grid.append(wave_angle)
            weather_grid.append(wave_height)
            weather_grid.append(current_angle)
            weather_grid.append(current_speed)

    # 7 is the number of objects in each grid cell, i.e. the node object and each weather param.
    weather_grid_2d = np.reshape(weather_grid, (resolution, resolution, 7))
    #print(weather_grid_2d)
    return weather_grid_2d


def dummy_drawWindAtPoint(enc, east, north, time, wind_angle, wind_speed):
    #long, lat = utm.utm_to_lat_lon('33N', east, north)
    windAngle = wind_angle
    windSpeed = wind_speed

    # adjust hypotenuse according to preference
    hypotenuse = 300

    # Good ole Pythagoras
    adjacent = hypotenuse*math.cos(math.radians(windAngle))
    opposite = hypotenuse*math.sin(math.radians(windAngle))

    if windSpeed > 15:
        vector_color = 'red'
    elif windSpeed > 10:
        vector_color = 'orange'
    elif windSpeed > 5:
        vector_color = 'yellow'
    else:
        vector_color = 'green'

    enc.draw_arrow((east, north), (east - opposite, north - adjacent), vector_color,
                  head_size=8, width=10, thickness=2)

    return 0


def dummy_drawWindGrid(enc, grid, time, wind_angle, wind_speed):
    print("Collecting wind data...")
    for row in grid:
        for node in row:
            #and not node.box_object.intersects(enc.land.geometry)
            if node.grid_index[0] % 1 == 0 and node.grid_index[1] % 1 == 0:
                #print("Grid index: ", node.grid_index[0], node.grid_index[1])
                lat = node.box_object.centroid.x
                long = node.box_object.centroid.y
                #print("(lat,long): ", lat, long)
                dummy_drawWindAtPoint(enc, lat, long, time, wind_angle, wind_speed)

    return 0


def dummy_drawCurrentAtPoint(enc, east, north, time, current_angle, current_speed):
    long, lat = utm.utm_to_lat_lon('33N', east, north)

    currentAngle = current_angle
    currentSpeed = current_speed

    # arrow length; adjust according to preference
    hypotenuse = 300

    # Good ole Pythagoras
    adjacent = hypotenuse*math.cos(math.radians(currentAngle))
    opposite = hypotenuse*math.sin(math.radians(currentAngle))

    # TODO: change into color spectrum?
    if currentSpeed > 2:
        vector_color = 'red'
    elif currentSpeed > 1:
        vector_color = 'orange'
    elif currentSpeed > 0.5:
        vector_color = 'yellow'
    else:
        vector_color = 'green'

    enc.draw_arrow((east - opposite, north - adjacent), (east, north), vector_color,
                   head_size=15, width=10, thickness=1.5)

    return 0


def dummy_drawCurrentGrid(enc, grid, time, current_angle, current_speed):
    print("Collecting current data...")
    for row in grid:
        for node in row:
            #and not node.box_object.intersects(enc.land.geometry)
            if node.grid_index[0] % 1 == 0 and node.grid_index[1] % 1 == 0:
                #print("Grid index: ", node.grid_index[0], node.grid_index[1])
                lat = node.box_object.centroid.x
                long = node.box_object.centroid.y
                #print("(lat,long): ", lat, long)
                dummy_drawCurrentAtPoint(enc, lat, long, time, current_angle, current_speed)

    return 0


def dummy_drawWaveAtPoint(enc, east, north, time, wave_angle, wave_height):
    long, lat = utm.utm_to_lat_lon('33N', east, north)
    #print("Long: ", long)
    #print("Lat: ", lat)
    waveAngle = wave_angle
    waveHeight = wave_height

    # arrow length; adjust according to preference
    #original: 300
    hypotenuse = 300

    # Good ole Pythagoras
    adjacent = hypotenuse*math.cos(math.radians(waveAngle))
    opposite = hypotenuse*math.sin(math.radians(waveAngle))

    if waveHeight > 11:
        vector_color = 'red'
    elif waveHeight > 3.9:
        vector_color = 'orange'
    elif waveHeight > 1.9:
        vector_color = 'yellow'
    else:
        vector_color = 'green'

    enc.draw_arrow((east, north), (east - opposite, north - adjacent), vector_color,
                   head_size=8, width=10, thickness=2)

    return 0


def dummy_drawWaveGrid(enc, grid, time, wave_angle, wave_height):
    print("Collecting wave data...")
    for row in grid:
        for node in row:
            #and not node.box_object.intersects(enc.land.geometry)
            if node.grid_index[0] % 1 == 0 and node.grid_index[1] % 1 == 0:
                #print("Grid index: ", node.grid_index[0], node.grid_index[1])
                lat = node.box_object.centroid.x
                long = node.box_object.centroid.y
                #print("(lat,long): ", lat, long)
                dummy_drawWaveAtPoint(enc, lat, long, time, wave_angle, wave_height)

    return 0
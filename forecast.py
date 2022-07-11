from pprint import pprint
import json
import requests
import seacharts
import numpy as np
import matplotlib.pyplot as plt
import math
import utmconvert as utm
import numpy as np



def getWindAngle(east, north, time):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    r = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=%s&lon=%s' % (north, east), headers=headers)

    jsonResponse = r.json()

    windAngle = jsonResponse["properties"]["timeseries"][0]["data"]["instant"]["details"]["wind_from_direction"]
    #print(windAngle)
    return windAngle


def getWindSpeed(east, north, time):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    r = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=%s&lon=%s' % (north, east), headers=headers)

    jsonResponse = r.json()
    #pprint(jsonResponse)

    windSpeed = jsonResponse["properties"]["timeseries"][time]["data"]["instant"]["details"]["wind_speed"]
    #print("Wind speed: ", windSpeed)
    return windSpeed


def getCurrentAngle(east, north, time):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    r = requests.get('https://api.met.no/weatherapi/oceanforecast/2.0/complete?lat=%s&lon=%s' % (north, east), headers=headers)

    jsonResponse = r.json()
    #pprint(jsonResponse)

    max_time = 202
    if time > max_time:
        print("Time: ", time)
        real_time = max_time
    else:
        real_time = time

    try:
        currentAngle = jsonResponse["properties"]["timeseries"][real_time]["data"]["instant"]["details"]["sea_water_to_direction"]
    except IndexError:
        print("Index error")
        currentAngle = 0
    #print("Current angle: ", currentAngle)
    return currentAngle


def getCurrentSpeed(east, north, time):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    r = requests.get('https://api.met.no/weatherapi/oceanforecast/2.0/complete?lat=%s&lon=%s' % (north, east), headers=headers)
    #pprint(r.json())

    jsonResponse = r.json()
    #pprint(jsonResponse)

    max_time = 202
    if time > max_time:
        print("Time: ", time)
        real_time = max_time
    else:
        real_time = time

    try:
        currentSpeed = jsonResponse["properties"]["timeseries"][real_time]["data"]["instant"]["details"]["sea_water_speed"]
    except IndexError:
        print("Index error")
        currentSpeed = 0

    #print("Current speed: ", currentSpeed)
    return currentSpeed


def getWaveHeight(east, north, time):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    r = requests.get('https://api.met.no/weatherapi/oceanforecast/2.0/complete?lat=%s&lon=%s' % (north, east), headers=headers)

    jsonResponse = r.json()

    max_time = 202
    if time > max_time:
        print("Time: ", time)
        real_time = max_time
    else:
        real_time = time

    try:
        waveHeight = jsonResponse["properties"]["timeseries"][real_time]["data"]["instant"]["details"]["sea_surface_wave_height"]
    except IndexError:
        print("Index error")
        waveHeight = 0

    return waveHeight


def getWaveAngle(east, north, time):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    r = requests.get('https://api.met.no/weatherapi/oceanforecast/2.0/complete?lat=%s&lon=%s' % (north, east), headers=headers)

    jsonResponse = r.json()
    #pprint(jsonResponse)

    max_time = 202
    if time > max_time:
        print("Time: ", time)
        real_time = max_time
    else:
        real_time = time

    try:
        waveAngle = jsonResponse["properties"]["timeseries"][real_time]["data"]["instant"]["details"]["sea_surface_wave_from_direction"]
    except IndexError:
        print("Index error")
        waveAngle = 0

    return waveAngle


#  draws wind vector in enc object at specified coordinates
def drawWindAtPoint(enc, east, north, time):
    long, lat = utm.utm_to_lat_lon('33N', east, north)
    #print("Long: ", long)
    #print("Lat: ", lat)
    windAngle = getWindAngle(long, lat, time)
    windSpeed = getWindSpeed(long, lat, time)

    # adjust hypotenuse according to preference
    hypotenuse = 300

    # Good ole Pythagoras
    adjacent = hypotenuse*math.cos(math.radians(windAngle))
    opposite = hypotenuse*math.sin(math.radians(windAngle))

    if windSpeed > 15:
        vector_color = 'red'
    elif windSpeed > 5:
        vector_color = 'orange'
    elif windSpeed > 3:
        vector_color = 'yellow'
    else:
        vector_color = 'green'

    enc.draw_arrow((east, north), (east - opposite, north - adjacent), vector_color,
                  head_size=8, width=10, thickness=2)

    return 0


def drawCurrentAtPoint(enc, east, north, time):
    long, lat = utm.utm_to_lat_lon('33N', east, north)

    try:
        currentAngle = getCurrentAngle(long, lat, time)
        currentSpeed = getCurrentSpeed(long, lat, time)

        # adjust hypotenuse according to preference
        hypotenuse = 300

        # Good ole Pythagoras
        adjacent = hypotenuse * math.cos(math.radians(currentAngle))
        opposite = hypotenuse * math.sin(math.radians(currentAngle))

        if currentSpeed > 2:
            vector_color = 'blue'
        elif currentSpeed > 1:
            vector_color = 'cornflowerblue'
        elif currentSpeed > 0.5:
            vector_color = 'turquoise'
        else:
            vector_color = 'cyan'

        enc.draw_arrow((east - opposite, north - adjacent), (east, north), vector_color,
                   head_size=15, width=10, thickness=1.5)

        return 0

    except:
        print("No data")
        return 0


def drawWaveAtPoint(enc, east, north, time):
    long, lat = utm.utm_to_lat_lon('33N', east, north)

    waveAngle = getWaveAngle(long, lat, time)
    waveHeight = getWaveHeight(long, lat, time)

    # adjust hypotenuse according to preference
    hypotenuse = 200

    # Good ole Pythagoras
    adjacent = hypotenuse*math.cos(math.radians(waveAngle))
    opposite = hypotenuse*math.sin(math.radians(waveAngle))

    print("Wave height: ", waveHeight)
    if waveHeight > 11:
        vector_color = 'red'
    elif waveHeight > 5:
        vector_color = 'darkorange'
    elif waveHeight > 3:
        vector_color = 'orange'
    elif waveHeight > 2.4:
        vector_color = 'gold'
    elif waveHeight > 2:
        vector_color = 'yellow'
    elif waveHeight > 1:
        vector_color = 'green'
    elif waveHeight > 0.7:
        vector_color = 'green'
    elif waveHeight > 0.5:
        vector_color = 'forestgreen'
    else:
        vector_color = 'limegreen'

    enc.draw_arrow((east, north), (east - opposite, north - adjacent), vector_color,
                   head_size=8, width=10, thickness=2)

    return 0


def drawWindGrid(enc, grid, time):
    print("Collecting wind data...")
    for row in grid:
        for node in row:
            #add this to if expression if you don't like to draw on land
            #and not node.box_object.intersects(enc.land.geometry)
            if node.grid_index[0] % 3 == 0 and node.grid_index[1] % 3 == 0:
                lat = node.box_object.centroid.x
                long = node.box_object.centroid.y
                drawWindAtPoint(enc, lat, long, time)


def drawCurrentGrid(enc, grid, time):
    print("Collecting current data...")
    for row in grid:
        for node in row:
            if node.grid_index[0] % 12 == 0 and node.grid_index[1] % 12 == 0 and \
                    not node.box_object.intersects(enc.land.geometry):
                lat = node.box_object.centroid.x
                long = node.box_object.centroid.y
                drawCurrentAtPoint(enc, lat, long, time)


def drawWaveGrid(enc, grid, time):
    print("Collecting wave data...")
    for row in grid:
        for node in row:
            # add this to if expression if you don't like to draw on land
            #and not node.box_object.intersects(enc.land.geometry)
            if node.grid_index[0] % 3 == 0 and node.grid_index[1] % 3 == 0:
                lat = node.box_object.centroid.x
                long = node.box_object.centroid.y
                drawWaveAtPoint(enc, lat, long, time)


def draw_distance_grid(grid_base, start_node, enc):
    print("Drawing distance grid...")
    for row in grid_base:
        for node in row:
            # time estimate can be made more accurate w. a proper speed estimator
            delta_x = abs(start_node.grid_index[0] - node.grid_index[0])
            delta_y = abs(start_node.grid_index[1] - node.grid_index[1])
            max_dist = max(delta_x, delta_y)

            # distance over speed (time) in hours
            time_scalar = (2500 / 0.514) / 3600
            time_estimate_hours = int(time_scalar * max_dist)
            print("Time estimate: ", time_estimate_hours)

            if max_dist == 0:
                color = 'green'
            elif 0 < max_dist < 2:
                color = 'yellow'
            elif 1 < max_dist < 4:
                color = 'orange'
            else:
                color = 'red'

            enc.draw_polygon(node.box_object, color, fill=True)

    return 0


def create_weather_grid(grid_base, resolution, start_node):
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

            wind_angle = getWindAngle(long, lat, time_estimate_hours)
            wind_speed = getWindSpeed(long, lat, time_estimate_hours)
            wave_angle = getWaveAngle(long, lat, time_estimate_hours)
            #print("Wave angle: ", wave_angle)
            wave_height = getWaveHeight(long, lat, time_estimate_hours)
            #print("Wave height:", wave_height)
            current_angle = getCurrentAngle(long, lat, time_estimate_hours)
            #print("Current angle: ", current_angle)
            current_speed = getCurrentSpeed(long, lat, time_estimate_hours)
            #print("Current speed: ", current_speed)

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


def weather_cost(enc, movement_grid, weather_grid, current_node_index, neighbor_node_index):

    current_node = movement_grid[current_node_index[0]][current_node_index[1]]
    neighbor_node = movement_grid[neighbor_node_index[0]][neighbor_node_index[1]]

    east_movement = neighbor_node_index[0] - current_node_index[0]
    north_movement = neighbor_node_index[0] - current_node_index[0]
    # TODO: replace ownship_angle with real angle from compass
    ownship_angle = math.degrees(math.atan(north_movement/(east_movement+0.0001)))
    #print("Ownship angle between nodes ", current_node_index, " and ", neighbor_node_index, ': ',  ownship_angle)

    weather_cell = None
    done = False
    while not done:
        for row in weather_grid:
            for cell in row:
                if neighbor_node.box_object.intersects(cell[0].box_object):
                    weather_cell = cell
                    done = True


    #wind cost
    wind_angle = weather_cell[1]

    wind_angle_scalar = 0.001
    wind_angle_cost = wind_angle_scalar*abs(wind_angle - ownship_angle)

    wind_speed = weather_cell[2]
    wind_speed_scalar = 0.001
    wind_speed_cost = wind_speed_scalar*wind_speed
    wind_cost = wind_angle_cost + wind_speed_cost

    # wave cost
    wave_angle = weather_cell[3]
    wave_height = weather_cell[4]

    if 0.1 < wave_height < 2.5:
        wave_angle_scalar = 0
    else:
        wave_angle_scalar = 0.2

    wave_angle_cost = wave_angle_scalar * abs(math.sin(wave_angle) - math.sin(ownship_angle))

    if wave_height < 0.1:
        wave_height_scalar = 0.05
    elif 0.1 < wave_height < 2.5:
        wave_height_scalar = 0
    else:
        wave_height_scalar = 0.05

    wave_height_cost = wave_height_scalar * wave_height

    wave_cost = wave_angle_cost + wave_height_cost

    # current cost
    current_angle = weather_cell[5]
    current_angle_scalar = 0.001
    current_angle_cost = current_angle_scalar * abs(math.sin(current_angle) - math.sin(ownship_angle))

    current_speed = weather_cell[6]
    current_speed_scalar = 0.001
    current_speed_cost = current_speed_scalar * current_speed
    current_cost = current_angle_cost + current_speed_cost
    #print("Current cost: ", current_cost)

    cost = wind_cost + wave_cost + current_cost

    return cost






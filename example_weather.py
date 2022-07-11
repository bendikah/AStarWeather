import seacharts
import AStar
import AStarWeather
import node
import forecast
import dummy_forecast
import utmconvert
import utmconvert as utm
import utilities
from shapely.geometry import Point
import time


# Example script for using the AStarWeather algorithm
# Big ass map, takes forever to collect weather

if __name__ == '__main__':

    start_time = time.time()

    size = 15000, 15000       # w, h (east, north) size of map, distance in meters
    center = 215050, 7125575  # Frohavet north-east
    center_coords = utmconvert.utm_to_lat_lon('33N', center[0], center[1])
    resolution = 50           # number of nodes for each side of map

    node_size = size[0] / resolution, size[1] / resolution  # size in meters of each grid cell
    corner_point = center[0] - size[0] / 2, center[1] - size[1] / 2  # bottom left corner point of map

    # coords used to generate front page
    start_coords = center[0] + 2500, center[1] - 2000
    end_coords = center[0] - 5000, center[1] + 2800

    # make start, end points
    start_point = Point(start_coords[0], start_coords[1])
    end_point = Point(end_coords[0], end_coords[1])

    files = ['Basisdata_50_Trondelag_25833_Dybdedata_FGDB.gdb']  # Norwegian county database name
    enc = seacharts.ENC(size=size, center=center, files=files, new_data=False)  # enc object

    # movement grid and weather grid
    grid = node.create_grid(resolution, corner_point, node_size)
    start_node = node.get_start_node(grid, start_point, end_point)
    end_node = node.get_end_node(grid, start_point, end_point)

    weather_resolution = 2500
    weather_grid_size = int(size[0]/weather_resolution)

    weather_grid_base = node.create_grid(7, corner_point, (2500, 2500))
    weather_grid = forecast.create_weather_grid(weather_grid_base, 7, start_node)

    path1 = AStarWeather.AStarAlgorithm(start_node, end_node, grid, weather_grid, enc)  # gives nodes we need to visit
    print("Length original path: ", len(path1)*node_size[0])

    # naive pruning
    pruned_path1 = utilities.prune(enc, path1, 100)
    print("Length pruned path: ", len(pruned_path1)*node_size[0])

    # draw path and wave grid
    AStarWeather.draw_line_path(start_point, end_point, path1, enc, 'white')
    #forecast.drawWindGrid(enc, grid, 0)
    #forecast.drawCurrentGrid(enc, grid, 0)
    forecast.drawWaveGrid(enc, grid, 0)

    shore_buffer = enc.shore.geometry.buffer(200)
    land_buffer = enc.land.geometry.buffer(200)
    enc.draw_polygon(shore_buffer, 'orange')
    enc.draw_polygon(land_buffer, 'red')

    print("My program took", time.time() - start_time, "s to run")

    #enc.save_image("example_weather")

    enc.show_display()


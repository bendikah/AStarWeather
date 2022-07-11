import seacharts
import AStar
import node
from shapely.geometry import Point
import time

#Script to create a small mission in a rough triangle shape.
#This script uses the original A* algorithm, not the weather one

if __name__ == '__main__':
    start_time = time.time()

    size = 10000, 10000       # w, h (east, north) size of map, distance in meters
    center = 213479, 7094395  # middle of Frohavet
    resolution = 10           # number of nodes for each side of map

    node_size = size[0] / resolution, size[1] / resolution  # size in meters of each grid cell
    corner_point = center[0] - size[0] / 2, center[1] - size[1] / 2  # bottom left corner point of map

    # middle of Frohavet low res start, end coordinates
    start_coords = center[0] + 3400, center[1] - 3400
    end_coords = center[0] - 3400, center[1] + 3500

    start_coords2 = end_coords
    end_coords2 = center[0] + 2000, center[1] + 4000

    start_coords3 = end_coords2
    end_coords3 = start_coords

    # make start, end points
    start_point = Point(start_coords[0], start_coords[1])
    end_point = Point(end_coords[0], end_coords[1])

    start_point2 = Point(start_coords2[0], start_coords2[1])
    end_point2 = Point(end_coords2[0], end_coords2[1])

    start_point3 = Point(start_coords3[0], start_coords3[1])
    end_point3 = Point(end_coords3[0], end_coords3[1])

    files = ['Basisdata_50_Trondelag_25833_Dybdedata_FGDB.gdb']  # Norwegian county database name
    enc = seacharts.ENC(size=size, center=center, files=files, new_data=True)  # enc object

    # 2D array consisting of Node objects
    grid = node.create_grid(resolution, corner_point, node_size)
    grid2 = node.create_grid(resolution, corner_point, node_size)
    grid3 = node.create_grid(resolution, corner_point, node_size)

    # draw grid on map
    node.draw_grid(enc, grid)

    # assign start and end nodes
    start_node = node.get_start_node(grid, start_point, end_point)
    end_node = node.get_end_node(grid, start_point, end_point)

    start_node2 = node.get_start_node(grid2, start_point2, end_point2)
    end_node2 = node.get_end_node(grid2, start_point2, end_point2)

    start_node3 = node.get_start_node(grid3, start_point3, end_point3)
    end_node3 = node.get_end_node(grid3, start_point3, end_point3)

    # generate paths
    path1 = AStar.AStarAlgorithm(start_node, end_node, grid, enc)  # gives nodes we need to visit
    path2 = AStar.AStarAlgorithm(start_node2, end_node2, grid2, enc)
    path3 = AStar.AStarAlgorithm(start_node3, end_node3, grid3, enc)

    # draw paths
    AStar.draw_line_path(start_point, end_point,   path1, enc, 'white')
    AStar.draw_line_path(start_point2, end_point2, path2, enc, 'red')
    AStar.draw_line_path(start_point3, end_point3, path3, enc,  'green')

    # save the image as png
    # enc.save_image("triangular_mission")

    print("My program took", time.time() - start_time, "to run")

    enc.show_display()

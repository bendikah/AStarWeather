from shapely.geometry import box
import shapely.geometry
import math
import numpy as np

# Node object containing the shapely box, f, g, grid index and parent node coordinates


class Node:
    def __init__(self, box_object, f, g, grid_index, parent):
        self.box_object = box_object
        self.f = f
        self.g = g
        self.grid_index = grid_index
        self.parent = parent

    def __eq__(self, other):
        return self.grid_index == other.grid_index


# create nxn box object b, use it to generate a Node object, add Node object to node list, reshape to grid
def create_grid(resolution, corner_point, node_size):
    nodes = []
    for i in range(resolution):
        for j in range(resolution):
            # don't think about why it works, it just does
            b = box(corner_point[0] + j * node_size[0], corner_point[1] + i * node_size[1],
                    corner_point[0] + node_size[0] + j*node_size[0], corner_point[1] + node_size[1] + i * node_size[1])

            node = Node(b, 0, 0, (i, j), (math.inf, math.inf))  # init parent to inf
            nodes.append(node)

    nodes2d = np.reshape(nodes, (resolution, resolution))  # make 1D list into 2D grid

    return nodes2d


# draws grid on the enc object
def draw_grid(enc, grid):
    shore_buffer = enc.shore.geometry.buffer(200)
    land_buffer = enc.land.geometry.buffer(200)

    for row in grid:
        for cell in row:
            if cell.box_object.intersects(land_buffer) or cell.box_object.intersects(shore_buffer):
                # draw land, shore nodes
                #enc.draw_polygon(cell.box_object, 'red', fill=True)
                pass
            else:
                # draw ocean nodes
                enc.draw_polygon(cell.box_object, 'cyan', fill=False)
                pass


def get_start_node(grid, start_point, end_point):
    start_node = None
    distance = math.inf
    for row in grid:
        for cell in row:
            if cell.box_object.intersects(start_point):  # candidate for start point
                intersecting_node = cell
                # enc.draw_polygon(cell.box_object, 'magenta', fill=True)
                new_distance = intersecting_node.box_object.distance(end_point)
                if new_distance < distance:  # selected node is the closest to end point
                    distance = new_distance
                    start_node = intersecting_node

    return start_node


def get_end_node(grid, start_point, end_point):
    end_node = None
    distance = math.inf
    for row in grid:
        for cell in row:
            if cell.box_object.intersects(end_point):  # candidate for end point
                intersecting_node = cell
                # enc.draw_polygon(cell.box_object, 'magenta', fill=True)
                new_distance = intersecting_node.box_object.distance(start_point)
                if new_distance < distance:  # selected node is the closest to start point
                    distance = new_distance
                    end_node = intersecting_node
    return end_node

import math
import forecast


def AStarAlgorithm(start_node, end_node, grid, weather_grid, enc):
    print("Starting A* algorithm...")
    # Check if start or end nodes are valid
    if not is_valid_node(start_node, enc) or not is_valid_node(end_node, enc):
        print("Invalid node")
        return False

    open_list = []  # list of nodes in the optimal path, from start to end
    closed_list = []
    start_node.g = 0
    start_node.f = start_node.g + heuristic(start_node, end_node)
    start_node.parent = None
    open_list.append(start_node)

    while open_list:
        lowest_f = 0
        for i in range(len(open_list)):
            if open_list[i].f < open_list[lowest_f].f:
                lowest_f = i

        current = open_list[lowest_f]

        if current == end_node:
            print("Goal!")
            return reconstruct_path(start_node, current)

        open_list.remove(current)
        closed_list.append(current)

        for neighbor in weatherNeighborNodes(current.grid_index, grid, weather_grid, enc, current):
            if neighbor not in closed_list:
                neighbor.f = neighbor.g + heuristic(neighbor, end_node) # TODO: experiment with decreasing heuristic
                if neighbor not in open_list:
                    open_list.append(neighbor)
                else:
                    open_neighbor = [n for n in open_list if n.grid_index == neighbor.grid_index][0]
                    if neighbor.g < open_neighbor.g:
                        open_neighbor.g = neighbor.g
                        open_neighbor.parent = current
    return False  # no feasible path

# Checks if node is valid
def is_valid_node(node, enc):
    shore_buffer = enc.shore.geometry.buffer(200)
    land_buffer = enc.land.geometry.buffer(200)

    if node.box_object.intersects(land_buffer) \
    or node.box_object.intersects(shore_buffer):
        print("Invalid node!")
        return False
    return True


# Constructs a list of all nodes in the optimal path from start to end node
def reconstruct_path(start_node, end_node):
    print("Reconstructing path...")
    path = []
    node = end_node

    while node.parent:
        path.append(node)
        node = node.parent

    path.append(start_node)
    return path


# draw the path constructed by construct_path in nodes
def draw_node_path(path, enc):
    print("Drawing path...")
    point_list = []
    for node in path:
        waypoint = node.box_object.centroid.x, node.box_object.centroid.y
        enc.draw_circle(waypoint, 50, 'white', thickness=2, fill=True)
        point_list.append(waypoint)
        # enc.draw_polygon(node.box_object, 'white', fill=True) draw the boxes themselves
    for i in range(len(point_list)-1):
        enc.draw_line([point_list[i], point_list[i+1]], 'white')


# draw the path constructed by construct_path in lines
def draw_line_path(start_point, end_point, path, enc, color):
    print("Drawing path...")
    point_list = []
    start_x, start_y = start_point.x, start_point.y
    end_x, end_y = end_point.x, end_point.y
    enc.draw_circle([start_x, start_y], 50, 'snow', fill=True)
    enc.draw_circle([end_x, end_y], 100, 'green', fill=True)
    path_copy = path[1:-1]

    for node in path_copy:
        waypoint = node.box_object.centroid.x, node.box_object.centroid.y
        # enc.draw_circle(waypoint, 50, 'snow', fill=True)
        point_list.append(waypoint)

    # switch out first and last with real points
    point_list.insert(0, (end_x, end_y))
    point_list.append((start_x, start_y))

    for i in range(0, len(point_list)-1):
        enc.draw_line([point_list[i], point_list[i+1]], color)


# euclidean distance
def heuristic(start_node, end_node): # square root is expensive!
    h = math.sqrt((start_node.grid_index[0] - end_node.grid_index[0])**2
                 + (start_node.grid_index[1] - end_node.grid_index[1])**2)
    return h


# euc distance squared
# def heuristic(start_node, end_node):
#    h2 = ((start_node.grid_index[0] - end_node.grid_index[0])**2
#        + (start_node.grid_index[1] - end_node.grid_index[1])**2)
#    return h2

# manhattan distance
# def heuristic(start_node, end_node):
#    h = abs(start_node.grid_index[0] - end_node.grid_index[0]) \
#        + abs(start_node.grid_index[1] - end_node.grid_index[1])
#    return h

# number of steps
# def heuristic(start_node, end_node):
#    h = max(abs(start_node.grid_index[0] - end_node.grid_index[0]),
#            abs(start_node.grid_index[1] - end_node.grid_index[1]))
#    print("h: ", h)
#    return h

# Function to find the valid neighbor nodes of a specific node,
    # and the cost of moving to that node (g-cost).
    # where node_index = (i, j)
    # node_grid is a 2d list containing the node grid
def weatherNeighborNodes(node_index, node_grid, weather_grid, enc, current_node):
    neighbors = []
    radial_cost = 0.5 # cost of moving normally
    diagonal_cost = 0.55  # cost of moving diagonally
    west_node = east_node = north_node = south_node = None
    north_west_node = north_east_node = south_west_node = south_east_node = None

    shore_buffer = enc.shore.geometry.buffer(200)
    land_buffer = enc.land.geometry.buffer(200)

    # check surrounding nodes if it is possible to move there
    # first check NSWE
    if node_index[1] != 0:
        west_node_index = (node_index[0], node_index[1] - 1)
        west_node = node_grid[west_node_index[0]][west_node_index[1]]
        west_box = west_node.box_object
        if west_box.intersects(land_buffer) or west_box.intersects(shore_buffer):
            # enc.draw_polygon(west_box, 'black', fill=True)
            # print("Land to the West!")
            pass
        else:
            neighbors.append(west_node)
    else:
        print("We are on the Western border!")

    try:
        east_node_index = (node_index[0], node_index[1] + 1)
        east_node = node_grid[east_node_index[0]][east_node_index[1]]
        east_box = east_node.box_object
        if east_box.intersects(land_buffer) or east_box.intersects(shore_buffer):
            # enc.draw_polygon(east_box, 'black', fill=True)
            # print("Land to the East!")
            pass
        else:
            neighbors.append(east_node)
    except:
        print("We are on the Eastern border!")

    try:
        north_node_index = (node_index[0] + 1, node_index[1])
        north_node = node_grid[north_node_index[0]][north_node_index[1]]
        north_box = north_node.box_object
        if north_box.intersects(land_buffer) or north_box.intersects(shore_buffer):
            # enc.draw_polygon(north_box, 'black', fill=True)
            # print("Land to the North!")
           pass
        else:
            neighbors.append(north_node)
    except:
        print("We are on the Northern border!")

    try:
        south_node_index = (node_index[0] - 1, node_index[1])
        south_node = node_grid[south_node_index[0]][south_node_index[1]]
        south_box = south_node.box_object
        if south_box.intersects(land_buffer) or south_box.intersects(shore_buffer):
            # enc.draw_polygon(south_box, 'black', fill=True)
            # print("Land to the South!")
            pass
        else:
            neighbors.append(south_node)
    except:
        print("We are on the Southern border!")

    # now we check the diagonals:
    if node_index[0] != 0 and node_index[1] != 0:
        south_west_node_index = (node_index[0] - 1, node_index[1] - 1)
        south_west_node = node_grid[south_west_node_index[0]][south_west_node_index[1]]
        south_west_box = south_west_node.box_object
        if south_west_box.intersects(land_buffer) or south_west_box.intersects(shore_buffer):
            # enc.draw_polygon(south_west_box, 'black', fill=True)
            # print("Land to the South West!")
            pass
        else:
            neighbors.append(south_west_node)
    else:
        print("South-West is outside the grid!")

    try:
        south_east_node_index = (node_index[0] - 1, node_index[1] + 1)
        south_east_node = node_grid[south_east_node_index[0]][south_east_node_index[1]]
        south_east_box = south_east_node.box_object
        if south_east_box.intersects(land_buffer) or south_east_box.intersects(shore_buffer):
            # enc.draw_polygon(south_east_box, 'black', fill=True)
            # print("Land to the South East!")
            pass
        else:
            neighbors.append(south_east_node)
    except:
        print("South-East is outside the grid!")

    if node_index[0] != 0 and node_index[1] != 0:
        north_west_node_index = (node_index[0] + 1, node_index[1] - 1)
        north_west_node = node_grid[north_west_node_index[0]][north_west_node_index[1]]
        north_west_box = north_west_node.box_object
        if north_west_box.intersects(land_buffer) or north_west_box.intersects(shore_buffer):
            # enc.draw_polygon(north_west_box, 'black', fill=True)
            # print("Land to the North West!")
            pass
        else:
            neighbors.append(north_west_node)
    else:
        print("North-West is outside the grid!")

    try:
        north_east_node_index = (node_index[0] + 1, node_index[1] + 1)
        north_east_node = node_grid[north_east_node_index[0]][north_east_node_index[1]]
        north_east_box = north_east_node.box_object
        if north_east_box.intersects(land_buffer) or north_east_box.intersects(shore_buffer):
            # enc.draw_polygon(north_east_box, 'black', fill=True)
            # print("Land to the North East!")
            pass
        else:
            neighbors.append(north_east_node)
    except:
        print("North-East is outside the grid!")

    for neighbor in neighbors:
        neighbor_index = neighbor.grid_index

        # draw neighbors
        # enc.draw_polygon(neighbor.box_object, 'green')
        if neighbor is not current_node.parent:  # no cycles
            weather_cost = forecast.weather_cost(enc, node_grid, weather_grid, node_index, neighbor_index)
            if neighbor is north_node or neighbor is west_node or neighbor is east_node or neighbor is south_node:
                neighbor.g = current_node.g + radial_cost + weather_cost # update cost
            else:
                neighbor.g = current_node.g + diagonal_cost + weather_cost  # update cost
            neighbor.parent = current_node  # if we move to a node, the current node will be its parent

    #enc.draw_polygon(current_node.box_object, 'yellow')
    return neighbors

import seacharts
import forecast
import node

if __name__ == '__main__':
    size = 10000, 10000  # w, h (east, north) size of map, distance in meters
    center = 269915, 7044235  # Munkholmen island
    resolution = 25  # number of nodes for each side of the graph
    # try playing around with different grid resolutions!

    node_size = size[0] / resolution, size[1] / resolution  # size in meters of each grid cell
    corner_point = center[0] - size[0] / 2, center[1] - size[1] / 2  # bottom left corner point of map

    files = ['Basisdata_50_Trondelag_25833_Dybdedata_FGDB.gdb']  # Norwegian county database name

    # TODO: set new_data = False after first execution
    enc = seacharts.ENC(size=size, center=center, files=files, new_data=False)  # enc object

    grid = node.create_grid(resolution, corner_point, node_size)  # base grid to draw weather onto
    forecast.drawWindGrid(enc, grid, 0)

    # enc.save_image("windgrid")  # save image
    enc.show_display()  # display ENC


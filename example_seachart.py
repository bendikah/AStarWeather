import seacharts

if __name__ == '__main__':
    size = 1000, 1000      # w, h (east, north) size of map, distance in meters
    center = 269915, 7044235  # Munkholmen island

    files = ['Basisdata_50_Trondelag_25833_Dybdedata_FGDB.gdb']  # Norwegian county database name

    # TODO: set new_data = False after first execution
    enc = seacharts.ENC(size=size, center=center, files=files, new_data=True)  # enc object

    #enc.save_image("seachart")  # save image
    enc.show_display()  # display ENC


from shapely.geometry import LineString
import math
import itertools

# Script containing the two pruning function skip-prune and recseg-prune


def prune(enc, path, skip):
    pruned_path = path.copy()
    i = 0
    while i < len(pruned_path) - skip - 1:
        start_point = (pruned_path[i].box_object.centroid.x, pruned_path[i].box_object.centroid.y)
        end_point = (pruned_path[i+skip].box_object.centroid.x, pruned_path[i+skip].box_object.centroid.y)
        line = LineString([start_point, end_point])
        if not line.intersects(enc.land.geometry):
            print("Line does not intersect land at waypoint: ", i)
            for j in range(i+1, i+skip-1):
                pruned_path.remove(pruned_path[j])
        else:
            print("Line intersects land at waypoint: ", i)
        i += 1

    return pruned_path


def prune_recseg(enc, path, max_skip):
    pruned_path = path.copy()

    min_seg_num = math.ceil(len(pruned_path)/max_skip)
    print("Seg num: ", min_seg_num)
    segment_list = []

    for i in range(min_seg_num):
        print("i: ", i)
        segment = pruned_path[i*max_skip:i*max_skip + max_skip + 1]
        segment_list.append(segment)

    reduced_segment_list = []

    for segment in segment_list:
        line = LineString([segment[0].box_object.centroid, segment[-1].box_object.centroid])

        #TODO: fix elif statement
        if max_skip < 2:
            reduced_segment = segment
        elif not line.intersects(enc.shore.geometry) and not line.intersects(enc.land.geometry):
            print("No intersect")
            reduced_segment = [segment[0], segment[-1]]
        else:
            print("Intersect, initiating recursion")
            reduced_segment = prune_recseg(enc, segment, math.ceil(max_skip/2))

        reduced_segment_list.append(reduced_segment)

    reduced_segment_list = list(itertools.chain.from_iterable(reduced_segment_list))
    return reduced_segment_list

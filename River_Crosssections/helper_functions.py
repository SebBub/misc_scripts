# This script is part of the workflow to assess
# navigability in the Baro-Akobo-Sobat region
#
# Project carried out by HYDROC GmbH, 2018-2019
# for the World Food Programme
#
# Authors:
# Jens Kiesel - jenskiesel@gmail.com
# Claas Faber - claas.faber@posteo.de
#
# This script
# - contains helper functions that are accessed by different
#   scripts of the whole workflow
#
# Python 3.6.6
import os
import shutil
import shapefile
import numpy as np

def feq(a, b):
    # this function tests if two floats are equal, smaller, larger, smaller/equal, larger/equal
    if abs(a - b) < 0.0000001:
        return True
    else:
        return False

#this function tests if two floats are equal with user defined accuracy c-digits
def feq2(a,b,c):
    var = float(1*10**(-c))
    if abs(a-b)<var:
        return True
    else:
        return False

def fsm(a, b):
    # this function tests if a is smaller b
    if b - a > 0.0000001:
        return True
    else:
        return False

def flaeq(a, b):
    if a - b > 0.0000001 or feq(a, b):
        return True
    else:
        return False

def fsmeq(a, b):
    if b - a > 0.0000001 or feq(a, b):
        return True
    else:
        return False

def get_filtered_files(files_folder, extension, in_file_string):
    """
    filters all centerline shapefiles from folder and returns list
    :param folder: folder that contains centerline shapefiles
    :return: list of files
    """
    all_files = os.listdir(files_folder)
    filtered_list = []
    for afile in all_files:
        if os.path.splitext(afile)[1] == extension and in_file_string in afile:
            filtered_list.append(afile)
    return filtered_list

def move_files(fps, src_fol, tar_fol):
    for fp in fps:
        fn = os.path.split(fp)[1]
        shutil.move(os.path.join(src_fol, fn), os.path.join(tar_fol, fn))

def interpolate_x_value(x1, y1, x2, y2, yi):
    """
    interpolating in between value1 y1 at x1 and value2 y2 at x2 a new value xi at yi
    :param x1: x coord of pt 1
    :param y1: y coord of pt 1
    :param x2: x coord of pt 2
    :param y2: y coord of pt 2
    :param yi: the y-value at which x is desired
    :return: the interpolated value xi [float]
    """
    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    yi = float(yi)
    if x1 == x2:
        return False
    #defining linear equation for interpolation
    xi = yi * ((x2-x1)/(y2-y1)) - y1*((x2-x1)/(y2-y1)) + x1
    return xi

def get_distance(point1, point2):
    """
        this function calculates the distance between two points
        point1 [list]: [x,y]
        point2 [list]: [x,y]
        it returns: dist [float]
    """
    dx=point2[0]-point1[0]
    dy=point2[1]-point1[1]
    return (dx*dx+dy*dy)**(0.5)


def get_closest_point(point, ptslists):
    # this function finds the closest point to a source point by looping over all points in ptslists
    # it takes:
    # point [list of floats]: [x1,y1,...,...]
    # ptslists [list of lists of floats]: [[x1,y1,a11,a12,...a1n],[x2,y2,a21,a22,...a2n],[...],[xn,yn,an1,an2,...ann]]
    # it returns:
    # closestpoint,location [[list],int]: [x1,y1,a11,a12,...a1n], location of the point in ptslists (eg. 0 for point one in ptslists, 1 for point two in ptslists)

    mindist = get_distance(point, ptslists[0])
    closestpoint = ptslists[0]
    i = 0
    location = 0
    for pt in ptslists[1:]:
        i += 1
        dist = get_distance(point, pt)
        if dist < mindist:
            location = i
            mindist = dist
            closestpoint = pt
    return [closestpoint, location]


def map_pts_to_line(ptslist, lft_bank_dist, rgt_bank_dist, bnk_height, aline, out_polyline):
    """
    this function takes a list of points with depth attribute and the according distance to the left and right bank
    (lft_bank_dist, rgt_bank_dist,) and "maps" them to 'aline'
    - vector is calculated from line
    - perpendicular unit vector is generated
    - distance between each point in ptslists and line is calculated
    - point is moved in direction of the unit vector * distance
    - make sure the points are sorted along the line and
    - add the left and right bank to the length of the line
    - the points are shifted to match the length of aline
    - bnk_height is added to the depths
    :param ptslist: raw points to be mapped to aline [[x1,y1,depth1],[x2,y2,depth2], ... [xn,yn,depthn]], Type List
    :param lft_bank_dist: the distance from the raw observation point to left bank top, Type: float
    :param rgt_bank_dist: the distance from the raw observation point to right bank top, Type: float
    :param bnk_height: height of the bank above water surface, Type: float
    :param aline: points that define a line to which the xs points are mapped [[x1,y1],[x2,y2]], Type List
    """
    pline = perp_line(aline[0], aline[1], 1)  # the line with length 1 along which the point is moved
    pvt = vector(pline[0], pline[1])  # converting to pline to vector
    moved_pts = []
    for pt_to_move in ptslist:
        # get correct direction from pt to line: create arbitrary line from pt_to_move along the vector
        # find intersect point of resulting line with aline
        # vector to move is from pt_to_move to intersect point
        line = [pt_to_move, move_pt_along_vector(pt_to_move, pvt, 1)]
        intersect_pt = intersect_pt_endless_lines(line, aline)
        mvt = vector(pt_to_move, intersect_pt)  # the move vector
        dist = dist_pt_ln(pt_to_move, aline)  # distance by which the point is moved
        moved_pts.append(move_pt_along_vector(pt_to_move,mvt,dist))

    # moved_pts are ordered along a line and hence, the outer most points can be found by the following logic
    x_lst, y_lst, d_lst = [],[],[]
    for pt in moved_pts:
        x_lst.append(pt[0])
        y_lst.append(pt[1])
        d_lst.append(pt[2])
    idx_minx = min(range(len(x_lst)), key=x_lst.__getitem__)
    idx_maxx = max(range(len(x_lst)), key=x_lst.__getitem__)
    idx_miny = min(range(len(y_lst)), key=y_lst.__getitem__)
    idx_maxy = max(range(len(y_lst)), key=y_lst.__getitem__)

    if idx_minx == idx_miny:
        pt1 = [x_lst[idx_minx],y_lst[idx_miny],d_lst[idx_minx]]
    elif idx_minx == idx_maxy:
        pt1 = [x_lst[idx_minx],y_lst[idx_maxy],d_lst[idx_minx]]
    if idx_maxx == idx_miny:
        pt2 = [x_lst[idx_maxx],y_lst[idx_miny],d_lst[idx_maxx]]
    elif idx_maxx == idx_maxy:
        pt2 = [x_lst[idx_maxx],y_lst[idx_maxy],d_lst[idx_maxx]]
    # sort the points
    moved_pts_sorted = []
    moved_pts_sorted.append(get_closest_point(aline[0],[pt1, pt2])[0])
    moved_pts.remove(moved_pts_sorted[0])
    nr_iterations = len(moved_pts)
    for i in range(nr_iterations):
        actual_pt = get_closest_point(moved_pts_sorted[-1],moved_pts)[0]
        moved_pts.remove(actual_pt)
        moved_pts_sorted.append(actual_pt)

    DrawPolyline(out_polyline, [aline])

    # shift the points plus bank distances to match the length of aline
    target_length = get_distance(aline[0],aline[1])
    source_length = lft_bank_dist + get_distance(moved_pts_sorted[0],moved_pts_sorted[-1]) + rgt_bank_dist
    station_lst = [0, lft_bank_dist * target_length / source_length]  # the distances of depth points from left bank
    depth_lst = [0,moved_pts_sorted[0][2]+bnk_height]  # the depths of each station, starting with 0 at bank
    for pt in moved_pts_sorted[1:]:
        source_dist = get_distance(moved_pts_sorted[0],pt)
        station_lst.append(station_lst[1] + source_dist * target_length / source_length)
        depth_lst.append(pt[2]+bnk_height)
    station_lst.append(station_lst[-1] + rgt_bank_dist * target_length / source_length)  # the distances of elevation points to left bank
    depth_lst.append(0)
    return station_lst, depth_lst


def simplify_xs(stations, depths, dist_thresh, stats):
    """
    simplifies the xs through removing points that are within the distance threshold and taking the stats-depth
    value of the stations within dist_thresh
    - keep first, second, second last and last station
    - stats = 'max' is used for instance if sonar is used and may be blocked at random points through vegetation to
      be sure to get the river bed
    :param stations: a list of floats with the distance from the left bank
    :param depth:  a list of floats with the depths at each distance
    :param dist_thresh:  the distance threshold expressed as percentage of max(stations) for which stations are grouped
    :param stats: 'min', 'max', 'mean' for grouping points within dist_thresh
    :return: simplified stations and depth
    """
    filtered_stations = [stations[0],stations[1]]
    filtered_depths = [depths[0], depths[1]]
    dist_thresh_m = dist_thresh/100.0 * max(stations)

    prev_station = stations[1]
    cur_depths = []
    for i,station in enumerate(stations[2:-2]):
        cur_depths.append(depths[i+2])
        if station - prev_station >= dist_thresh_m:
            filtered_stations.append(station)
            if stats == 'min':
                filtered_depths.append(min(cur_depths))
            elif stats == 'max':
                filtered_depths.append(max(cur_depths))
            elif stats == 'mean':
                filtered_depths.append(sum(cur_depths)/len(cur_depths))
            prev_station = station
            cur_depths = []
    filtered_stations.extend([stations[-2],stations[-1]])
    filtered_depths.extend([depths[-2],depths[-1]])
    return filtered_stations, filtered_depths


def get_xs_area(stations, depths):
    """

    :param stations:
    :param depths:
    :return:
    """
    A = 0
    for i in range(len(stations)-1):
        di = depths[i]
        dj = depths[i+1]
        x = stations[i+1]-stations[i]
        A+=(di+dj)/2*x
    return A

#this function draws polylines from points (in the order in which the points are listed in the list)
#it takes:
#shape_path_str: the filename of the resulting polyline shape
#pts_lst_lst [list of lists of floats]: [[[xl11,yl11],[xl12,yl12],[...],
#                                    [xl1n,yl1n]],[[xl21,yl21],[xl22,yl22],
#                                    [...],[xl2n,yl2n]],[[xlm1,ylm1,],
#                                    [xlm2,ylm2],[...],[xlmn,ylmn]]]
#it returns :
#true if executed successfully
def DrawPolylineWithField(shape_path_str, field_lst, pts_lst_lst):
    import shapefile
    write_obj = shapefile.Writer(shapefile.POLYLINE)
    write_obj.autoBalance = 1
    write_obj.field(field_lst[0], field_lst[1], field_lst[2])
    for i,pts_lst in enumerate(pts_lst_lst):
        write_obj.poly(shapeType=3, parts=[pts_lst])
        write_obj.record(pts_lst[0][2])
    write_obj.save(shape_path_str)
    return True

#this function calculates the distance between two points
#it takes:
#point1 [list]: [x1,y1,...,...]
#point2 [list]: [x2,y2,...,...]
#it returns:
#dist [float]: the distance between the points
def Distance(point1, point2):
    dx=point2[0]-point1[0]
    dy=point2[1]-point1[1]
    dist = (dx*dx+dy*dy)**(0.5)
    return dist

def move_pt_along_vector(pt, vt, dist):
    """
    this function moves a point along a vector with length dist
    :param pt: [x,y,attr]
    :param uvt: as defined in function
    :param dist: distance by which point is to be moved
    :return: mpt: [x,y]
    """
    uvt = unit_vector(vt)
    mvt = scalar_times_vector(uvt, dist)
    return [pt[0]+mvt[0],pt[1]+mvt[1],pt[2]]


def dist_pt_ln(pt, ln):
    """
    :param pt: [x,y]
    :param ln:  [[x1,y1],[x2,y2]]
    :return: distance between point and line  - line extending unlimited
    """
    import math
    x0 = pt[0]
    y0 = pt[1]
    x1 = ln[0][0]
    y1 = ln[0][1]
    x2 = ln[1][0]
    y2 = ln[1][1]
    return abs((y2-y1)*x0-(x2-x1)*y0+x2*y1-y2*x1)/math.sqrt((y2-y1)**2+(x2-x1)**2)


def intersect_pt_endless_lines(ln1, ln2):
    """
    finds the intersect point between two lines that are indefinitely long
    and defined through two points each
    :param ln1: [[x1,y1],[x2,y2]]
    :param ln2: [[x3,y3],[x4,y4]]
    :return:
    """
    x1,y1,x2,y2, = ln1[0][0],ln1[0][1],ln1[1][0],ln1[1][1]
    x3,y3,x4,y4, = ln2[0][0],ln2[0][1],ln2[1][0],ln2[1][1]
    xi = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    yi = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    return [xi,yi]


def scalar_times_vector(vt, scalar):
    mvt = []
    for item in vt:
        mvt.append(scalar*item)
    return mvt


def DrawPolyline(shape_path_str, pts_lst_lst):
    import shapefile
    write_obj = shapefile.Writer(shapefile.POLYLINE)
    write_obj.autoBalance = 1
    write_obj.field('ID','C','10')
    for i,pts_lst in enumerate(pts_lst_lst):
        write_obj.poly(shapeType=3, parts=[pts_lst])
        write_obj.record(str(i))
    write_obj.save(shape_path_str)
    return True


def deg_to_rad(phi):
    return phi*3.14159265358979323846/180.0


def vector(pt1, pt2):
    # this function creates a vector from two points
    # it takes:
    # pt1, pt2 [list] = [x1,y1,z1,...], [x2,y2,z2,...]
    # return vt [list] = [a1,b1...]
    vt = []
    i=0
    while i < min(len(pt1),len(pt2)):
        vt.append(pt2[i]-pt1[i])
        i+=1
    return vt


def unit_vector(vt):
    # this function returns the unit vector of a vector
    # it takes:
    # vt [list] = [a1,b1,...n1]
    sqsum = 0
    uvt = []
    for item in vt:
        sqsum+=item*item
    length = sqsum**0.5
    if length == 0:
        print("vt has coincident points")
        return False
    for item in vt:
        uvt.append(item/length)
    return uvt


def rot_vector(vt, phi):
    # this function calculates a rotated vector
    # it takes:
    # vt [list] = [x1,y1] the input vector
    # phi [float] = the rotation angle in degrees (+phi left, -phi right)
    # it returns
    # the totated vector [list] = [xr1,yr1]
    import math
    rot = [[math.cos(deg_to_rad(phi)),-math.sin(deg_to_rad(phi))],[math.sin(deg_to_rad(phi)),math.cos(deg_to_rad(phi))]] #rotation matrix for phi rotation left
    return [rot[0][0]*vt[0]+rot[0][1]*vt[1],rot[1][0]*vt[0]+rot[1][1]*vt[1]]


def perp_line(pt1, pt2, length):
    # this function creates a perpendicular line to the line pt1->pt2 on pt1, which becomes middle point
    # it takes:
    # pt1 [list] = [x1,y1]
    # pt2 [list] = [x2,y2]
    # length [double] = total length of the line to be created
    # it returns:
    # return [list] = [[x1,y1][x2,y2]
    vt = [pt2[0]-pt1[0],pt2[1]-pt1[1]] #create vector from points
    uvt = unit_vector(vt)
    uvtrot1 = rot_vector(uvt, 90)
    uvtrot2 = rot_vector(uvt, 270)
    plnpt1 = [pt1[0]+uvtrot1[0]*length/2,pt1[1]+uvtrot1[1]*length/2] #x1 + unitvector x * length
    plnpt2 = [pt1[0]+uvtrot2[0]*length/2,pt1[1]+uvtrot2[1]*length/2]
    return [plnpt1,plnpt2]


def project_point(pt, src_epsg, tar_epsg, GDAL_version):
    """
    !!!!!!!!!! IMPORTANT v2.4 of GDAL calculates this point.AddPoint(pt[0], pt[1])
    differently: point.AddPoint(pt[1], pt[0]) !!!!!!!!!!!!!!!!!!!!!!!!!
    function projects a point
    :param pt: [x,y] in source coordinates
    :param src_epsg: the source EPSG code
    :param tar_epsg: the target EPSG code
    :return: pt [x,y] transformed coordinates
    """
    import ogr, osr
    point = ogr.Geometry(ogr.wkbPoint)  # create a geometry from coordinates
    if GDAL_version<=2.4:
        point.AddPoint(pt[0], pt[1])
    else:
        point.AddPoint(pt[1], pt[0])
    inSpatialRef = osr.SpatialReference()  # create coordinate transformation
    inSpatialRef.ImportFromEPSG(src_epsg)
    outSpatialRef = osr.SpatialReference()
    outSpatialRef.ImportFromEPSG(tar_epsg)
    coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
    point.Transform(coordTransform)  # transform point
    return [point.GetX(), point.GetY()]


def middle_point(ptslists):
    """
    this function returns the middle point of points
    :param ptslists: [list of lists of floats]: [[x1,y1,a11,a12,...a1n],[x2,y2,a21,a22,...a2n],[...],[xn,yn,an1,an2,...ann]]
    :return: pt [list] = [x1,y1]
    """
    accx = 0
    accy = 0
    for point in ptslists:
        accx+=point[0]
        accy+=point[1]
    return [accx / len(ptslists), accy / len(ptslists)]


def get_raster_value_at_point(point, raster_file, neighbours, stats):
    #
    # this function returns the raster value
    # at location x/y in the coordinate system
    # of the raster
    #
    # if neighbours == True, takes the neighbouring 8 cells and
    # returns the stats value = max, min, mean
    #
    import gdal
    import struct
    src_ds = gdal.Open(raster_file)
    gt = src_ds.GetGeoTransform()
    rb = src_ds.GetRasterBand(1)
    #no_data_val = rb.GetNoDataValue()
    data_type_id = rb.DataType
    raster_type = gdal.GetDataTypeName(data_type_id)
    # Conversion between GDAL types and python pack types
    data_types = {'Byte': 'B', 'UInt16': 'H', 'Int16': 'h', 'UInt32': 'I', 'Int32': 'i', 'Float32': 'f', 'Float64': 'd'}
    nrows = src_ds.RasterYSize
    xllcorner = gt[0]
    yllcorner = gt[3] - gt[1] * src_ds.RasterYSize
    cellsize = gt[1]
    xloc = int((point[0] - xllcorner) / cellsize)  # the location (column number) of x from the left edge
    yloc = int((nrows - (point[1] - yllcorner) / cellsize))  # the location (line number) of y from the upper edge
    if not neighbours:
        structval = rb.ReadRaster(xloc, yloc, 1, 1, buf_type=data_type_id)
        val = struct.unpack(data_types[raster_type], structval)
        return val[0]
    else:
        vals = []
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                structval = rb.ReadRaster(xloc+x, yloc+y, 1, 1, buf_type=data_type_id)
                vals.append(struct.unpack(data_types[raster_type], structval)[0])
        if stats == 'min':
            return min(vals)
        elif stats == 'max':
            return max(vals)
        elif stats == 'mean':
            return sum(vals)/len(vals)


def interpolate_no_data_values(values, nodata):
    # find no data values in list and save previous and next data point as interpolation borders
    intborders = []
    for i in range(0, len(values) - 1, 1):
        if feq(values[i + 1], nodata) and not values[i] == nodata:
            intborders.append(i)
        elif feq(values[i], nodata) and not values[i + 1] == nodata:
            intborders.append(i + 1)
            # interpolate between the values
    intdic = {}
    for i in range(0, len(intborders), 2):
        intdic[intborders[i]] = interpolation_steps(values[intborders[i]], values[intborders[i + 1]],
                                                   intborders[i + 1] - intborders[i] - 1)
        # merge interpolated values to original list
    for i in range(0, len(values), 1):
        for j in range(0, len(intborders), 2):
            if i == intborders[j]:
                for k in range(0, len(intdic[i]), 1):
                    values[i + k] = intdic[i][k]
    return values


def interpolation_steps(value1, value2, steps):
    # this function interpolates in between two values at certain steps
    # it takes:
    # value1 [float]: value1 of the interpolation
    # value2 [float]: value2 of the interpolation
    # steps [int]: the number of desired steps in between value1 and value2
    # it returns:
    # a list of interpolated values [value1, 1st interpolated, 2nd..., value2]
    interpolated = []
    value1 = float(value1)
    value2 = float(value2)
    steps = float(steps) + 1
    interpolated.append(value1)
    distance = value2 - value1
    if steps == 0.0:
        delta = 0
    else:
        delta = distance / steps
    i = 1.0
    while i < steps:
        if steps == 0.0:
            inter = value1
        else:
            inter = (delta) * i + value1
        interpolated.append(inter)
        i += 1.0
    interpolated.append(value2)
    return interpolated


def elevation_correction_along_line(elevationlist, maxup, maxdown):
    """
    corrects extreme jumps in elevation within "elevationlist"
    :param elevationlist: a list of float values
    :param maxup: maximum elevation jump allowed to increase from one item to the next
    :param maxdown: maximum elevation jump allowed to decrease from one item to the next
    :return: the corrected list
    """
    minimalist = []
    minimalist.append(float(elevationlist[0])) #append first entry
    lastele = float(elevationlist[0])
    for ele in elevationlist[1:]:
        if ele > lastele + maxup:
            ele = lastele + maxup
        if ele < lastele - maxdown:
            ele = lastele - maxdown
        lastele = ele
        minimalist.append(ele)
    return minimalist


def exp_func(x, a, b):
    """
    function that describes the relationship between flow areas (y) and flow accumulation (x)
    :param x: flow accumulation
    :param a: variable1 to be fitted
    :param b: variable2 to be fitted
    :return: the function's result
    """
    return a*np.exp(b*x)

def pow_func(x, a, b):

    return a*x**b

def fit_function(flw_areas, flw_accs):
    """
    uses scipy to fit a curve to the data - need to use random start values since
    it may not always converge
    :param flw_accs:
    :param flw_areas:
    :return: popt = the optimized parameters from func
    """
    import scipy
    xdata = flw_accs
    ydata = flw_areas
    popt, pcov = scipy.optimize.curve_fit(exp_func, xdata, ydata, maxfev=1000)
    """
    for i in range(10):
        start = np.random.uniform(-10, 10, size=4)
        # Get parameters estimate
        try:
            popt, pcov = scipy.optimize.curve_fit(exp_func, xdata, ydata, maxfev=1000)
        except RuntimeError:
            continue
        err = ((ydata - exp_func(xdata, *popt)) ** 2).sum()
        if err < err_last:
            err_last = err
            best = popt
    return best
    """
    return popt

def shape_to_points(file_path_str, extract_field_nr_int):
	"""
		reads geometry and one field value from a line shapefile in a nested list:
		  .each shape is made of point_records
		   - points clockwise: usual polygon
		   - points counterclockwise: hole
		  .each point_record is made of [x,y,rec]
		it takes
		file_path_str = the location of the shapefile
		extract_field_nr_int = an int representing the column id of the .dbf
							   (0 is the first, n the last), leave emtpy ('' or None)
							   in case no record is desired
		it returns
		shapes_lst_lst_lst = a list with depth 3
	"""
	sf = shapefile.Reader(file_path_str)
	shapes = sf.shapes()
	records = sf.records()
	shapes_lst_lst_lst = []
	for shape_id,shape in enumerate(shapes): #each record
		points_record_lst_lst = [] #[[x1, y1, rec1], [...]]
		if extract_field_nr_int is None or extract_field_nr_int == '':
			record_value = None
		else:
			record_value = int(records[shape_id][extract_field_nr_int])
		for pt_id_int,point in enumerate(shape.points): #loop over all points in the current shape
			if record_value is None:
				points_record_lst_lst.append([point[0], point[1]])
			else:
				points_record_lst_lst.append([point[0], point[1], record_value])
			if pt_id_int in shape.parts and not pt_id_int == 0: #shape.parts contains the list-location of points which define a new part, if single-part, shape.parts contains only [0]
				shapes_lst_lst_lst.append(points_record_lst_lst)
				points_record_lst_lst = []
		shapes_lst_lst_lst.append(points_record_lst_lst) #append the last shape
	return shapes_lst_lst_lst


def point_in_poly(x,y,poly):
    """
    Determine if a point is inside a given polygon or not.
    polys [lists]: is a list of polygons, one polygon is a list of points, the first polygon is the outer part, additional polygons are holes.
    [[[x1nohole,y1nohole],[x2nohole,y2nohole],...],[x1hole1,y1hole1],[...]],[[x1hole2,y1hole2],..]]]
    The algorithm is the "Ray Casting Method"
    implemented by "Simple Machine Forum" at "PSE Entertainment Corp", J.D.
    """
    inside = False
    n = len(poly)
    p1x,p1y = poly[0][:2]
    for i in range(n+1):
        p2x,p2y = poly[i % n][:2]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside


def read_raw_xs(fp, src_epsg, tar_epsg, GDAL_version):
    """
    function defines the xs objects based on the xs files
    and populates the data that can be derived from the xs files
    :return:
    """
    points = []
    with open(fp, 'r') as xs_read:
        for aline in xs_read:
            if aline.startswith('Dist left bank'):
                lft_bank_dist = float(aline.split(',')[1])
            elif aline.startswith('Dist right bank'):
                rgt_bank_dist = float(aline.split(',')[1])
            elif aline.startswith('Min bank height'):
                bank_height = float(aline.split(',')[1])
            elif aline.startswith('lat,lon'):
                continue
            else:
                point_lonlat = [float(aline.split(',')[1]),float(aline.split(',')[0])]
                point_xyd = project_point(point_lonlat, src_epsg, tar_epsg, GDAL_version)
                depth = float(aline.split(',')[2])
                point_xyd.append(depth)
                points.append(point_xyd)
        mp = middle_point(points)
        return lft_bank_dist, rgt_bank_dist, bank_height, points


if __name__ == "__main__":
    xs_file = r'c:\Users\jensk\Work\02_Programming\CrossSections\xs_Sobat_001_20190327_obs.csv'
    src_epsg = 4326
    tar_epsg = 32636
    GDAL_version = 3.0
    lft_bank_dist, rgt_bank_dist, bank_height, points = read_raw_xs(xs_file, src_epsg, tar_epsg, GDAL_version)
    out_polyline = r'c:\Users\jensk\Work\02_Programming\CrossSections\polyline.shp'
    out_mapped_csv = r'c:\Users\jensk\Work\02_Programming\CrossSections\xs_Sobat_001_20190327_MAPPED.csv'

    #line to map the points to (define in QGIS)
    aline_ll_tool = [[1035462.70659366, 340802.35004690], [1035788.82363771, 340768.10386567]]  # from LatLon Tool QGIS
    aline = [[aline_ll_tool[0][1],aline_ll_tool[0][0]],[aline_ll_tool[1][1],aline_ll_tool[1][0]]]

    station_lst, depth_lst = map_pts_to_line(points, lft_bank_dist, rgt_bank_dist, bank_height, aline, out_polyline)
    with open(out_mapped_csv, 'w') as wf:
        wf.write('station,depth\n')
        for stat, dep in zip(station_lst, depth_lst):
            wf.write(f'{stat},{dep}\n')




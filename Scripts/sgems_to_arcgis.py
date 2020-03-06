import csv
import os
import arcpy

"""Load GSLIB file and refactor for ArcGIS"""
# Get input file and set workspace from relative path
# Default Workspace and file paths will be replaced if parameters are given
in_workspace = os.path.dirname(__file__)
in_file = os.path.join(in_workspace, '..\\Data\\test')
out_file = os.path.join(in_workspace, '..\\Data\\output.txt')
out_raster = os.path.join(in_workspace, '..\\Data\\outputRaster.tif')
arcpy.env.overwriteOutput = True

# Check if parameters are given
if arcpy.GetParameterAsText(0):
    in_file = arcpy.GetParameterAsText(0)
    out_raster = arcpy.GetParameterAsText(1)

# Default header data for testing purposes
n_cols = '70'
n_rows = '105'
xll_center = '378923'
yll_center = '4072345'
cell_size = '30'
nodata_value = '-32768'
#aggregation_distance = 100

header = ['NCOLS ' + n_cols, 'NROWS ' + n_rows, 'XLLCENTER ' + xll_center,
          'YLLCENTER ' + yll_center,
          'CELLSIZE ' + cell_size, 'NODATA_VALUE ' + nodata_value]


def parse_header(params, doc_reader):
    # Parse first 3 lines of header as parameters to be added back later
    i = 0
    for param in params:
        params[i] = next(doc_reader)
        i += 1
    return params


def parse_coordinates(coords):
    coord_string = str(coords)
    split = coord_string.split("(")
    split.remove()
    coordinates = split[1].split('x')
    return split


def load_csv():
    params = ['coords', 'columns', 'name']
    parsed_coordinates = ''

    # Open GSLIB file as csv object for formatting purposes
    with open(in_file, 'rb') as f:
        doc_reader = csv.reader(f, delimiter='\t')

        parse_header(params, doc_reader)

        # parse_coordinates(params[0])

        # Reverse the remaining entries
        doc_reversed = reversed(list(doc_reader))

        # Create output file to be loaded into ArcMap
        with open(out_file, 'wb') as new_file:
            doc_writer = csv.writer(new_file, delimiter=' ', quoting=csv.QUOTE_NONE, escapechar=' ')
            # Re-write header back to the top of reversed list
            for line in header:
                new_file.write(line + '\n')

            # Write remaining entries into newly created file
            for row in doc_reversed:
                doc_writer.writerow(row)

    # Convert ASCII file to raster. Output will be in same directory as input GSLIB file
    arcpy.ASCIIToRaster_conversion(out_file, out_raster)
    arcpy.Mirror_management(out_raster, os.path.join(in_workspace, '..\\Data\\raster_m.tif'))

    # Clean-up stray files
    arcpy.Delete_management(out_raster)


load_csv()

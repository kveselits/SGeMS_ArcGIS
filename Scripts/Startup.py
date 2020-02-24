import csv
import os

import arcpy


class Startup(object):
    """Load GSLIB file and refactor for ArcGIS"""


in_workspace = os.path.dirname(__file__)
in_file = os.path.join(in_workspace, '../Data', 'test')
out_file = os.path.join(in_workspace, '../Data', 'output.txt')
out_raster = os.path.join(in_workspace, '../Data', 'outputRaster.tif')


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
    with open(in_file, 'rb') as file:
        doc_reader = csv.reader(file, delimiter='\t')

        parse_header(params, doc_reader)

        parse_coordinates(params[0])

        # Reverse the remaining entries
        doc_reversed = reversed(list(doc_reader))

        # Create output file to be loaded into ArcMap
        with open(out_file, 'wb') as new_file:
            doc_writer = csv.writer(new_file, delimiter=' ', quotechar='', quoting=csv.QUOTE_NONE, escapechar=' ')
            # Re-write header back to the top of reversed list
            doc_writer.writerow(params)

            # Write remaining entries into newly created file
            for row in doc_reversed:
                doc_writer.writerow(row)

    arcpy.env.workspace = arcpy.env.workspace = in_workspace
    arcpy.ASCIIToRaster_conversion(out_file, out_raster)


load_csv()

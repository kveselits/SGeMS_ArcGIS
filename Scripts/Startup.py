import csv
import os

import arcpy


class Startup(object):
    """Load GSLIB file and refactor for ArcGIS"""


dirname = os.path.dirname(__file__)
inFilename = os.path.join(dirname, '../Data', 'test')
outFilename = os.path.join(dirname, '../Data', 'output.txt')
outRaster = os.path.join(dirname, '../Data', 'outputRaster.tif')


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
    with open(inFilename, 'rb') as file:
        doc_reader = csv.reader(file, delimiter='\t')

        parse_header(params, doc_reader)

        parse_coordinates(params[0])

        # Reverse the remaining entries
        doc_reversed = reversed(list(doc_reader))

        # Create output file to be loaded into ArcMap
        with open(outFilename, 'wb') as new_file:
            doc_writer = csv.writer(new_file, delimiter=' ', quotechar='', quoting=csv.QUOTE_NONE, escapechar=' ')
            # Re-write header back to the top of reversed list
            doc_writer.writerow(params)

            # Write remaining entries into newly created file
            for row in doc_reversed:
                doc_writer.writerow(row)

    arcpy.env.workspace = arcpy.env.workspace = dirname
    arcpy.ASCIIToRaster_conversion(outFilename, outRaster)


load_csv()

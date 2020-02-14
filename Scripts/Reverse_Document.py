class Reverse_Document(object):
    """description of class"""

    lines = []


with open('test.gslib') as f:
    lines = f.readlines()

with open('../../../source/repos/SGeMS_ArcGIS/SGeMS_ArcGIS/output.txt', 'w') as f:
    for line in reversed(lines):
        if (line[::-2] <> '\n'):
            line = line + '\n'
        if not line.strip():
            f.write(line)

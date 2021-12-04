def read_file(filename):
    contents = ''
    with open(filename) as readfile:
        contents = readfile.read()
    return contents

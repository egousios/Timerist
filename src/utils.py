import json

def load_from_stylesheet(file):
    '''
    A function that reads a qss stylesheet line-by-line
    and returns the data as a string for PyQt5 to read
    and parse the stylesheet.
    '''
    with open(file, "r") as f:
        data = f.read()
        f.close()
    return str(data)

def write_and_save_json_data(json_file, json_data):
    file=open(json_file).close()
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=4)

def load_json_data_from_json_file(json_file):
    with open(json_file, 'r') as sf:
        data = sf.read()
        sf.close()
    jsonified_data = json.loads(data)
    return jsonified_data

def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)

    return tuple(rgb)
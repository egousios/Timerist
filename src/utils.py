import json

def load_from_stylesheet(file: str) -> str:
    '''
    A function that reads a qss stylesheet line-by-line
    and returns the data as a string for PyQt5 to read
    and parse the stylesheet.
    '''
    with open(file, "r") as f:
        data = f.read()
    return str(data)

def write_and_save_json_data(json_file: str, json_data: dict) -> None:
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=4)

def load_json_data_from_json_file(json_file: str) -> dict:
    with open(json_file, 'r') as sf:
        jsonified_data = json.load(sf)
    return jsonified_data

def hex_to_rgb(hex_value: str) -> tuple:
    rgb = []
    for i in range(0, len(hex_value), 2):
        decimal = int(hex_value[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)

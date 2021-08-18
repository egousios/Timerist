import json

def load_editor_settings(editor_settings_json_file):
    with open(editor_settings_json_file, 'r') as sf:
        data = sf.read()
        sf.close()
    jsonified_data = json.loads(data)
    return jsonified_data

def save_editor_settings(editor_settings_json_file, data):
    file=open(editor_settings_json_file).close()
    with open(editor_settings_json_file, 'w') as f:
        json.dump(data, f, indent=4)
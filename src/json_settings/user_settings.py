import json

def load_user_settings(user_settings_json_file):
    with open(user_settings_json_file, 'r') as sf:
        data = sf.read()
        sf.close()
    jsonified_data = json.loads(data)
    return jsonified_data

def save_user_settings(user_settings_json_file, data):
    file=open(user_settings_json_file).close()
    with open(user_settings_json_file, 'w') as f:
        json.dump(data, f, indent=4)
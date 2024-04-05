import json

from other_func import process_and_replace_keys


def load_json_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.loads(file.read())
    process_and_replace_keys(data)
    return data


MAIN_DATA = load_json_file('data.json')

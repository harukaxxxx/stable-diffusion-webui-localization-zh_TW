import json
import os
import glob
from collections import defaultdict

JSON_FOLDER = './template/zh_TW'
EXTENSIONS_FOLDER = './template/zh_TW/extensions'
MERGED_FILE = './localizations/zh_TW.json'
REPORT_FILE = './tools/merge_report.txt'


def merge_json_files():
    # Get all JSON files in the folder
    json_files = glob.glob(os.path.join(JSON_FOLDER, '*.json'))
    if os.path.exists(EXTENSIONS_FOLDER):
        json_files += glob.glob(os.path.join(EXTENSIONS_FOLDER, '*.json'))

    # Put StableDiffusion.json as the first element in the list
    stable_diffusion_file = './template/zh_TW\\StableDiffusion.json'
    if stable_diffusion_file in json_files:
        json_files.remove(stable_diffusion_file)
        json_files.insert(0, stable_diffusion_file)
    # Merge all JSON files
    merged = defaultdict(lambda: defaultdict(str))
    duplicate_keys = defaultdict(list)
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key in data.keys():
                if key in merged and isinstance(merged[key], dict) and isinstance(data[key], dict):
                    # Key already exists, recursively merge subkeys
                    merged[key] = merge_dict(
                        merged[key], data[key], duplicate_keys, file)
                elif key in merged:
                    # Key already exists, add to list of duplicate keys
                    duplicate_keys[key].append(file)
                else:
                    merged[key] = data[key]

    # Write merged JSON file
    with open(MERGED_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(merged, json_file, ensure_ascii=False, indent=4)

    # Print report
    if len(duplicate_keys) > 0:
        print('\n#####################\nDuplicate keys found.\n#####################')
        for key, files in duplicate_keys.items():
            print(f'\n"{key}" duplicate in these files:')
            for file in files:
                # Get the value for the key in the file
                with open(file, 'r', encoding='utf-8') as json_data:
                    data = json.load(json_data)
                    value = data.get(key)
                print(f'"{value}" in "{file}"')
    else:
        print('Duplicate keys not found.')


def merge_dict(dict1, dict2, duplicate_keys, file):
    # Recursively merge dictionaries
    for key in dict2.keys():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            # Key already exists, recursively merge subkeys
            dict1[key] = merge_dict(
                dict1[key], dict2[key], duplicate_keys, file)
        elif key in dict1:
            # Key already exists, add to list of duplicate keys
            duplicate_keys[key].append(file)
        else:
            dict1[key] = dict2[key]
    return dict1


if __name__ == '__main__':
    merge_json_files()

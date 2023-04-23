import json
import os
import glob
from collections import defaultdict

JSON_FOLDER = './template/zh_TW'
EXTENSIONS_FOLDER = './template/zh_TW/extensions'
MERGED_FILE = './localizations/zh_TW.json'


def merge_json_files():
    """
    合併 JSON_FOLDER 與 EXTENSIONS_FOLDER 變數路徑下的多個 JSON 檔案內容到 MERGED_FILE 變數路徑檔案中。

    參數:
        無

    返回值:
        無

    備註:
        JSON 檔案的合併是基於鍵值（key）的，若有重複的鍵值，後面讀取的檔案中的鍵值會覆蓋前面的鍵值。

    使用範例:
        merge_json_files()
    """

    # 獲取 JSON_FOLDER 與 EXTENSIONS_FOLDER 變數路徑下的所有 JSON 檔案
    json_files = glob.glob(os.path.join(JSON_FOLDER, '*.json'))
    if os.path.exists(EXTENSIONS_FOLDER):
        json_files += glob.glob(os.path.join(EXTENSIONS_FOLDER, '*.json'))

    # 合併所有 JSON 檔案的內容
    merged = defaultdict(lambda: defaultdict(str))
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            for key in data.keys():
                merged[key] = data[key]

    # 儲存合併好的 JSON 檔案
    with open(MERGED_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(merged, json_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    merge_json_files()

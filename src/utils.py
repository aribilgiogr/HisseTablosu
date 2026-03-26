import json
import os

FILE_PATH = "symbols.json"


def load_symbols():
    if not os.path.exists(FILE_PATH):
        return []

    with open(FILE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_symbols(symbols: list):
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(symbols, file, indent=4)

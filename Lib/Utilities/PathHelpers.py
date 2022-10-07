from os import path
from pathlib import Path

def build_folder_path(*args):
    csv_folder_path = Path(path.join(*args))
    csv_folder_path.mkdir(parents=True, exist_ok=True)
    return csv_folder_path
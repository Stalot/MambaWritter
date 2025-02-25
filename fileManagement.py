from pathlib import Path
from typing import Final, Iterator
import json
import sys

def bundle_path(relative_path: str | Path) -> Path:
    """
    Resolves the given path relative to the application's bundle directory.

    The function checks if the application is running in a bundled environment,
    like when the application is packaged using tools like PyInstaller, and adjusts
    the path accordingly.
    """
    bundle_dir = Path(getattr(sys, '_MEIPASS', Path.cwd()))
    config_path = bundle_dir / relative_path
    return config_path

def create_app_necessary_folders() -> dict[str, Path]:
    """
    Creates all folders the app needs to work if they don't exist yet.
    """
    documents_folderpath: Path = Path.home() / "Documents/MambaWritter"
    local_appdata_folderpath: Path = Path.home() / "AppData/Local/MambaWritter"
    
    folder_list: tuple[Path] = (documents_folderpath, local_appdata_folderpath)
    for folderpath in folder_list:
        if not folderpath.exists():
            folderpath.mkdir()
        else:
            print(folderpath, "already exists.")
    folders: dict[str, Path] = {"documents": documents_folderpath,
                                "appdata": local_appdata_folderpath}
    return folders

def read_json(filepath: str | Path) -> dict:
    with open(filepath, "r") as json_file:
        data: dict = json.loads(json_file.read())
    return data

def iterate_file(filepath: str | Path) -> Iterator:
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            yield line

if __name__ == "__main__":
    FOLDER_PATHS: Final[dict[str, Path]] = create_app_necessary_folders()
    print(FOLDER_PATHS)
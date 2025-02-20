from pathlib import Path
import json
import sys
from typing import Final

def bundle_path(path: str | Path) -> Path:
    bundle_dir = Path(getattr(sys, '_MEIPASS', Path.cwd()))
    config_path = bundle_dir / path
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

if __name__ == "__main__":
    FOLDER_PATHS: Final[dict[str, Path]] = create_app_necessary_folders()
    print(FOLDER_PATHS)
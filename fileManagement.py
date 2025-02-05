from pathlib import Path
import json

def find_internal_folder_in_cwd() -> Path | None:
    """
    Searchs for the _internal folder in the Current Working Directory (cwd).
    """
    cwd = Path.cwd()
    intern_files = (file for file in cwd.glob("*"))
    
    folder_match = None
    for file in intern_files:
        if file.name == "_internal":
            folder_match = file.absolute()
    return folder_match

def update_json_file(file_path: Path, new_data: dict) -> None:
    with open(file_path, "w") as json_file:
        json.dump(new_data, json_file, indent=4)

if __name__ == "__main__":
    folder = find_internal_folder_in_cwd()
    
    current_app_settings: dict ={
            "textbox": {
                "font": {
                    "size": 48,
                    "family": "papyrus",
                    "weight": "bold"                
                }
            }
        }
    
    settings_file_path = Path("cache\settings2.json")
    
    update_json_file(settings_file_path, current_app_settings)
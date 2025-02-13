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

def path(path: str | Path) -> Path:
    """
    Retrieves an absolute path based on the current working directory.

    The function first checks if an internal folder exists in the current working directory.
    If the internal folder does not exist, it joins the provided path with the current working directory.
    If the internal folder exists, it joins the provided path with the internal folder.
    """
    cwd = Path.cwd()
    internal_folder: Path | None = find_internal_folder_in_cwd()
    
    output_path = None
    # If the _internal folder doesn't exist:
    if not internal_folder:
        output_path = cwd.joinpath(path).absolute()
        return output_path

    # If it does:
    output_path = internal_folder.joinpath(path).absolute()
    return output_path

def read_json(filepath: str | Path) -> dict:
    with open(filepath, "r") as json_file:
        data: dict = json.loads(json_file.read())
    return data

if __name__ == "__main__":
    data = read_json("cache/app_settings.json")
    print(data)
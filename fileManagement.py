from pathlib import Path

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

if __name__ == "__main__":
    folder = find_internal_folder_in_cwd()
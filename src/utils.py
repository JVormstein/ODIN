import os.path

def check_file(file: str) -> str:
    
    if os.path.exists(file):
        return os.path.abspath(file)
    raise FileNotFoundError(file)

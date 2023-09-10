import yaml
import os

def read_yaml(file_path:str)->dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"yaml file not found {file_path}")
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)
    
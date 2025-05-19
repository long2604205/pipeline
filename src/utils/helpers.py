from pathlib import Path
import yaml

def load_config(relative_path):
    base_dir = Path(__file__).resolve().parent.parent
    full_path = base_dir / relative_path
    with open(full_path, 'r') as f:
        return yaml.safe_load(f)
import importlib.util
from pathlib import Path


module_path = Path(__file__).with_name("load-staging.py")
spec = importlib.util.spec_from_file_location("load_staging", module_path)
load_staging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(load_staging)


if __name__ == "__main__":
    load_staging.main()

import os
from pathlib import Path


ASSETS_DIR = os.getenv("ASSETS_DIR")
MLMODEL_URI = os.getenv("MLMODEL_URI")
MLMODELS_DIR = os.getenv("MLMODELS_DIR", "")

assert ASSETS_DIR, "ASSETS_DIR is not set"
assert MLMODEL_URI, "MLMODEL_URI is not set"
assert MLMODELS_DIR, "MLMODELS_DIR is not set"

IMAGE_DEMO_FILE = (Path(ASSETS_DIR) / "mnist-instance.png").resolve()

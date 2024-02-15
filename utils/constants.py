"""Exposes the constants used from the zonify service."""

import os
import pathlib

PORT = 13123

_HOME_DIR = pathlib.Path.home()
DB_LOCATION = os.path.join(_HOME_DIR, "resources", "polygons.gpkg")

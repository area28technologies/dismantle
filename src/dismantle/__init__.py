"""Dismantle is a Python package / plugin / extension manager."""
import logging
from dismantle.__version__ import __version__  # noqa: F401


logging.getLogger(__name__).addHandler(logging.NullHandler())

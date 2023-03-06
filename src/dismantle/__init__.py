"""Dismantle is a Python package / plugin / extension manager."""
import logging

from dismantle.__version__ import __version__  # noqa: F401

logging.basicConfig(
    level='DEBUG',
    format='%(asctime)s - %(name)s - [ %(message)s ]',
    datefmt='%d-%b-%y %H:%M:%S',
    force=True,
    handlers=[logging.NullHandler()],
)
log = logging.getLogger(__name__)

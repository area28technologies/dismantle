"""
Utility functions
"""
from pathlib import Path
from typing import Union


def _parse_filepath(path: Union[str, Path]) -> Union[str, Path]:
    """If it exists, strips path of the file scheme and returns
    the filepath. Otherwise, simply returns the path"""
    return str(path)[7:] if str(path).startswith('file://') else path

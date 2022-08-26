"""Check packages."""
import argparse
import sys

from dismantle import __version__


def build_parser():
    """Build the argument for the cli."""
    return argparse.ArgumentParser(
        'dismantle',
        description='Dismantle package management'
    )


def main(args=None):
    """Add entry point for python -m option."""
    args = args or sys.argv[1:]
    parser = build_parser()
    app = f'%(prog)s version {__version__}'
    parser.add_argument('-v', '--version', action='version', version=app)
    args = parser.parse_args(args)

"""Check packages."""
import argparse
import sys
from . import __version__


def main(args=None):
    """Main command line entry point."""
    args = args if args else sys.argv[1:]
    parser = argparse.ArgumentParser(
        'dismantle',
        description='Dismantle package management'
    )
    app = '%(prog)s version ' + __version__
    parser.add_argument('-v', '--version', action='version', version=app)
    args = parser.parse_args(args)

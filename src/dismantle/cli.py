"""Check packages."""
import argparse
import sys

from dismantle import __version__


def build_parser():
    """Build the argument for the cli."""
    parser = argparse.ArgumentParser(
        'dismantle',
        description='Dismantle package management'
    )
    return parser


def main(args=None):
    """Main command line entry point."""
    args = args if args else sys.argv[1:]
    parser = build_parser()
    app = '%(prog)s version ' + __version__
    parser.add_argument('-v', '--version', action='version', version=app)
    args = parser.parse_args(args)

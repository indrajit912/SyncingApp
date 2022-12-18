# Functions required for the project Sync
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

import getpass
from pathlib import Path
from .constants import *


def current_username():
    """
    Returns the current username

    Returns:
    --------
        `str`
    """
    return getpass.getuser()


def media_path(drive_name:str=None):
    """
    Returns the `Path(/media/{username}/{drive_name})`
    """
    drive_name = '' if drive_name is None else drive_name
    return Path(f"/media/{current_username()}/{drive_name}")


def get_dir_layout(dirpath: Path):
    """Get list of paths relative to dirpath of all files in dir and subdirs recursively."""
    for p in dirpath.iterdir():
        if p.is_dir():
            yield from get_dir_layout(p)
            continue
        yield str(p.relative_to(dirpath))


def main():
    print("Functions for Sync.")


if __name__ == '__main__':
    main()
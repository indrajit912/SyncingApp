# Functions required for the project Sync
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

import getpass
from pathlib import Path


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



def main():
    print("Functions for Sync.")


if __name__ == '__main__':
    main()
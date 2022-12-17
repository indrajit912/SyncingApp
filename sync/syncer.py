# Classes for Sync
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

from pathlib import Path
from datetime import datetime
import shutil

from .constants import *


class Syncer:
    """
    A class for directories synchronisation class

    Author: Indrajit Ghosh
    Created On: Dec 17, 2022

    Arguments:
    ----------
        `source_dir`: `Path`; This could be a dir in the local system.
        `end_dir`: `Path`; This could be a dir in an external HDD.

    This class prioritize `source_dir` during syncing!
    """
    def __init__(self, source_dir:Path, end_dir:Path, *, log_file:Path=None, **kwargs):

        self._source = source_dir
        self._end = end_dir

        # Setting Kwargs
        self._log_file = Path(__file__).parent.parent / 'sync.log' if log_file is None else log_file

    
    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, new:Path):
        self._source = Path(new)
    
    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, new:Path):
        self._end = Path(new)


    def __repr__(self):
        s = f"""{self.__class__.__name__}(
    source_dir = {self.source},
    end_dir = {self.end},
)"""

        return s


    def log(self, message:str):
        """
        This function appends the message into LOG file
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_info = '[' + now + ']' + message + '\n'
        with open(self._log_file, 'a') as l:
            l.write(log_info)
            print(log_info)


def main():
    print('Classes for Sync')


if __name__ == '__main__':
    main()
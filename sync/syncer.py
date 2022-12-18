# Classes for Sync
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

from pathlib import Path
from datetime import datetime
from filecmp import dircmp
import shutil, os

from .constants import *


# TODO: The following class might be used like:
#           syncObj = Syncer(dirs:list)
#           syncObj.sync() # Synchronise all dirs inside the list `dirs`

# Ref: "https://gist.github.com/pyrochlore/b754039446ef1583c258b4053cdaf2b4"


class Syncer:
    """
    A class for directories synchronisation class

    Author: Indrajit Ghosh
    Created On: Dec 17, 2022

    Argument(s):
    ----------
        `nodes`: `list[Path(), ... , Path()]` or `list[str, ... , str]  
                This is the list of paths of directories to be synced!
    """
    def __init__(self, nodes:list, name:str='Untitled_Syncer', *, log_file:Path=None, **kwargs):

        self._nodes = [Path(p) for p in nodes] # Come up with a better name
        self._name = name

        self._files_copied_count:int = 0
        self._dirs_copied_count:int = 0

        # Setting Kwargs
        self._log_file = Path(__file__).parent.parent / 'sync.log' if log_file is None else log_file

        # Writing log file
        # self.log(message="Syncer Initialized!")

    
    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, new:list):
        self._nodes = [Path(p) for p in new]

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        self._name = new_name

    
    @property
    def files_copied(self):
        return self._files_copied_count

    @property
    def dirs_copied(self):
        return self._dirs_copied_count


    def __repr__(self):
        s = f"""{self.__class__.__name__}(
    source_dir = {self.nodes},
    name = {self.name}
)"""
        return s


    def add_node(self, node:Path):
        self._nodes.append(node)


    def log(self, message:str):
        """
        This function appends the message into LOG file
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_info = '[' + now + '] ' + message + '\n'
        with open(self._log_file, 'a') as l:
            l.write(log_info)
            print(log_info)


    def sync_nodes(self, **kwargs):
        """
        This methods synchronize all nodes
        """
        # For each node in self.nodes
        for node in self.nodes:
            # If the list has another item after it, sync them
            if self.nodes.index(node) < len(self.nodes) - 1:
                next_node = self.nodes[self.nodes.index(node) + 1]
                log_msg = f"Synchronising node ```{node}``` and ```{next_node}```."
                self.log(message=log_msg)
                self._compare_directories(left=node, right=next_node, **kwargs)

    
    def _copy(self, file_list:list, src:Path, dst:Path):
        """
        This method copies a list of files(or dirs) from source node `src` to destination node `dst`
        """
        file_list = [Path(p) for p in file_list]
        for file_or_dir in file_list:
            src_path = src / file_or_dir.name
            if src_path.is_dir():
                shutil.copytree(src_path, dst=dst / file_or_dir.name)
                self._dirs_copied_count += 1
                msg = f"Copied directory `{file_or_dir.name}` from ```{src.name}``` to ```{dst.name}```."
                self.log(message=msg)

            else:
                shutil.copy2(src_path, dst)
                self._files_copied_count += 1
                msg = f"Copied `{file_or_dir.name}` from ```{src.name}``` to ```{dst.name}```."
                self.log(message=msg)

    
    def _compare_directories(self, left:Path, right:Path, **kwargs):
        """
        This method compares directories recursively (on each sub-dirs) using filecmp.dircmp() class.
        `kwargs` can be any keyword of `filecmp.dircmp`


        Attributes of `filecmp.dircmp()`:
        ----------------------------------
        left_only, right_only: names only in dir1, dir2.
        common_dirs: names of the subdirectories in both dir1 and dir2.
        diff_files: list of filenames which differ.
        """
        comparison = dircmp(a=left, b=right, **kwargs)
        
        if comparison.common_dirs:
            for dir_name in comparison.common_dirs:
                self._compare_directories(left=left / dir_name, right=right / dir_name)

        if comparison.left_only:
            self._copy(file_list=comparison.left_only, src=left, dst=right)

        if comparison.right_only:
            self._copy(file_list=comparison.right_only, src=right, dst=left)
        
        left_newer_files = []
        right_newer_files = []

        if comparison.diff_files:
            for f in comparison.diff_files:
                left_modified = os.stat(left / f).st_mtime
                right_modified = os.stat(right / f).st_mtime

                if left_modified > right_modified:
                    left_newer_files.append(f)
                else:
                    right_newer_files.append(f)
        
        self._copy(file_list=left_newer_files, src=left, dst=right)
        self._copy(file_list=right_newer_files, src=right, dst=left)
        




def main():
    print('Classes for Sync')


if __name__ == '__main__':
    main()
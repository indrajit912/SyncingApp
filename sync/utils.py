# Classes for Synchronising
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

from pathlib import Path
from datetime import datetime
from filecmp import dircmp
import shutil, os

__all__ = ["Syncer", "Syncing"]

DEFAULT_SYNC_IGNORE = [
    '.git', '.github', '.env', 'env', '.hg', '.bzr', '_darcs', 'credentials.json', 'token.json',
    '__pycache__', '.venv', 'venv', 'RCS', 'CVS', 'tags', '.sync', 'sync.log',
]

GITHUB_REPO_URL = "https://github.com/indrajit912/SyncingAndBackingUp.git"


class Syncer:
    """
    A class for synchronising directories.

    Author: Indrajit Ghosh
    Created On: Dec 17, 2022

    Argument(s):
    ----------
        `nodes`: `list[Path(), ... , Path()]` or `list[str, ... , str]  
                This is the list of paths of directories to be synced!
    """
    def __init__(
        self, nodes:list, name:str='Untitled_Syncer', *, 
        log_file:Path=None, 
        sync_ignore:list=None,
        sync_hide:list=None
    ):

        self._nodes = [Path(p) for p in nodes] # Come up with a better name
        self._name = name

        self._files_copied_count:int = 0
        self._dirs_copied_count:int = 0

        # Setting Kwargs
        self._log_file = Path(__file__).parent.parent / 'sync.log' if log_file is None else log_file
        self._ignore = DEFAULT_SYNC_IGNORE if sync_ignore is None else sync_ignore
        self._hide = [os.curdir, os.pardir] if sync_hide is None else sync_hide

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

    @property
    def ignore(self):
        return self._ignore
    
    @ignore.setter
    def ignore(self, new_list:list):
        self._ignore = new_list

    @property
    def hide(self):
        return self._hide
    
    @hide.setter
    def hide(self, new_list:list):
        self._hide = new_list


    def __repr__(self):
        s = f"""{self.__class__.__name__}(
    source_dir = {self.nodes},
    name = {self.name}
)"""
        return s


    def __str__(self):
        s = f"<class : '{self.__class__.__name__}'>\n   Nodes:\n"
        for node in self.nodes:
            s += f"\t- {node}\n"
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


    def sync_nodes(self):
        """
        This methods synchronize all nodes
        """
        self.log(message=f"Syncer name: {self.name}")
        # For each node in self.nodes
        for node in self.nodes:
            # If the list has another item after it, sync them
            if self.nodes.index(node) < len(self.nodes) - 1:
                next_node = self.nodes[self.nodes.index(node) + 1]
                log_msg = f"Synchronising node ```{node}``` and ```{next_node}```."
                self.log(message=log_msg)
                self._compare_directories(left=node, right=next_node, ignore=self.ignore, hide=self.hide)


        msg = f"TOTAL COUNT: directories_copied = {self._dirs_copied_count} and files_copied = {self._files_copied_count}.\n\n"
        self.log(msg)

    
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
                if not str(src_path) in self._ignore:
                    shutil.copy2(src_path, dst)
                    self._files_copied_count += 1
                    msg = f"Copied `{file_or_dir.name}` from ```{src.name}``` to ```{dst.name}```."
                    self.log(message=msg)
                else:
                    pass

    
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
                self._compare_directories(left=left / dir_name, right=right / dir_name, **kwargs)

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


class Syncing:
    """
    A class which provides an interface to sync between `local` and `remote` repo
    just like `git`

    Author: Indrajit Ghosh
    Created On: Dec 20, 2022
    """

    def __init__(self, local:Path, remote:Path, title:str=None, ignore:list=None):
        
        self._local = local
        self._remote = remote
        self._title = self.local.name if title is None else title
        self._ignore = DEFAULT_SYNC_IGNORE if ignore is None else DEFAULT_SYNC_IGNORE + ignore

        self._dot_sync_dir = local / ".sync"
        if not self._dot_sync_dir.exists():
            self._dot_sync_dir.mkdir()
        # Writing .sync file
        self._add_repo_info_to_dot_sync_dir()

        self._syncing_ignore_file = self._local / "syncing.ignore"
    
    
    def __repr__(self):
        return f"{self.__class__.__name__}(local={self._local},\nremote={self._remote}\n)"

    
    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, new):
        self._local = new

    @property
    def remote(self):
        return self._remote

    @remote.setter
    def remote(self, new):
        self._remote = new

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new):
        self._title = new
    
    @property
    def ignore(self):
        return self._ignore

    @ignore.setter
    def ignore(self, new):
        self._ignore = new


    def _add_repo_info_to_dot_sync_dir(self):
        with open(self._dot_sync_dir / "local.txt", 'w') as f:
            f.write(str(self._local))
        with open(self._dot_sync_dir / "remote.txt", "w") as f:
            f.write(str(self._remote))
        with open(self._dot_sync_dir / "title.txt", "w") as f:
            f.write(self._title)


    def _write_syncing_ignore_file(self):
        with open(self._syncing_ignore_file, "w") as f:
            f.write(f"# All the following files will be ignored by the App Syncing\n# Author: Indrajit Ghosh\n")
            f.write(f"# Email: indrajitghosh912@gmail.com\n")
            f.write(f"# Github Repo for Syncing App: {GITHUB_REPO_URL}\n")
            f.write(f"# --------------------------------------------------\n\n")
            for ignore in self._ignore:
                f.write(ignore)
                f.write('\n')

    def _update_syncing_ignore_file(self):
        if not self._syncing_ignore_file.exists():
            self._write_syncing_ignore_file()

        with open(self._syncing_ignore_file, 'r') as f:
            for e in f.readlines():
                if not e.startswith('#') and e != '\n':
                    e_abs = self._local / e.strip()
                    self._ignore.append(str(e))

        self._ignore = list(set(self._ignore))


    def push(self):
        """
        This sync all files inside `local` to a dir inside `remote`
        If `repo_name` is None then it will be set to `local.parent.name`
        """
        sync_title = f"{self._title}-sync"
        
        self._update_syncing_ignore_file()

        syncer = Syncer(
            name=sync_title,
            nodes=[
                self.local,
                self.remote
            ],
            sync_ignore=self._ignore
        )

        syncer.sync_nodes()



def main():
    print('Classes for Sync')


if __name__ == '__main__':
    main()
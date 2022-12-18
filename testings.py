# Sync Tests
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#


################# REFERENCES
# TODO: Finding Duplicates: "https://stackoverflow.com/questions/748675/finding-duplicate-files-and-removing-them"
# TODO: Comparing files

# Get file sizes by os.stat()

from sync import *
import os, stat
import filecmp

BACKUP_DIR = Path.home() / "Downloads" / "backup_test_dir"
SOURCE_DIR = Path.home() / "Downloads" / "source_test_dir"
F1 = SOURCE_DIR / "sound_waves.mp4"
F2 = SOURCE_DIR / "Assignment_2_FuncAnalysis_Mmat1_2021_22.pdf"
F3 = SOURCE_DIR / "spam.txt"
PIC = SOURCE_DIR / "holi.jpg"

def _sig(st):
    """
    This function accepts the result of `os.stat(<path>)` and returns a tuple
    containg: (File type, File size, Last modified)
    """
    return (stat.S_IFMT(st.st_mode), # File type
            st.st_size, # File size
            st.st_mtime) # Last modified

def list_files_and_dirs(path):
    """
    Returns the lists containg AbsolutePaths of directories and files
    at the given path
    """
    given_path = Path.absolute(path)
    dirs = []
    files = []

    for file_or_dir in given_path.glob('*'):
        if file_or_dir.is_dir():
            dirs.append(file_or_dir)
        if file_or_dir.is_file():
            files.append(file_or_dir)

    # p = Path.absolute(files[0]) # Getting the absolute path

    return sorted(dirs), sorted(files)


def main():

    syncer = Syncer(
        nodes=[SOURCE_DIR, BACKUP_DIR],
        name="IndraSync"
    )

    syncer.sync_nodes()
    

if __name__ == '__main__':
    main()
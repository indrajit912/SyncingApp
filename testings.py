# Sync Tests
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#


################# REFERENCES
# TODO: Finding Duplicates: "https://stackoverflow.com/questions/748675/finding-duplicate-files-and-removing-them"

# Get file sizes by os.stat()

from sync import *

BACKUP_DIR = Path.home() / "Downloads" / "backup_test_dir"
SOURCE_DIR = Path.home() / "Downloads" / "source_test_dir"
F1 = SOURCE_DIR / "sound_waves.mp4"
F2 = SOURCE_DIR / "Assignment_2_FuncAnalysis_Mmat1_2021_22.pdf"
F3 = SOURCE_DIR / "spam.txt"
PIC = SOURCE_DIR / "holi.jpg"


def main():

    syncer = Syncer(
        nodes=[SOURCE_DIR, BACKUP_DIR, Path.home() / 'Downloads/indra/'],
        name="IndraSync"
    )

    syncer.sync_nodes()


if __name__ == '__main__':
    main()
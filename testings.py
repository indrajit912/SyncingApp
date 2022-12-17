# Sync Tests
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

from sync import *

BACKUP_DIR = Path.home() / "Downloads" / "backup_test_dir"
SOURCE_DIR = Path.home() / "Downloads" / "source_test_dir"


def main():

    syncer = Syncer(
        source_dir=SOURCE_DIR,
        end_dir=BACKUP_DIR,
    )

    print(syncer)


if __name__ == '__main__':
    main()
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
DOWNLOADS = Path.home() / "Downloads"


def main():

    nodes = [
        DOWNLOADS / "hey",
        DOWNLOADS / "nice"
    ]

    syncer = Syncer(nodes=nodes, name="TestSync")

    syncer.sync_nodes()



if __name__ == '__main__':
    main()
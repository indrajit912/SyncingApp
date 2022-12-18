# Project to synchronize data between my laptop and external HDD
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

from sync import *

EXT_HDD_NAME = "INDRA_MAC"


def main():

    VOLDEMORT_AT_HDD = media_path(EXT_HDD_NAME) / "Voldemort"

    if not VOLDEMORT_AT_HDD.exists():
        VOLDEMORT_AT_HDD.mkdir()

    syncer = Syncer(
        nodes=[
            Path.cwd(),
            VOLDEMORT_AT_HDD
        ],
        name="Voldemort-INDRA_MAC_HDD-Sync"
    )

    syncer.sync_nodes()


if __name__ == '__main__':
    main()
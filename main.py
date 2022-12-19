# Project to synchronize data between my laptop and external HDD
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

from sync import *
from filecmp import dircmp

# TODO: Make cmd interface e.g. 
#       ```sync remote add origin <dir_at_hdd>```
#       ```sync push origin master```

# Voldemort
DOCUMENTS = Path.home() / "Documents"
VIDEOS = Path.home() / "Videos"

DIRS_AT_VOLDEMORT = [
    # DOCUMENTS / "hello_world",
    DOCUMENTS / "Meself_Indra",
    VIDEOS
]


# My External HDD
INDRA_MAC = "INDRA_MAC"


def sync_indra_mac():

    indra_mac = media_path(INDRA_MAC)
    if not indra_mac.exists():
        print(f"The HDD with the name `{INDRA_MAC}` is not connected to this PC.")
    
    else:
        VOLDEMORT_AT_HDD = media_path(INDRA_MAC) / "Voldemort"

        if not VOLDEMORT_AT_HDD.exists():
            VOLDEMORT_AT_HDD.mkdir()


        # Synchronizing
        for dir in DIRS_AT_VOLDEMORT:

            voldemort_dir = VOLDEMORT_AT_HDD / dir.name # directory with the same name at HDD
            if not voldemort_dir.exists():
                voldemort_dir.mkdir()

            log_file_path = dir / "sync.log"

            name = f"Voldemort-{dir.name}-syncer" # Name of the Syncer Obj
            syncer = Syncer(
                nodes=[dir, voldemort_dir],
                name=name,
                log_file=log_file_path
            )

            syncer.sync_nodes()



def main():
    # sync_indra_mac()
    nice = Path.home() / "Downloads/nice"

    syncer = Syncer(
        nodes=[VIDEOS / "movies/", nice],
    )

    # syncer.sync_nodes()

    

if __name__ == '__main__':
    main()
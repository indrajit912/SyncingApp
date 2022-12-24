# Project to synchronize data between my laptop and external HDD
#
# Author: Indrajit Ghosh
#
# Created on: Dec 17, 2022
#

from sync import *
import sys, os

# TODO: there is a bug! this script is generating `syncing.ignore` at Path(__file__).parent
#       This should not be the case at all. Fix this.

# My External HDD
INDRA_MAC = "INDRA_MAC"

VOLDEMORT_AT_HDD = media_path(INDRA_MAC) / "Voldemort"
HELLO_WORLD_AT_INDRA_MAC = VOLDEMORT_AT_HDD / "hello_world"
BORINGAUTOMATE_AT_INDRA_MAC = HELLO_WORLD_AT_INDRA_MAC / "BoringAutomate"


def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')


def syncing_init(local:Path, remote:Path, title:str=None):

    sy = Syncing(
        local=local,
        remote=remote,
        title=title
    )
    print("Syncing App initialized with the following info:")
    print(sy)


def read_dot_sync_dir(dot_sync_dir:Path):
    with open(dot_sync_dir / 'local.txt', 'r') as f:
        local = Path(f.read())

    with open(dot_sync_dir / 'remote.txt', 'r') as f:
        remote = Path(f.read())

    title_path = dot_sync_dir / 'title.txt'
    if title_path.exists():
        with open(title_path, 'r') as f:
            title = f.read()
    else:
        title = None

    return local, remote, title


def syncing_push():
    dot_sync_dir = Path.cwd() / ".sync"
    if not dot_sync_dir.exists():
        raise Exception("No remote found! First initialize one by the cmd ```syncing init``` ")

    else:
        local, remote, title = read_dot_sync_dir(dot_sync_dir)
        if remote is None:
            raise Exception("No remote found! First initialize one by the cmd ```syncing init``` ")

        # Check whether `syncing.ignore` exists or not if so read it and pass its values
        #       through Syncing(ignore=)
        local_syncing_ignore_file = local / 'syncing.ignore'
        _ignore = []
        if local_syncing_ignore_file.exists():
            with open(local_syncing_ignore_file, 'r') as f:
                for e in f.readlines():
                    if not e.startswith('#') and e != '\n':
                        e = local / e.strip()
                        _ignore.append(str(e))
        
        syncObj = Syncing(local=local, remote=remote, title=title, ignore=_ignore)
        syncObj.push()



def syncing_app():
    
    USAGES = f"""
    Syncing App

    Author: Indrajit Ghosh
    Created On: Dec 20, 2022

    Usages:
        [Initializing] ```syncing init```  
        [Syncing] ```syncing push```
    """
    clear_screen()

    if len(sys.argv) < 2:
        print(USAGES)
        sys.exit()

    else:
        if sys.argv[1] == 'init':
            local_dir = Path.cwd()
            dot_sync_dir = local_dir / '.sync'
            res = 'y'
            if dot_sync_dir.exists():
                remote_txt = dot_sync_dir / 'remote.txt'
                saved_remote = open(remote_txt, 'r').read()
                if saved_remote is not None:
                    print(f"WARNING: There is already a remote dir exists at:\n   {saved_remote}")
                    res = input("Do you still continue to replace this old one?(y/n): ")
                    if res.lower() not in ['y', 'yes', 'n', 'no']:
                        raise Exception(f"Wrong input {res}!")
            
            if res in ['y', 'yes']:
                remote_dir = Path(input("Enter the path of the remote dir: "))
                title = input("Enter a title (If you don't have any simply hit <ENTER>): ")
                title = None if title == '' else title

                if not remote_dir.exists():
                    raise Exception(f"The remote directory {remote_dir} doesn't exits!")

                syncing_init(local=local_dir, remote=remote_dir, title=title)
            else:
                print("Okay! No changes made.")
        
        elif sys.argv[1] == 'push':
            syncing_push()


def main():
    syncing_app()


if __name__ == '__main__':
    main()
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
# https://www.geeksforgeeks.org/how-to-upload-project-on-github-from-pycharm/

"""
net view \\CalDrives

"""

import os

Debug = False

CalDrives = [
    "Cassie_Windows",
    "home",
    "homes",
    "LaurieO",
    "linux",
    "music",
    "NetBackup", "photo", "video", "web", "web_packages"
]

Buffalo = [
    "Music", "Cassie-Windows", "Cassie-Linux", "Laurie",
    "Cassie-Backup", "Laurie-Backup", "Cassie", "cenicol", "Shared",
    "webaxs"
]

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def fn1():
    '''
    print out the environment variables
    '''
    if Debug:
        print (os.environ)
        keys = list(os.environ.keys())
        for k in keys:
            print(k)
        print(keys)


def fn2():
    '''
    try to print a list of shares.
    -- Not possible as
       \\CalDrives is not a directory
       \\CalDrives cannot be enumerated
    path = device\share
    device=\\CalDrives
    share=homes
    path=\\CalDrives\Cassie_Windows
    of course escaping each backslash gives
    path=\\\\CalDrives\\Cassie_Windows
    '''
    backup_repository_path = "\\\\CalDrives\\"        # Can't have an empty share (after \\).
    backup_repository_path = "\\\\CalDrives"          # Mounts, but is not a directory
    backup_repository_path = "\\\\CalDrives\\homes"

    backup_storage_available = os.path.isdir(backup_repository_path)
    print("backup_storage_available", backup_storage_available)


    BACKUP_REPOSITORY_USER_NAME = "cenicol"
    BACKUP_REPOSITORY_USER_PASSWORD = "ka1.ssa8"
    if backup_storage_available:
        # logger.info("Backup storage already connected.")
        print("Backup storage already connected.")
        shares = os.listdir(backup_repository_path)
        for share in shares:
            print("\t", share)
    else:
        # logger.info("Connecting to backup storage.")
        print("Connecting to backup storage.")

    if os.path.ismount(backup_repository_path):
        print("Path is a mount point")
    else:
        print("Path is not a mount point")

    if not backup_storage_available:
        """  
        I want to build a command like the one below.
        cassi> net use /user:cenicol \\CalDrives\homes ka1.ssa8
        """
        #
        # net use /user:BACKUP_REPOSITORY_USER_NAME BACKUP_REPOSITORY_PATH BACKUP_REPOSITORY_USER_PASSWORD
        print("BACKUP_REPOSITORY_USER_NAME", BACKUP_REPOSITORY_USER_NAME)
        print("BACKUP_REPOSITORY_USER_PASSWORD", BACKUP_REPOSITORY_USER_PASSWORD)
        print("backup_repository_path", backup_repository_path)
        print(f"NET USE /USER:\\{BACKUP_REPOSITORY_USER_NAME} ")
        mount_command = "net use /user:" + BACKUP_REPOSITORY_USER_NAME + " " + backup_repository_path + " " + BACKUP_REPOSITORY_USER_PASSWORD
        print("mount_command=", mount_command)
        os.system(mount_command)

        backup_storage_available = os.path.isdir(backup_repository_path)
        print("backup_storage_available", backup_storage_available)
        if backup_storage_available:
            print("Connection success.")
            #logger.fine("Connection success.")
            print("listing ", backup_repository_path)
            dirs = os.listdir(backup_repository_path)
            for file in dirs:
                print(file)
        else:
            raise Exception("Failed to find storage directory.")
            print("not backup_storage_available", backup_repository_path)



def list_mount_points ():
    print("CalDrives")
    for point in CalDrives:
        print("\t", point)
    print("Buffalo")
    for point in Buffalo:
        print("\t", point)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    print_hi('Cassie')
    # print_hi(os.environ.get("USERNAME"))

    list_mount_points()

    fn2()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

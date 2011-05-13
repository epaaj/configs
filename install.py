#! /usr/bin/env python

# install.py by Jimmy Garpehäll (epaaj@ninjaloot.se)
#
# WTFPL.
#
# Git repo config file installer

"""
install.py is a git repo config installer. It creates symlinks to the config
files and will backup any existing files before overwriting.
"""

import sys
import os
import errno
from optparse import OptionParser

PACKAGES = {
    "i3": (
        ("i3",),
        tuple(),
    ),
    "ncmpcpp": (
        ("ncmpcpp",),
        tuple(),
    ),
    "stumpwm": (
        tuple(),
        ("stumpwm/stumpwmrc",),
    ),
    "vim": (
        ("vim",),
        ("vim/vimrc",),
    ),
    "x": (
        tuple(),
        ("x/Xdefaults", "x/xinitrc"),
    ),
    "zsh": (
        tuple(),
        ("zsh/zshrc", "zsh/aliasrc"),
    ),
}

DIRECTORIES = []
FILES = []

for package in PACKAGES:
    for arg in sys.argv:
        if package == arg:
            for k in PACKAGES[package][0]:
                DIRECTORIES.append(k)
            for k in PACKAGES[package][1]:
                FILES.append(k)

if len(DIRECTORIES) < 1 and len(FILES) < 1:
    for package in PACKAGES:
        for k in PACKAGES[package][0]:
            DIRECTORIES.append(k)
        for k in PACKAGES[package][1]:
            FILES.append(k)

STDBACKUPDIRECTORY = os.path.join(os.environ['HOME'], ".bak", "")

PARSER = OptionParser()
PARSER.add_option("-b", "--backup",
                action="store", dest="backup", metavar="DIRECTORY",
                help="backup destination (absolute path). Default: " + STDBACKUPDIRECTORY)
PARSER.add_option("-u", "--uninstall",
                action="store_true", dest="uninstall", default=False,
                help="uninstall")
PARSER.add_option("-p", "--pretend",
                action="store_true", dest="pretend", default=False,
                help="tests the installation without changing anything. Only prints messages.")
PARSER.add_option("-e", "--extrafiles",
                action="store_true", dest="extrafiles", default=False,
                help="show existing config files not handled by this program.")
(OPTIONS, ARGS) = PARSER.parse_args()

def check_backup():
    '''Check backup directory'''
    if os.path.lexists(DEST):
        if len(os.listdir(DEST)) == 0:
            print("Backup directory exists but is empty:", DEST)
            print("Proceeding with installation.")
        else:
            print("Backup directory exists and is not empty:", DEST)
            print("If this is the first time running this installation you may want to backup or delete", DEST)
            print("Do so now and then proceed with the installation or abort.")
            print("Note that the installation will ask before overwriting any files.")
            while(True):
                answer = input("Proceed? [y/n]: ")
                if answer == "y":
                    return DEST
                elif answer == "n":
                    print("Backup failed. Aborting installation.")
                    quit()
                else:
                    print("Input y or n")
    else:
        print("Backup directory does not exist. Creating", DEST)
        os.mkdir(DEST)
        return DEST

def backup(src):
    '''Backup'''
    if os.path.lexists(os.path.join(DEST, src)):
        print("Backup file exists:", DEST + src)
        print("Overwriting file. Backup if needed and then proceed.")
        while(True):
            answer = input("Overwrite? [y/n]: ")
            if answer == "y":
                if do_rename(os.path.join(os.environ['HOME'], src), os.path.join(DEST, src)):
                    return True
                else:
                    return False
            elif answer == "n":
                print("Backing up", DEST + src, "aborted.")
                return False
            else:
                print("Input y or n")
    else:
        tmp = os.path.split(DEST + src)
        if not os.path.lexists(tmp[0]):
            os.makedirs(tmp[0])
        if do_rename(os.path.join(os.environ['HOME'], src), os.path.join(DEST, src)):
            return True
        else:
            return False

def restore(target, restore_files):
    '''Restore'''
    bfilename = os.path.join(DEST, target)
    filename = os.path.join(os.environ['HOME'], target)
    if do_remove(filename):
        if restore_files:
            if do_rename(bfilename, filename):
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def install_files():
    '''Check files'''
    for i in range(len(FILES)):
        linkto = os.path.abspath(FILES[i])
        bfilename = "." + os.path.basename(FILES[i])
        filename = os.path.join(os.environ['HOME'], bfilename)
        if os.path.lexists(filename):
            if os.path.islink(filename):
                linksto = os.readlink(filename)
                if linksto == linkto:
                    print("Target link is correct:", filename, "->", linkto)
                else:
                    print("Target link wrong. Backing up", filename)
                    if backup(filename):
                        print("Creating link", filename, "->", linkto)
                        do_symlink(linkto, filename)
            elif os.path.isfile(filename):
                print("Target file exists. Backing up", filename)
                if backup(bfilename):
                    print("Creating link", filename, "->", linkto)
                    do_symlink(linkto, filename)
            else:
                print("File is no file O_o")
        else:
            print("File does not exist. Creating link:", filename, "->", linkto)
            do_symlink(linkto, filename)
        print("")

def get_directories():
    '''Get directories'''
    filelist = []
    for i in range(len(DIRECTORIES)):
        filelist.append(DIRECTORIES[i])
        tmp = read_dir(DIRECTORIES[i], os.path.join(DIRECTORIES[i], ""))
        for j in range(len(tmp)):
            filelist.append(tmp[j])
    return filelist

def read_dir(path, prev):
    '''Reads directory recursive'''
    read_dirfilelist = os.listdir(path)
    for i in range(len(read_dirfilelist)):
        if prev != "":
            read_dirfilelist[i] = prev + read_dirfilelist[i]
        if os.path.isdir(read_dirfilelist[i]):
            tmp = read_dir(read_dirfilelist[i], os.path.join(read_dirfilelist[i], ""))
            for j in range(len(tmp)):
                read_dirfilelist.append(tmp[j])
    return read_dirfilelist

def file_type_check(path):
    '''Check if directory'''
    typelist = []
    for i in range(len(path)):
        if os.path.isdir(path[i]):
            typelist.append("dir")
        elif os.path.isfile(path[i]):
            typelist.append("file")
    return typelist

def check_directories():
    '''Check directories'''
    for i in range(len(FILETYPELIST)):
        bfilename = "." + FILELIST[i]
        filename = os.path.join(os.environ['HOME'], bfilename)
        if FILETYPELIST[i] == "dir":
            if os.path.lexists(filename):
                if os.path.isdir(filename):
                    print("Directory exists:", filename)
                elif os.path.isfile(filename):
                    # Directory is file
                    print("Directory is a file. Backing up", filename)
                    if backup(bfilename):
                        do_mkdir(filename)
            else:
                print("CREATE DIRECTORY")
                os.mkdir(filename)
        elif FILETYPELIST[i] == "file":
            linkto = os.path.abspath(FILELIST[i])
            if os.path.lexists(filename):
                if os.path.isfile(filename):
                    if os.path.islink(filename):
                        linksto = os.readlink(filename)
                        if linksto == linkto:
                            print("Target link is correct:", filename, "->", linkto)
                        else:
                            print("Target link wrong. Backing up", filename)
                            if backup(bfilename):
                                print("Creating link", filename, "->", linkto)
                                do_symlink(linkto, filename)
                    else:
                        print("Target file exists. Backing up", filename)
                        if backup(bfilename):
                            print("Creating link", filename, "->", linkto)
                            do_symlink(linkto, filename)                        
                    
                elif os.path.isdir(filename):
                    print("Target file is a directory. Backing up", filename)
                    if backup(bfilename):
                        print("Creating link", filename, "->", linkto)
                        do_symlink(linkto, filename)
                        
            else:
                print("File does not exist. Creating link", filename, "->", linkto)
                do_symlink(linkto, filename)
        print("")

def do_mkdir(dirname):
    '''Create directory and check for errors'''
    try:
        if not PARSER.values.pretend:
            os.mkdir(dirname)
        else:
            pass
    except OSError as err:
        # Directory exists
        if err.errno == errno.EEXIST:
            pass
        # No access
        elif err.errno == errno.EACCES:
            print("Could not create directory:", dirname)
            print("Permission denied.")
        else:
            print("Could not create directory:", dirname)
        return False
    else:
        return True

def do_symlink(target, linkname):
    '''Create symlink and check for errors'''
    try:
        if not PARSER.values.pretend:
            os.symlink(target, linkname)
        else:
            pass
    except OSError as err:
        print("Could not create symlink:", linkname, "->", target)
        # Target exists
        if err.errno == errno.EEXIST:
            print("Target file exists:", linkname)
        # No access
        elif err.errno == errno.EACCES:
            print("Permission denied.")
        else:
            print("Unknown error. Error No:", err.errno)
        return False
    else:
        return True

def do_rename(src, target):
    '''Rename file or directory and check for errors'''
    try:
        if not PARSER.values.pretend:
            os.rename(src, target)
        else:
            pass
    except OSError as err:
        print("Could not move file", src)
        # Target exists
        if err.errno == errno.EEXIST:
            print("Target file exists:", target)
        # No access
        elif err.errno == errno.EACCES:
            print("Permission denied.")
        # Src does not exist
        elif err.errno == errno.ENOENT:
            print("Source file does not exist:", src)
        # Target is a directory
        elif err.errno == errno.EISDIR:
            print("Target file is a directory:", target)
        # If src is a file and target is not a directory
        elif err.errno == errno.ENOTDIR:
            print("Source is a directory:", src)
            print("Target is a file:", target)
        else:
            print("Unknown error. Error No:", err.errno)
        return False
    else:
        return True

def do_remove(target):
    '''Remove file and check for errors'''
    try:
        if not PARSER.values.pretend:
            os.remove(target)
        else:
            pass
    except OSError as err:
        print("Could not remove file", target)
        # No access
        if err.errno == errno.EACCES:
            print("Permission denied.")
        # Target does not exist
        elif err.errno == errno.ENOENT:
            print("Source file does not exist:", target)
        # Target is a directory
        elif err.errno == errno.EISDIR:
            print("Target file is a directory:", target)
        else:
            print("Unknown error. Error No:", err.errno)
        return False
    else:
        return True

def do_rmdir(target):
    '''Remove directory and check for errors'''
    try:
        if not PARSER.values.pretend:
            os.rmdir(target)
        else:
            pass
    except OSError as err:
        print("Could not remove directory", target)
        # No access
        if err.errno == errno.EACCES:
            print("Permission denied.")
        # Target is not a directory
        elif err.errno == errno.ENOTDIR:
            print("Target is not a directory:", target)
        # Directory is not empty
        elif err.errno == errno.ENOTEMPTY:
            print("Directory is not empty and should not be removed:", target)
        else:
            print("Unknown error. Error No:", err.errno)
        return False
    else:
        return True

def check_extra_files():
    '''Check directories for files that will not be touched by the installation'''
    filelist = get_directories()
    filelist.sort()
    filetypelist = file_type_check(filelist)
    efilelist = DIRECTORIES
    for i in range(len(efilelist)):
        efilelist[i] = os.path.join(os.environ['HOME'], "." + efilelist[i])
        tmp = read_dir(efilelist[i], efilelist[i] + "/")
        for j in range(len(tmp)):
            efilelist.append(tmp[j])
    efilelist.sort()
    for i in range(len(filelist)):
        try:
            efilelist.remove(os.path.join(os.environ['HOME'], "." + filelist[i]))
        except ValueError:
            pass

    for i in range(len(efilelist)):
        print(i, ":", efilelist[i])

def uninstall_files(restore_files):
    '''Check files'''
    for i in range(len(FILES)):
        linkto = os.path.abspath(FILES[i])
        bfilename = "." + os.path.basename(FILES[i])
        filename = os.path.join(os.environ['HOME'], bfilename)
        if os.path.lexists(filename):
            if os.path.islink(filename):
                linksto = os.readlink(filename)
                if linksto == linkto:
                    # Restore
                    if restore(bfilename, restore_files):
                        print("Target restored:", filename)
                else:
                    print("Target seems already restored. Ignoring:", filename)
            else:
                print("Target seems already restored. Ignoring:", filename)
        else:
            print("Target not installed:", filename)

def clear_backup_directory():
    '''Remove empty directories in backup directory'''
    if os.path.lexists(DEST):
        if len(os.listdir(DEST)) == 0:
            pass
        else:
            delbackuplist = read_dir(DEST, DEST)
            delbackuplist.sort()
            for i in range(len(delbackuplist)):
                delbackuplist[i] = os.path.join(DEST, delbackuplist[i])
            delbackupfiletypelist = file_type_check(delbackuplist)
            for i in reversed(range(len(delbackuplist))):
                if delbackupfiletypelist[i] == "dir":
                    try:
                        if not PARSER.values.pretend:
                            os.rmdir(delbackuplist[i])
                        else:
                            pass
                    except OSError as err:
                        if err.errno == errno.ENOTEMPTY:
                            print("Directory is not empty and should not be removed:", delbackuplist[i])
                        else:
                            print(err)
            try:
                if not PARSER.values.pretend:
                    os.rmdir(DEST)
                else:
                    pass
            except OSError as err:
                if err.errno == errno.ENOTEMPTY:
                    print("Backup directory is not empty and will not be removed:", DEST)
                else:
                    print(err)
            else:
                print("Backup directory is empty and has been removed:", DEST)
    else:
        pass

def uninstall():
    '''Uninstall files'''
    restore_files = False
    if os.path.lexists(DEST):
        if len(os.listdir(DEST)) == 0:
            print("Backup directory exists but is empty:", DEST)
            print("No files to restore.")
        else:
            print("Backup directory is not empty:", DEST)
            print("Restoring files")
            restore_files = True
    else:
        print("Backup directory does not exists:", DEST)
        print("No files to restore.")
    print("")

    if len(FILES) > 0:
        print("")
        print("")
        print("UNINSTALLING FILES")
        print("")
        uninstall_files(restore_files)

    if len(DIRECTORIES) > 0:
        print("")
        print("")
        print("UNINSTALLING DIRECTORIES")

        for i in range(len(FILELIST)):
            bfilename = "." + FILELIST[i]
            filename = os.path.join(os.environ['HOME'], bfilename)
            if FILETYPELIST[i] == "file":
                linkto = os.path.abspath(FILELIST[i])
                if os.path.lexists(filename):
                    if os.path.isfile(filename):
                        if os.path.islink(filename):
                            linksto = os.readlink(filename)
                            if linksto == linkto:
                                # Restore
                                if restore(bfilename, restore_files):
                                    print("Target restored:", filename)
                            else:
                                print("Target seems already restored. Ignoring:", filename)
                        else:
                            print("Target seems already restored. Ignoring:", filename)
                    else:
                        print("Target seems already restored. Ignoring:", filename)
                else:
                    print("Target is not installed:", filename)
    
        for i in reversed(range(len(FILELIST))):
            bfilename = "." + FILELIST[i]
            filename = os.path.join(os.environ['HOME'], bfilename)
            if FILETYPELIST[i] == "dir":
                if len(os.listdir(filename)) == 0:
                    print("Directory empty:", filename)
                    print("Removing:", filename)
                    if do_rmdir(filename):
                        print("Directory removed:", filename)
        print("")

    print("")
    clear_backup_directory()
    print("")
    print("")
    print("UNINSTALLATION COMPLETE!")

if PARSER.values.extrafiles:
    check_extra_files()
    quit()

if PARSER.values.pretend:
    print("PRETENDING:")

# Get backup directory
if PARSER.values.backup == None:
    DEST = STDBACKUPDIRECTORY
else:
    DEST = PARSER.values.backup
    # Check if dest ends with separator. If not add it.
    if not DEST.endswith(os.sep):
        DEST = os.path.join(DEST, "")

FILELIST = get_directories()
FILELIST.sort()
for i in range(len(FILES)):
    try:
        FILELIST.remove(FILES[i])
    except ValueError:
        pass

FILETYPELIST = file_type_check(FILELIST)

if PARSER.values.uninstall:
    if len(DIRECTORIES) > 0 or len(FILES) > 0:
        uninstall()
    else:
        print("Nothing to uninstall.")
else:
    print("")
    print("")
    print("CHECKING BACKUP DIRECTORY")
    print("")
    check_backup()
    if len(FILES) > 0:
        print("")
        print("")
        print("CHECKING FILES")
        print("")
        install_files()
    if len(DIRECTORIES) > 0:
        print("")
        print("")
        print("CHECKING DIRECTORIES")
        print("")
        check_directories()

    print("")
    print("INSTALLATION COMPLETE")

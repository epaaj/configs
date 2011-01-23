#! /usr/bin/env python

# install.py by Jimmy Garpehäll (epaaj@ninjaloot.se)
#
# WTFPL.
#
# Git repo config file installer

import sys
import os
import errno
from optparse import OptionParser

packages = {
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

directories = []
files = []

for i in packages:
	for j in sys.argv:
		if i == j:
			for k in packages[i][0]:
				directories.append(k)
			for k in packages[i][1]:
				files.append(k)

if len(directories) < 1 and len(files) < 1:
	for i in packages:
		for k in packages[i][0]:
			directories.append(k)
		for k in packages[i][1]:
			files.append(k)

stdbackupdirectory = os.path.join(os.environ['HOME'], ".bak", "")

parser = OptionParser()
parser.add_option("-b", "--backup",
				action="store", dest="backup", metavar="DIRECTORY",
				help="backup destination (absolute path). Default: " + stdbackupdirectory)
parser.add_option("-u", "--uninstall",
				action="store_true", dest="uninstall", default=False,
				help="uninstall")
parser.add_option("-p", "--pretend",
				action="store_true", dest="pretend", default=False,
				help="test")
parser.add_option("-e", "--extrafiles",
				action="store_true", dest="extrafiles", default=False,
				help="show existing config files not handled by this program.")
(options, args) = parser.parse_args()

def checkbackup():
	'''Check backup directory'''
	if os.path.lexists(dest):
		if len(os.listdir(dest)) == 0:
			print("Backup directory exists but is empty:", dest)
			print("Proceeding with installation.")
		else:
			print("Backup directory exists and is not empty:", dest)
			print("If this is the first time running this installation you may want to backup or delete", dest)
			print("Do so now and then proceed with the installation or abort.")
			print("Note that the installation will ask before overwriting any files.")
			while(True):
				answer = input("Proceed? [y/n]: ")
				if answer == "y":
					return dest
				elif answer == "n":
					print("Backup failed. Aborting installation.")
					quit()
				else:
					print("Input y or n")
	else:
		print("Backup directory does not exist. Creating", dest)
		os.mkdir(dest)
		return dest

def backup(src):
	'''Backup'''
	if os.path.lexists(os.path.join(dest, src)):
		print("Backup file exists:", dest + src)
		print("Overwriting file. Backup if needed and then proceed.")
		while(True):
			answer = input("Overwrite? [y/n]: ")
			if answer == "y":
				if dorename(os.path.join(os.environ['HOME'], src), os.path.join(dest, src)):
					return True
				else:
					return False
			elif answer == "n":
				print("Backing up", dest + src, "aborted.")
				return False
			else:
				print("Input y or n")
	else:
		tmp = os.path.split(dest + src)
		if not os.path.lexists(tmp[0]):
			os.makedirs(tmp[0])
		if dorename(os.path.join(os.environ['HOME'], src), os.path.join(dest, src)):
			return True
		else:
			return False

def restore(target, restore_files):
	'''Restore'''
	bfilename = os.path.join(dest, target)
	filename = os.path.join(os.environ['HOME'], target)
	if doremove(filename):
		if restore_files:
			if dorename(bfilename, filename):
				return True
			else:
				return False
		else:
			return True
	else:
		return False

def installfiles():
	'''Check files'''
	for i in range(len(files)):
		linkto = os.path.abspath(files[i])
		bfilename = "." + os.path.basename(files[i])
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
						dosymlink(linkto, filename)
			elif os.path.isfile(filename):
				print("Target file exists. Backing up", filename)
				if backup(bfilename):
					print("Creating link", filename, "->", linkto)
					dosymlink(linkto, filename)
			else:
				print("File is no file O_o")
		else:
			print("File does not exist. Creating link:", filename, "->", linkto)
			dosymlink(linkto, filename)
		print("")

def getdirectories():
	'''Get directories'''
	filelist = []
	for i in range(len(directories)):
		filelist.append(directories[i])
		tmp = readdir(directories[i], os.path.join(directories[i], ""))
		for j in range(len(tmp)):
			filelist.append(tmp[j])
	return filelist

def readdir(path, prev):
	'''Reads directory recursive'''
	readdirfilelist = os.listdir(path)
	for i in range(len(readdirfilelist)):
		if prev != "":
			readdirfilelist[i] = prev + readdirfilelist[i]
		if os.path.isdir(readdirfilelist[i]):
			tmp = readdir(readdirfilelist[i], os.path.join(readdirfilelist[i], ""))
			for j in range(len(tmp)):
				readdirfilelist.append(tmp[j])
	return readdirfilelist

def filetypecheck(path):
	'''Check if directory'''
	typelist = []
	for i in range(len(path)):
		if os.path.isdir(path[i]):
			typelist.append("dir")
		elif os.path.isfile(path[i]):
			typelist.append("file")
	return typelist

def checkdirectories():
	'''Check directories'''
	for i in range(len(filetypelist)):
		bfilename = "." + filelist[i]
		filename = os.path.join(os.environ['HOME'], bfilename)
		if filetypelist[i] == "dir":
			if os.path.lexists(filename):
				if os.path.isdir(filename):
					print("Directory exists:", filename)
				elif os.path.isfile(filename):
					# Directory is file
					print("Directory is a file. Backing up", filename)
					if backup(bfilename):
						domkdir(filename)
			else:
				print("CREATE DIRECTORY")
				os.mkdir(filename)
		elif filetypelist[i] == "file":
			linkto = os.path.abspath(filelist[i])
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
								dosymlink(linkto, filename)
					else:
						print("Target file exists. Backing up", filename)
						if backup(bfilename):
							print("Creating link", filename, "->", linkto)
							dosymlink(linkto, filename)						
					
				elif os.path.isdir(filename):
					print("Target file is a directory. Backing up", filename)
					if backup(bfilename):
						print("Creating link", filename, "->", linkto)
						dosymlink(linkto, filename)
						
			else:
				print("File does not exist. Creating link", filename, "->", linkto)
				dosymlink(linkto, filename)
		print("")

def domkdir(dirname):
	'''Create directory and check for errors'''
	try:
		if not parser.values.pretend:
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

def dosymlink(target, linkname):
	'''Create symlink and check for errors'''
	try:
		if not parser.values.pretend:
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

def dorename(src, target):
	'''Rename file or directory and check for errors'''
	try:
		if not parser.values.pretend:
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

def doremove(target):
	'''Remove file and check for errors'''
	try:
		if not parser.values.pretend:
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

def doremdir(target):
	'''Remove directory and check for errors'''
	try:
		if not parser.values.pretend:
			rmdir(target)
		else:
			pass
	except OSError as err:
		print("Could not remove directory", filename)
		# No access
		if err.errno == errno.EACCES:
			print("Permission denied.")
		# Target is not a directory
		elif err.errno == errno.ENOTDIR:
			print("Target is not a directory:", filename)
		# Directory is not empty
		elif err.errno == errno.ENOTEMPTY:
			print("Directory is not empty and should not be removed:", filename)
		else:
			print("Unknown error. Error No:", err.errno)
		return False
	else:
		return True

def checkextrafiles():
	'''Check directories for files that will not be touched by the installation'''
	filelist = getdirectories()
	filelist.sort()
	filetypelist = filetypecheck(filelist)
	efilelist = directories
	for i in range(len(efilelist)):
		efilelist[i] = os.path.join(os.environ['HOME'], "." + efilelist[i])
		tmp = readdir(efilelist[i], efilelist[i] + "/")
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

def uninstallfiles(restore_files):
	'''Check files'''
	for i in range(len(files)):
		linkto = os.path.abspath(files[i])
		bfilename = "." + os.path.basename(files[i])
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

def clearbackupdirectory():
	'''Remove empty directories in backup directory'''
	if os.path.lexists(dest):
		if len(os.listdir(dest)) == 0:
			pass
		else:
			delbackuplist = readdir(dest, dest)
			delbackuplist.sort()
			for i in range(len(delbackuplist)):
				delbackuplist[i] = os.path.join(dest, delbackuplist[i])
			delbackupfiletypelist = filetypecheck(delbackuplist)
			for i in reversed(range(len(delbackuplist))):
				if delbackupfiletypelist[i] == "dir":
					try:
						if not parser.values.pretend:
							os.rmdir(delbackuplist[i])
						else:
							pass
					except OSError as err:
						if err.errno == errno.ENOTEMPTY:
							print("Directory is not empty and should not be removed:", delbackuplist[i])
						else:
							print(err)
			try:
				if not parser.values.pretend:
					os.rmdir(dest)
				else:
					pass
			except OSError as err:
				if err.errno == errno.ENOTEMPTY:
					print("Backup directory is not empty and will not be removed:", dest)
				else:
					print(err)
			else:
				print("Backup directory is empty and has been removed:", dest)
	else:
		pass

def uninstall():
	'''Uninstall files'''
	restore_files = False
	if os.path.lexists(dest):
		if len(os.listdir(dest)) == 0:
			print("Backup directory exists but is empty:", dest)
			print("No files to restore.")
		else:
			print("Backup directory is not empty:", dest)
			print("Restoring files")
			restore_files = True
	else:
		print("Backup directory does not exists:", dest)
		print("No files to restore.")
	print("")

	if len(files) > 0:
		print("")
		print("")
		print("UNINSTALLING FILES")
		print("")
		uninstallfiles(restore_files)

	if len(directories) > 0:
		print("")
		print("")
		print("UNINSTALLING DIRECTORIES")

		for i in range(len(filelist)):
			bfilename = "." + filelist[i]
			filename = os.path.join(os.environ['HOME'], bfilename)
			if filetypelist[i] == "file":
				linkto = os.path.abspath(filelist[i])
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
	
		for i in reversed(range(len(filelist))):
			bfilename = "." + filelist[i]
			filename = os.path.join(os.environ['HOME'], bfilename)
			if filetypelist[i] == "dir":
				if len(os.listdir(filename)) == 0:
					print("Directory empty:", filename)
					print("Removing:", filename)
					if dormdir(filename):
						print("Directory removed:", filename)
		print("")

	print("")
	clearbackupdirectory()
	print("")
	print("")
	print("UNINSTALLATION COMPLETE!")

if parser.values.extrafiles:
	checkextrafiles()
	quit()

if parser.values.pretend:
	print("PRETENDING:")

# Get backup directory
if parser.values.backup == None:
	dest = stdbackupdirectory
else:
	dest = parser.values.backup
	# Check if dest ends with separator. If not add it.
	if not dest.endswith(os.path._get_sep("")):
		dest = os.path.join(dest, "")

filelist = getdirectories()
filelist.sort()
for i in range(len(files)):
	try:
		filelist.remove(files[i])
	except ValueError:
		pass

filetypelist = filetypecheck(filelist)

if parser.values.uninstall:
	if len(directories) > 0 or len(files) > 0:
		uninstall()
	else:
		print("Nothing to uninstall.")
else:
	print("")
	print("")
	print("CHECKING BACKUP DIRECTORY")
	print("")
	checkbackup()
	if len(files) > 0:
		print("")
		print("")
		print("CHECKING FILES")
		print("")
		installfiles()
	if len(directories) > 0:
		print("")
		print("")
		print("CHECKING DIRECTORIES")
		print("")
		checkdirectories()

	print("")
	print("INSTALLATION COMPLETE")

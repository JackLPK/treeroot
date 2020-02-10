# Treeroot #

Treeroot is a script for generating empty files and directories. This script should be run with a 'structure file' to specify what files and/or directories you intend to create, for 'structure file', see `sample_files/structure_files`.

This script was originally created for testing purposes for one of my projects.

The idea of the name 'Treeroot' comes from the famous 'tree' command.


## Set up ##
There are 2 `.py` files: `treeroot.py` and `treerow.py`, see `src/treeroot.py` and `src/treerow.py`. Running `treeroot.py` with `treerow.py` in the same folder will work but might be a little bit troublesome. 
The recommanded way to use Treeroot is processing `treeroot.py` with PyInstaller first to create it as a single executable.

Note: beware of illegal characters for files and directories for the operating system.

### Structure file ###
A 'structure file' is needed for running this script. This file should contain text modelling or minicing the intended directory structure for creation. It is recommanded to not put files between consecutive directories.

Comments can be put into the structure file, start comments with `//`.

Note: directories cannot contain '.' and files should end with a '.' and file extension, except the relative root directory.

## Running ##
This script can be run as:

```
python treeroot.py structure_file
```
This would create the relative root directory in the current working directory, and child files and child directories under that directory.

If run as executable, the arguments are the same.

## Author ##
Pui Kit Li

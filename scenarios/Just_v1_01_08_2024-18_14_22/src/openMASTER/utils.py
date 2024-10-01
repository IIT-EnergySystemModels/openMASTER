import os.path
import shutil

def copy_and_overwrite(src, dst):
    # Create the subdirectory in the destination folder
    subdirectory = os.path.join(dst, os.path.basename(src))

    # If the subdirectory already exists, remove it
    if os.path.exists(subdirectory):
        shutil.rmtree(subdirectory)
        
    # Copy the contents of the source folder into the subdirectory
    shutil.copytree(src, subdirectory)

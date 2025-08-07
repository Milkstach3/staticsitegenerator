import shutil
import os
from CONSTANTS import SOURCE_DIR, DESTINATION_DIR


def copy_contents_recursive(source_dir=SOURCE_DIR, dest_dir=DESTINATION_DIR):
    # Make sure destination exists
    os.makedirs(dest_dir, exist_ok=True)

    # Copy everything from source to destination
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)  # copy2 preserves metadata

def delete_contents_recursive(dest_dir=DESTINATION_DIR):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        os.makedirs(dest_dir, exist_ok=True)
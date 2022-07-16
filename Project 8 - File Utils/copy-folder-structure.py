import shutil
import os

# ignore files in folder if present


def ignore_files(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]


# passing the src,dst,and ignore parameter
shutil.copytree('D:/original',
                'D:/new',
                ignore=ignore_files)

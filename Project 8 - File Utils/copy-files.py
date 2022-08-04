import glob
import shutil
import os

fileList = [
    'comma-separated list'
]


src_dir = "source_directory"
dst_dir = "destination_directory"
for fileName in fileList:
    try:
        shutil.copy(os.path.join(src_dir, fileName), dst_dir)
    except:
        print(fileName)
        continue

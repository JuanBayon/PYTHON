#!/usr/bin/env python3
from multiprocessing import Pool
import subprocess
import os

def run(task):
    # Do something with task here
    print("Handling {}".format(task))

if __name__ == "__main__":
    tasks = ['task1', 'task2', 'task3']
    # Create a pool of specific number of CPUs
    p = Pool(len(tasks))
    # Start each task within the pool     
    p.map(run, tasks)


"""
SUPPROCESS

src = "/data/prod/"
dest = "/data/prod_backup/"
subprocess.call(["rsync", "-arq", src, dest])
"""


#!/usr/bin/env python
global src
src = "{}/data/prod/".format(os.getenv("HOME"))

def sync_data(folder):
    dest = "{}/data/prod_backup/".format(os.getenv("HOME"))
    subprocess.call(["rsync", "-arq", folder, dest])
    print("Handling {}".format(folder))

if __name__ == "__main__":
    folders = []
    root = next(os.walk(src))[0]
    dirs = next(os.walk(src))[1]

    for dir in dirs:
        folders.append(os.path.join(root, dir))

    pool = Pool(len(folders)) if len(folders) != 0 else Pool(1) #aquí mejor el número de procesadores --> dejarlo en blanco pool = Pool()
    pool.map(sync_data, folders)



#!/usr/bin/env python3
from multiprocessing import Pool
import os
import subprocess

# 1 - Set SRC
src = "{}/data/prod".format(os.getenv("HOME"))

# 4 - Pool RSYNC commands
def runprocess(folder):
    dest = "{}/data/prod_backup".format(os.getenv("HOME"))
    subprocess.call(["rsync", "-arq", folder, dest])

# 2 - Set folders array
folders = []
for root, _dir, files in os.walk(src):
    for name in _dir:
        folders.append(os.path.join(root, name))

# 3 Build and run the Pool
p = Pool(len(folders))
p.map(runprocess, folders)




#!/usr/bin/env python3
src = "/home/student-01-#######/data/prod"
dirs = next(os.walk(src))[1]

def backingup(dirs):
    dest = "/home/student-01-#######/data/prod_backup"
    subprocess.call(["rsync", "-arq", src+'/'+ dirs, dest])




p = Pool(len(dirs))
p.map(backingup, dirs)
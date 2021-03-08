import pandas as pd
from multiprocessing import Pool
import subprocess as sp
import os
import time
import shutil
from zipfile import ZipFile
from os.path import basename

SV_DIR_BASE = "/driller/sv-benchmarks/c/"

def delete_folder(folder):
    if os.path.exists(folder) and os.path.isdir(folder):
        shutil.rmtree(folder)

def start_driller(task):
    # print(task)
    sp.run(["python", "start_driller", "-c", "1", "-d", "1", "-t", "900", "--memory", "15G", task])

def get_tasks(category):
    tasks = pd.read_csv("name_category.csv", header = 0)
    tasks = tasks[tasks["category"] == category]
    return [SV_DIR_BASE + task.replace("yml", "c") for task in tasks["sv-benchmarks"].values.tolist()]

def make_zip():
    folders = next(os.walk('output'))[1]
    for dir_name in folders:
        os.system("mkdir -p output_zip/{}".format(dir_name[:-2] + ".yml"))
        with ZipFile("output_zip/{}/test-suite.zip".format(dir_name[:-2] + ".yml"), 'w') as zipObj:
            for folderName, subfolders, filenames in os.walk("output/{}/".format(dir_name)):
                for filename in sorted(filenames):
                    print(filename)
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, basename(filePath))

if __name__ == '__main__':
    delete_folder("./work_dir")
    delete_folder("./output")
    p = Pool(processes = 14)
    start = time.time()
    tasks = get_tasks("ReachSafety-ControlFlow")
    async_result = p.map_async(start_driller, tasks)
    p.close()
    p.join()
    end = time.time()
    make_zip()
    print('total time (s)= ' + str(end-start))
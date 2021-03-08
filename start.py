import pandas as pd
from multiprocessing import Pool
import subprocess as sp
import os
import time
import shutil

SV_DIR_BASE = "/home/ethan/sv-benchmarks/c/"

def delete_folder(folder):
    if os.path.exists(folder) and os.path.isdir(folder):
        shutil.rmtree(folder)

def start_driller(task):
    # print(task)
    sp.run(["python", "start_driller", "-c", "1", "-d", "1", "-t", "30", task])

def get_tasks(category):
    tasks = pd.read_csv("name_category.csv", header = 0)
    tasks = tasks[tasks["category"] == category]
    return [SV_DIR_BASE + task.replace("yml", "c") for task in tasks["sv-benchmarks"].values.tolist()]


if __name__ == '__main__':
    delete_folder("./work_dir")
    delete_folder("./output")
    p = Pool(processes = 3)
    start = time.time()
    tasks = get_tasks("ReachSafety-ControlFlow")
    async_result = p.map_async(start_driller, tasks)
    p.close()
    p.join()
    end = time.time()
    print('total time (s)= ' + str(end-start))
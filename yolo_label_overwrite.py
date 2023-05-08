import os
import codecs
import argparse
import time
import re
import shutil

parser = argparse.ArgumentParser(
            description='label correction',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

parser.add_argument("input", help="path to input folder containing videos")

args = parser.parse_args()

def clear_toplevel(data_fpath):
    # delete all .txt files in data_fpath 
    for file in os.listdir(data_fpath):
        if os.path.isfile(f"{data_fpath}/{file}") and file.endswith(".txt"): 
            os.remove(f"{data_fpath}/{file}")

def overwrite_labels(data_fpath):
    yolo_dirs = []

    for directory in os.listdir(data_fpath):
        if os.path.isdir(f"{data_fpath}/{directory}") and directory.startswith("yolo"):
            yolo_dirs.append(directory)
    
    if len(yolo_dirs) > 1:
        print("Found:", yolo_dirs)
    else:
        print("Found recent YOLO labels", yolo_dirs)

        return
    
    yolo_dirname = yolo_dirs[:-1]
    print("Pulling from:", yolo_dirname)

    clear_toplevel(data_fpath)

    for file in os.listdir(f"{data_fpath}/{yolo_dirname}"):
        if os.isfile(file) and file.endswith(".txt"):
            shutil.move(f"{data_fpath}/{yolo_dirname}/{file}", f"{data_fpath}/{file}")

    os.rmdir(f"{data_fpath}/{yolo_dirname}")

if __name__ == "__main__":
    overwrite_labels(args.input)
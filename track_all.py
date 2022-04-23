#!/usr/bin/env python3


import argparse 
import yaml
import os 
import copy
import glob

description_text = 'How to trim videos'


parser = argparse.ArgumentParser(
        description=description_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("input", 
        help="path to input folder containing videos")

args = parser.parse_args()


if __name__ == "__main__":
    search_path = (os.path.join(args.input, "*.mp4"))
    for cfile in glob.glob(search_path):
        print(cfile)
        os.system("python3 tracking.py {} -t 1 -f 3".format(cfile))
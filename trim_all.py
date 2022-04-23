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
parser.add_argument("config_file",
        help="path to yaml config file folder")
parser.add_argument("input", 
        help="path to input folder containing videos")
parser.add_argument("output", 
        help="path to output folder to place trimmed videos")
args = parser.parse_args()


if __name__ == "__main__":
    search_path = (os.path.join(args.config_file, "*.yaml"))
    for cfile in glob.glob(search_path):
        print(cfile)
        os.system("python3 trim_videos.py {} {} {}".format(cfile, args.input, args.output))
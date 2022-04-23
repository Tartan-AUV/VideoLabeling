#!/usr/bin/env python3


import argparse 
import yaml
import os 
import copy
import glob
import shutil 

description_text = 'How to trim videos'


parser = argparse.ArgumentParser(
        description=description_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("input", 
        help="path to input folder containing tracked output videos")
parser.add_argument("output", 
        help="path to output folder containing videos")

args = parser.parse_args()


if __name__ == "__main__":
#     print(args.input)
#     print(os.listdir(args.input))
    for folder in os.listdir(args.input):
        if os.path.isdir(os.path.join(args.input, folder)):
                source_dir = os.path.join(args.input, folder)
                # print(source_dir)
                file_names = os.listdir(source_dir)
                
                for file_name in file_names:
                        try:
                                shutil.move(os.path.join(source_dir, file_name), args.output)
                        except:
                                print("File already exists")
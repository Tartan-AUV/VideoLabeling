#!/usr/bin/env python3

import argparse 
import csv
import os 
import random

description_text = 'Used to assign videos for labeling to people'


parser = argparse.ArgumentParser(
        description=description_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("output_file", type=argparse.FileType("w"),
        help="path to csv config file")
parser.add_argument("input", 
        help="path to input folder containing videos")

args = parser.parse_args()


if __name__ == "__main__":
    allFiles = [f for f in os.listdir(args.input) if (os.path.isfile(os.path.join(args.input, f)) and not f.startswith('.'))]
    allFiles = sorted(allFiles)
    allPeople = ['Sam', 'Theo', 'Katia', 'Sarah', 'Akshay', 'John', 'Micah', 'Rylan']
    random.shuffle(allPeople)
    multiplier = (len(allFiles) // len(allPeople)) + 1 
    allPeople = allPeople * multiplier
    allPeople = allPeople[:len(allFiles)]

    allPeople = sorted(allPeople)
    with open(args.output_file.name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zip(allFiles, allPeople))
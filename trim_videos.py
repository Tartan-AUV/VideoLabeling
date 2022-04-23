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
parser.add_argument("config_file",type=argparse.FileType("r"),
        help="path to yaml config file folder")
parser.add_argument("input", 
        help="path to input folder containing videos")
parser.add_argument("output", 
        help="path to output folder to place trimmed videos")
args = parser.parse_args()


def load_config():
    with open(args.config_file.name, "r") as stream:
        try:
            loaded_config = (yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
    return loaded_config

def process_configs(trims):
    newTimeline = []
    for key in trims.keys():
        for i, section in enumerate(trims[key]):
            if section[0] == -1:
                continue 
            newTimeline.append([section[0] + 1, section[1], [key]])
    sortedTimeline = (sorted(newTimeline))
    finalTimeline = []
    while(len(sortedTimeline) != 0):
        curElem = sortedTimeline[0]
        if len(finalTimeline) == 0:
            finalTimeline.append(curElem)
            sortedTimeline = sortedTimeline[1:]
        else:
            prevElem = finalTimeline[-1]
            if curElem[0] < prevElem[1]:
                
                if curElem[1] < prevElem[1]:
                    nextElem = copy.deepcopy(prevElem)
                    nextElem[0] = curElem[1]
                else:
                    nextElem = copy.deepcopy(curElem)
                    nextElem[0] = prevElem[1]
                    curElem[1] = prevElem[1]

                prevElem[1] = curElem[0]
                curElem[2] = curElem[2] + prevElem[2]
                sortedTimeline.append(nextElem)
            finalTimeline.append(curElem)
            sortedTimeline = sortedTimeline[1:]
        sortedTimeline = sorted(sortedTimeline)
    mergedTimeline = []
    for elem in finalTimeline:
        if elem[1] > elem[0]:
            mergedTimeline.append(elem)
    print(mergedTimeline)
    return (mergedTimeline)


def trim_videos(video_file, timeline):
    orig_video_name, ext = os.path.splitext((os.path.basename(video_file)))
    for i, elem in  enumerate(timeline):
        if (elem[1] - elem[0]) < 3:
            continue
        all_targets = "_".join(elem[2])
        new_video_name = "{}_{}_{}.mp4".format(orig_video_name, i, all_targets)
        new_video_file = os.path.join(args.output, new_video_name)
        trim_command = "ffmpeg -i {1} -ss 00:00:{0:02d} -to 00:00:{2:02d}   -async 1 {3} >/dev/null 2>&1".format(elem[0], video_file, elem[1], new_video_file)
        # print(trim_command)
        os.system(trim_command)
            
if __name__ == "__main__":
    loaded_config = load_config()
    video_name,_ = os.path.splitext((os.path.basename(args.config_file.name)))
    video_name = video_name + ".mp4"
    video_file = os.path.join(args.input, video_name)
    if not os.path.exists(video_file):
        print("ERROR: VIDEO FILE NOT FOUND: ", video_file)
    merged_timeline = process_configs(loaded_config)
    trim_videos(video_file, merged_timeline)

    

import os
import codecs
import argparse
import time
import re

parser = argparse.ArgumentParser(
            description='label correction',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

parser.add_argument("input", help="path to input folder containing videos")

args = parser.parse_args()

def fix_labels(data_fpath):
    data_fpath_yolo = f"{data_fpath}/yolo-labels-{time.time()}"
    os.mkdir(data_fpath_yolo)
        
    width, height = 1280, 720

    data_classes_tmp = open("data_classes.txt", "r").read().splitlines()
    data_classes = {}

    for i in range(len(data_classes_tmp)):
        data_classes[data_classes_tmp[i]] = i

    print("Data Classes:\n", data_classes)

    for file in os.listdir(data_fpath):
        if file.endswith(".txt"):
            with codecs.open(f"{data_fpath}/{file}", 'r', encoding='utf-8',
                             errors='ignore') as fdata:
                data = fdata.read().splitlines()
                data_clean = []

                for line in data:
                    if bool(re.match('^[a-zA-Z0-9\,\.]+$', line)) and line != "":
                        data_clean.append(line)
            
            fdata.close()

            new_obss = []

            try:
                for obs in data_clean:
                    indv_data = obs.split(",")
                    # print(indv_data)
                    indv_data_coords = indv_data[:len(indv_data) - 1]
                    # print(indv_data_coords)

                    x1, y1, x2, y2 = [float(x) for x in indv_data_coords]

                    data_class = data_classes[indv_data[len(indv_data) - 1]]
                    # print(x1, y1, x2, y2, data_class)

                    x_center = round( ((x2 + x1) / 2) / width, 6)
                    y_center = round(((y2 + y1) / 2) / height, 6)

                    bb_width = round(abs(x2 - x1) / width, 6)
                    bb_height = round(abs(y2 - y1) / height, 6)

                    new_obs = [int(data_class), x_center, y_center, bb_width, bb_height]
                    new_obss.append(new_obs)

                with codecs.open(f"{data_fpath_yolo}/{file}", 'w', encoding='utf-8',
                                errors='ignore') as fdata:
                    for obs in range(len(new_obss)):
                        f_line = ""
                        for elem in new_obss[obs]:
                            f_line += str(elem) + " "
                        if obs != len(new_obss) - 1:
                            fdata.write(f_line.strip() + "\n")
                        else:
                            fdata.write(f_line.strip())
            # except ValueError as e:
            #     print(f"Error: {e} in file {file}! Continuing...")
            except KeyError as e:
                print(f"Error: {e}! No such class.")
            fdata.close()


if __name__ == "__main__":
    fix_labels(args.input)
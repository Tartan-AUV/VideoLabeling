import os
import codecs
import argparse

parser = argparse.ArgumentParser(
            description='label correction',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

parser.add_argument("input", help="path to input folder containing videos")

args = parser.parse_args()

def fix_labels(data_fpath):
    width, height = 1280, 720

    data_classes_tmp = open("data_classes.txt", "r").read().splitlines()
    data_classes = {}

    for i in range(len(data_classes_tmp)):
        data_classes[data_classes_tmp[i]] = i

    print(data_classes)

    for file in os.listdir(data_fpath):
        if file.startswith("zed") and file.endswith(".txt"):
            # print(file)
            with codecs.open(data_fpath + "/" + file, 'r', encoding='utf-8',
                             errors='ignore') as fdata:

                data = fdata.read().splitlines()
            fdata.close()

            new_obss = []
            for obs in data:
                indv_data = obs.split(",")
                indv_data_coords = indv_data[:len(indv_data) - 1]

                x1, y1, x2, y2 = [float(x) for x in indv_data_coords]

                data_class = data_classes[indv_data[len(indv_data) - 1]]
                # print(x1, y1, x2, y2, data_class)

                x_center = round( ((x2 + x1) / 2) / width, 6)
                y_center = round(((y2 + y1) / 2) / height, 6)

                bb_width = round(abs(x2 - x1) / width, 6)
                bb_height = round(abs(y2 - y1) / height, 6)

                new_obs = [int(data_class), x_center, y_center, bb_width, bb_height]
                new_obss.append(new_obs)

            # print(new_obss)

            with codecs.open(data_fpath + "/" + file, 'w', encoding='utf-8',
                             errors='ignore') as fdata:
                for obs in range(len(new_obss)):
                    f_line = ""
                    for elem in new_obss[obs]:
                        f_line += str(elem) + " "
                    if obs != len(new_obss) - 1:
                        fdata.write(f_line.strip() + "\n")
                    else:
                        fdata.write(f_line.strip())
            fdata.close()


if __name__ == "__main__":
    fix_labels(args.input)
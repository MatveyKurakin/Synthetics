import os
import numpy as np
import cv2


def log(name: str, object: str, count: int, log_path: str) -> None:
    record = f'{name};{object};{count}\n'
    log_file = open(log_path + "\\" + "logs.txt", 'a')
    log_file.write(record)
    log_file.close()


def add_log(psd_path: str) -> None:
    psd_path += '\\PSD\\'
    files = [item for item in os.scandir(psd_path)]

    for item in files:
        if item.name.lower().endswith(".png"):

            label_map = cv2.imread(psd_path + item.name, cv2.IMREAD_GRAYSCALE)

            connectivity = 4
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(label_map, connectivity, cv2.CV_32S)

            log(item.name.split('.')[0], 'PSD', num_labels-1, path)


if __name__ == "__main__":
    path = "..\\..\\dataset\\test_dataset_no_noise"
    add_log(path)

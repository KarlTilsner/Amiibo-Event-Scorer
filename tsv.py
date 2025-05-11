import csv
import glob
import os

def openTSV(filename):
    arr = []
    with open(filename, encoding="utf-8") as file:
        data = csv.reader(file, delimiter="\t")
        next(data)
        for line in data:
            arr.append(line)
    return arr

def writeTSV(filename, data, header):
    with open(filename, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def getAllInFolder():
    folder_path = "./Tournament Records"
    tsv_files = glob.glob(os.path.join(folder_path, "*.tsv"))

    for file_path in tsv_files:
        print(file_path)
    
    return tsv_files

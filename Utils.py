"""Ewondo Transcription Transform API (ETTA)

Authors
 * St Germes Bengono Obiang 2023
"""

from csv import reader
import csv

import numpy


def readCSV(name):
    # open file in read mode
    result = []
    with open(name + '.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            # print(row[1])
            result.append(row[1])
    return result

def readCSV2Lab(name):
    # open file in read mode
    with open(name + '.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            with open('datas/labs/mono_cm_ewo_'+ row[0] + '.lab', "a") as f:
                f.write(str(row[1]))

def loadTone():
    # open file in read mode
    result = {}
    with open('tone.csv', 'r', encoding="utf-8") as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            # print(row[1])
            result[row[0]] = row[1].replace('_', '')
    return result


def builVoyell(base_voyell, tones):
    new_voyell = []
    # print("les voyelles" ,base_voyell)
    for voyell in base_voyell:
        new_voyell.append(voyell)
        for name, tone in tones.items():
            new_voyell.append(''.join((voyell, tone)))
        # if voyell is not 'e':
    # print("les voyelles", new_voyell)
    return new_voyell

def writeInFile(result, filename = 'result', ext = '.yml'):
    with open(filename + ext, "a") as f:
        f.write(str(result))
        f.write('\n')

def writeCSV(to_csv, file_name):
    keys = to_csv[0].keys()
    with open(file_name + '.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)

def writeDic(prons):
    with open("ewo_dic_simp.txt", "a", encoding="utf-8") as f:
        for pro in prons:
            f.write(pro['word'])
            f.write('\t')
            f.write(pro['prons'])
            f.write('\n')


def writeInFileArray(result):
    with open("sample.txt", "a") as f:
        data = f.read()
        f.write(str(result))
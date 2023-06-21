from csv import reader
import csv
import numpy as np

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

def wordStats():
    #Lecture du dataset
    sentences = readCSV('dataset')
    #Pour chaque ligne, splitter en fonction des espaces
    sent_len = np.array([len(x.split()) for x in sentences])
    print(sent_len)
    print('number of 1', np.count_nonzero(sent_len == 1))
    print('number of 2', np.count_nonzero(sent_len == 2))
    print('number of 3', np.count_nonzero(sent_len == 3))
    print('number of more than 3', np.count_nonzero(sent_len > 3))


wordStats()
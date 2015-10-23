import csv
import json

__author__ = 'Daniel Puschmann'


class DataReader(object):

    def __init__(self):
        pass


    def readCsv(self, file_name, delimiter=',', quotechar='\"'):
        with open(file_name, "rb") as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            keys = None
            data = []
            for row in reader:
                if keys is None:
                    keys = row
                    continue
                data_point = {key: value for (key, value) in zip(keys, row)}
                data.append(data_point)
            return data

    def readJson(self, file_name):
        with open(file_name, "rb") as json_file:
            file_content = ""
            for line in json_file:
                file_content += line#.replace("\\n","").replace("\\r","").replace("\\t","")
            data = json.loads(json.loads(file_content))
            return data

    def readJsonByRow(self,file_name):
        with open(file_name, "rb") as json_file:
            data = [json.loads(row) for row in json_file]
        return data

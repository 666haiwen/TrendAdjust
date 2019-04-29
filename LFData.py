import os
import csv
import json


class LFData(object):
    """
        Load the data of TrendData from disk to memeory.
        And translate them into csv files
    """
    def __init__(self, files, path='run/', settings='settings/'):
        self.path = path
        self.files = files
        self.settings = settings
        with open(self.settings + 'LF.json', 'r', encoding='utf-8') as fp:
            self.LF = json.load(fp)
    
    def read_lf_2_csv(self, file_name):
        with open(self.path + file_name + '.csv', 'w', newline='') as f:
            rows = []
            with open(os.path.join(self.path, file_name), 'r', encoding='gbk') as fp:
                for i, line in enumerate(fp):
                    rows.append(tuple(line.split(',')[:-1]))
            f_csv = csv.writer(f)
            f_csv.writerow(self.LF[file_name]['names'])
            f_csv.writerows(rows)

    def __call__(self):
        for file_name in self.files:
            self.read_lf_2_csv(file_name)
files = ['LF.L2', 'LF.L3', 'LF.L5', 'LF.L6']
lfData = LFData(files)
lfData()

import os
from utils import params_range,Tk_range


class TrendData(object):
    """
        Load the data of TrendData from disk to memeory.
        And check that the data is reasonable or not.
    """
    def __init__(self, path='template/', buses=None, generators=None, loads=None, transformers=None, acLinesData=None):
        self.path = path
        self.flag = True
        self.buses = self.__load_buses() if buses == None else buses
        self.generators = self.__load_generators() if generators == None else generators
        self.loads = self.__load_loads() if loads == None else loads
        self.transformers = self.__load_transformers() if transformers == None else transformers
        self.acLinesData = self.__load_ac_lines() if acLinesData == None else  acLinesData
    
    def getValue(self):
        return self.buses, self.generators, self.loads, self.transformers, self.acLinesData
    
    def getReasonable(self):
        return self.flag

    def __load_buses(self):
        buses = [None]
        with open(os.path.join(self.path,'LF.L1'), 'r', encoding='gbk') as fp:
            for line in fp:
                data = line.split(',')[:-1]
                buses.append({
                    'vBase': float(data[1])
                })
        return buses
    

    def __load_generators(self):
        generators = []
        flag = False
        with open(os.path.join(self.path,'LF.L5'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                data = line.split(',')[:-1]
                if (int(data[0]) not in [0, 1]):
                    print('Generators({}): \t The mark value is either 0 or 1'.format(i + 1))
                    self.flag = False
                if (int(data[2]) not in [0, 1, -1, -2, -3]):
                    print('The type value in line({}) of generators is not belong to [0, 1, -1, -2, -3]'.format(i + 1))
                    self.flag = False
                if int(data[2]) == 0:
                    flag = True
                P = float(data[3])
                Q = float(data[4])
                V = float(data[5])
                PMin = float(data[10])
                PMax = float(data[9])
                QMin = float(data[8])
                QMax = float(data[7])
                self.flag = params_range(P, PMin, PMax, 'P', 'generators', i + 1)
                self.flag = params_range(Q, QMin, QMax, 'Q', 'generators', i + 1)
                self.flag = params_range(V, 0.95, 1.05, 'V', 'generators', i + 1)
                generators.append({
                    'mark': int(data[0]),
                    'type': int(data[2]),
                    'Pg': P,
                    'Qg': Q,
                    'V0': V,
                    'QMax': QMax,
                    'QMin': QMin,
                    'PMax': PMax,
                    'PMin': PMin,
                    'data': data.copy()
                })
        if not flag:
            print('There is no generator\'s type value is 0!')
            self.flag = False
        return generators
    
    def __load_loads(self):
        loads = []
        with open(os.path.join(self.path,'LF.L6'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                data = line.split(',')[:-1]
                if (int(data[0]) not in [0, 1]):
                    print('loads({}): \t The mark value is either 0 or 1'.format(i + 1))
                    self.flag = False
                P = float(data[4])
                Q = float(data[5])
                PMin = float(data[11])
                PMax = float(data[10])
                QMin = float(data[9])
                QMax = float(data[8])
                self.flag = params_range(P, PMin, PMax, 'P', 'loads', i + 1)
                self.flag = params_range(Q, QMin, QMax, 'Q', 'loads', i + 1)
                loads.append({
                    'mark': int(data[0]),
                    'Pg': P,
                    'Qg': Q,
                    'QMax': QMax,
                    'QMin': QMin,
                    'PMax': PMax,
                    'PMin': PMin,
                    'data': data.copy()
                })
        return loads

    def __load_transformers(self):
        transformers = []
        with open(os.path.join(self.path,'LF.L3'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                data = line.split(',')[:-1]
                if (int(data[0]) not in [0, 1]):
                    print('Transformers({}): \t The mark value is either 0 or 1'.format(i + 1))
                    self.flag = False
                tkMin, tkMax = Tk_range(data, self.buses, i + 1)
                Tk = float(data[6])
                self.flag = params_range(Tk, tkMin, tkMax, 'TK', 'transformers', i + 1)
                transformers.append({
                    'mark': int(data[0]),
                    'i': int(data[1]),
                    'j': int(data[2]),
                    'Tk': Tk,
                    'data': data.copy()
                })
        return transformers
    
    def __load_ac_lines(self):
        acLinesData = []
        with open(os.path.join(self.path,'LF.L2'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                data = line.split(',')[:-1]
                if (int(data[1]) != int(data[2])):
                    if (int(data[0]) not in [0, 1, 2, 3]):
                        print('AC_Lines({}): \t The mark value isn\'t belong to [0, 1, 2, 3]'.format(i + 1))
                        self.flag = False
                elif (int(data[0]) not in [0, 1]):
                    print('AC_Lines({}): \t The mark value is either 0 or 1'.format(i + 1))
                    self.flag = False
                acLinesData.append({
                        'mark': int(data[0]),
                        'i': int(data[1]),
                        'j': int(data[2]),
                        'I': float(data[14]),
                        'data': data.copy()
                })
        return acLinesData

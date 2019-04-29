from TrendData import TrendData
from vertify import Vertify
from utils import Tk_range
from const import INTERVAL
import numpy as np
import os


class AdjustTrend(object):
    """
        The process of adjust trend data.
        @param:
            path: the path of template data to load
            runPath: the path of WMLFRTMsg.exe
            resPath: the path of reasonable output
            adjustType: the type of adjust(0: Auto, 1: Manually)
    """
    def __init__(self, path, runPath, resPath, adjustType=0):
        if adjustType not in [0, 1]:
            raise ValueError('The adjustType of AdjustTrend must be 0 or 1 not {}'\
                .format(adjustType))
        if adjustType == 0:
            self.trendData = TrendData(path=path)
            self.buses, self.generators, self.loads, self.transformers, self.acLinesData = self.trendData.getValue()
        self.type = adjustType
        self.path = path
        self.runPath = runPath
        self.resPath = resPath
        self.vertify = Vertify(runPath,resPath)
        self.adjustFunc = [self.__adjust_generators, self.__adjust_loads,\
             self.__adjust_transformers, self.__adjust_ac_lines]
        

    def __output(self):
        """
            1.vertify the reasonable of input data.
            2.write the adjust input data to the dst dirs
            3.vertify the reasonable of output
        """
        def fpWrite(fp, data):
            for s in data:
                fp.write(s + ',')
            fp.write('\n')

        # 1.step
        if self.trendData.getReasonable() == False:
            print('There are some error in the input data!')
            return
        # 2.step
        with open(os.path.join(self.runPath, 'LF.L5'), 'w+', encoding='utf-8') as fp:
            for v in self.generators:
                data = v['data']
                data[0] = str(v['mark'])
                data[2] = str(v['type'])
                data[3] = str(v['Pg'])
                data[4] = str(v['Qg'])
                data[5] = str(v['V0'])
                fpWrite(fp, data)

        with open(os.path.join(self.runPath, 'LF.L6'), 'w+', encoding='utf-8') as fp:
            for v in self.loads:
                data = v['data']
                data[0] = str(v['mark'])
                data[4] = str(v['Pg'])
                data[5] = str(v['Qg'])
                fpWrite(fp, data)
        
        with open(os.path.join(self.runPath, 'LF.L3'), 'w+', encoding='utf-8') as fp:
            for v in self.transformers:
                data = v['data']
                data[0] = str(v['mark'])
                data[6] = str(v['Tk'])
                fpWrite(fp, data)
        
        with open(os.path.join(self.runPath, 'LF.L2'), 'w+', encoding='utf-8') as fp:
            for v in self.acLinesData:
                data = v['data']
                data[0] = str(v['mark'])
                fpWrite(fp, data)
        # 3.step
        self.vertify(TrendData(buses=self.buses, generators=self.generators,\
             loads=self.loads, transformers=self.transformers, acLinesData=self.acLinesData))

    def __get_pq(self, data):
        pmax, pmin = data['PMax'], data['PMin']
        if pmax == 0:
            pmax = data['Pg'] + 5
        if pmin == 0:
            pmin = data['Pg'] - 5
        qmax, qmin = data['QMax'], data['QMin']
        if qmax == 0:
            qmax = data['Qg'] + 5
        if qmin == 0:
            qmin = data['Qg'] - 5
        pInterval = (pmax - pmin) / INTERVAL
        qInterval = (qmax - qmin) / INTERVAL
        return pmax, pmin, pInterval, qmax, qmin, qInterval

    def __adjust_generators(self, adjustList, i, value, auto):
        if auto == False:
            self.generators[i]['mark'] = value['mark']
            self.generators[i]['type'] = value['type']
            self.generators[i]['Pg'] = value['Pg']
            self.generators[i]['Qg'] = value['Qg']
            self.generators[i]['V0'] = value['V0']
        else:
            pmax, pmin, pInterval, qmax, qmin, qInterval = self.__get_pq(self.generators[i])
            vInterval = 10 / INTERVAL
            for mark in range(2):
                self.generators[i]['mark'] = mark
                for t in range(-3, 2):
                    self.generators[i]['type'] = t
                    if t == 0:
                        continue
                    for p in np.arange(pmin, pmax, pInterval):
                        self.generators[i]['Pg'] = p
                        if t == 1 or t == -3:
                            for q in np.arange(qmin, qmax, qInterval):
                                self.generators[i]['Qg'] = q
                                self.__adjust_hidden(adjustList)
                        else:
                            for v in range(INTERVAL + 1):
                                self.generators[i]['V0'] = (95 + v * vInterval) / 100
                                self.__adjust_hidden(adjustList)

    def __adjust_loads(self, adjustList, i, value, auto):
        if auto == False:
            self.loads[i]['mark'] = value['mark']
            self.loads[i]['Pg'] = value['Pg']
            self.loads[i]['Qg'] = value['Qg']
        else:
            pmax, pmin, pInterval, qmax, qmin, qInterval = self.__get_pq(self.loads[i])
            for mark in range(2):
                self.loads[i]['mark'] = mark
                for p in np.arange(pmin, pmax, pInterval):
                    self.loads[i]['Pg'] = p
                    for q in np.arange(qmin, qmax, qInterval):
                        self.loads[i]['Qg'] = q
                        self.__adjust_hidden(adjustList)

    def __adjust_transformers(self, adjustList, i, value, auto):
        if auto == False:
            self.transformers[i]['mark'] = value['mark']
            self.transformers[i]['Tk'] = value['Tk']
        else:
            for mark in range(2):
                self.transformers[i]['mark'] = mark
                minTk, maxTk = Tk_range(self.transformers[i], self.buses, i + 1)
                # default 10 intervals
                interval = (maxTk - minTk) / INTERVAL
                for times in range(INTERVAL + 1):
                    self.transformers[i]['Tk'] = minTk + interval * times
                    self.__adjust_hidden(adjustList)

    def __adjust_ac_lines(self, adjustList, i, value, auto):
        if auto == False:
            self.acLinesData[i]['mark'] = value['mark']
        else:
            if self.acLinesData[i]['i'] == self.acLinesData[i]['j']:
                for v in range(4):
                    self.acLinesData[i]['mark'] = v
                    self.__adjust_hidden(adjustList)
            else:
                for v in range(2):
                    self.acLinesData[i]['mark'] = v
                    self.__adjust_hidden(adjustList)

    def __adjust_hidden(self, adjustList):
        """
            Set every adjust step to a hidden func ==> Nesting loop
        """
        if len(adjustList) == 0:
            self.__output()
            return
        target = adjustList[0]['target']
        i = adjustList[0]['line'] - 1
        value = adjustList[0]['value']
        auto = adjustList[0]['auto']
        self.adjustFunc[target](adjustList[1:], i, value, auto)

    def get_lines(self, target):
        return len([self.generators, self.loads, self.transformers, self.acLinesData][target])

    def __call__(self, adjustList):
        if self.type == 1:
            self.trendData = TrendData(self.runPath)
        self.buses, self.generators, self.loads, self.transformers, self.acLinesData = self.trendData.getValue()
        self.__adjust_hidden(adjustList)

import os
from TrendData import TrendData
from shutil import copyfile


class Vertify(object):
    """
        Run the WMLFRTMsg.exe and get the result.
        If the result is reasonable, copy the input and output of the WMLFRTMsg.exe into resultsFiles
        @params:
            runPath: the path to the file with WMLFRTMsg.exe
            resPath: the path to the file store the reasonable result

    """
    def __init__(self, runPath, resPath):
        self.runPath = runPath
        self.resPath = resPath
        if not os.path.exists(resPath):
            os.makedirs(resPath)
        ## cd to the run file
        os.chdir(self.runPath)
        # the file doesn't be copied
        self.filesName = ['exe', 'dll', 'dat', 'DLL']
        
    
    def copy_res(self):
        """
            copy the input and output of reasonible case to the results file
        """
        dirs = os.listdir(self.resPath)
        dirsLength = len(dirs)
        while os.path.exists(os.path.join(self.resPath, str(dirsLength))):
            dirsLength += 1
        dstPath = os.path.join(self.resPath, str(dirsLength))
        os.makedirs(dstPath)
        dirs = os.listdir(self.runPath)
        for fileName in dirs:
            flag = True
            for systemFile in self.filesName:
                if systemFile in fileName:
                    flag = False
                    break
            if flag:
                srcFile = os.path.join(self.runPath, fileName)
                dstFile = os.path.join(dstPath, fileName)
                copyfile(srcFile, dstFile)

    
    def __call__(self, inputData):
        """
            run the WMLFRTMsg.exe and vertify the results are reasonable or not.
            @param:
                inputData: data of input files, type = TrendData
        """
        os.system('WMLFRTMsg.exe')
        with open(os.path.join(self.runPath,  'LF.CAL'), 'r', encoding='gbk') as fp:
            firstLine = fp.readline()
            data = firstLine.split(',')
            if int(data[0]) == 0:
                print('The result doesn\'t converge!')
                return False
        # bus
        with open(os.path.join(self.runPath,  'LF.LP1'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                if i == 0:
                    continue
                data = line.split(',')
                v = float(data[1])
                if v > 1.05 or v < 0.95:
                    print('The voltage({}) of the busId({}) is out of range.'\
                        .format(v, i + 1))
                    return False
        # AC lines
        with open(os.path.join(self.runPath,  'LF.LP2'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                data = line.split(',')
                Lf2 = inputData.acLinesData[i]
                if int(Lf2.data[14]) == 0:
                    continue
                Pi = float(data[3])
                Qi = float(data[4])
                Pj = float(data[5])
                Qj = float(data[6])
                Ui = inputData.buses[Lf2['i']]['vBase']
                Uj = inputData.buses[Lf2['j']]['vBase']
                if Pi ** 2 + Qi ** 2 > (Ui * Lf2['I']) ** 2:
                    print('The Pi ** 2 +Qi ** 2 out of Range in line({}) of LF.LP2'\
                        .format(i + 1))
                    return False
                if Pj ** 2 + Qj ** 2 > (Uj * Lf2['I']) ** 2:
                    print('The Pj ** 2 +Qj ** 2 out of Range in line({}) of LF.LP2'\
                        .format(i + 1))
                    return False
        # Transformer
        with open(os.path.join(self.runPath,  'LF.LP3'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                data = line.split(',')
                Lf3 = inputData.transformers[i]
                if int(Lf3.data[18]) == 0:
                    continue
                Pi = float(data[3])
                Qi = float(data[4])
                Pj = float(data[5])
                Qj = float(data[6])
                S = float(Lf3.data[18])
                if Pi ** 2 + Qi ** 2 > S ** 2:
                    print('The Pi ** 2 +Qi ** 2 out of Range in line({}) of LF.LP3'\
                        .format(i + 1))
                    return False
                if Pj ** 2 + Qj ** 2 > S ** 2:
                    print('The Pj ** 2 +Qj ** 2 out of Range in line({}) of LF.LP3'\
                        .format(i + 1))
                    return False
        # Generator
        with open(os.path.join(self.runPath,  'LF.LP5'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                data = line.split(',')
                Lf5 = inputData.generators[i]
                Pg = float(data[1])
                Qg = float(data[2])
                if Pg < Lf5['PMin'] or Pg > Lf5['PMax']:
                    print('The Pg({}) of line({}) in LF.LP5 out of range([{}, {}])'\
                        .format(Pg, i + 1, Lf5['PMin'], Lf5['PMax']))
                    return False
                if Qg < Lf5['QMin'] or Pg > Lf5['QMax']:
                    print('The Qg({}) of line({}) in LF.LP5 out of range([{}, {}])'\
                        .format(Qg, i + 1, Lf5['QMin'], Lf5['QMax']))
                    return False
        # Load
        with open(os.path.join(self.runPath,  'LF.LP6'), 'r', encoding='gbk') as fp:
            for i, line in enumerate(fp):
                data = line.split(',')
                Lf6 = inputData.loads[i]
                Pg = float(data[2])
                Qg = float(data[3])
                if Pg < Lf6['PMin'] or Pg > Lf6['PMax']:
                    print('The Pg({}) of line({}) in LF.LP6 out of range([{}, {}])'\
                        .format(Pg, i + 1, Lf6['PMin'], Lf6['PMax']))
                    return False
                if Qg < Lf6['QMin'] or Pg > Lf6['QMax']:
                    print('The Qg({}) of line({}) in LF.LP6 out of range([{}, {}])'\
                        .format(Qg, i + 1, Lf6['QMin'], Lf6['QMax']))
                    return False
                
        self.copy_res()
        return  True


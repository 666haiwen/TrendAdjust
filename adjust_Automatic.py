import os
from adjust import AdjustTrend
from const import *

adjustProcess = AdjustTrend(templatePath, runPath, resPath)

print('Adjust trendData of input files.....')
adjustList = []
while (True):
    target = 7
    while target not in [0,1,2,3,4,5]:
        print('\nPlease input 0-4;  0:generators(LF.L5)    1:loads(LF.L6)\n' + \
            '                     2:transformers(LF.L3)  3:acLiniesData(LF.L2)\n' + \
            '                     4: run    5:exit')
        target = int(input('input = '))
    if target == 5:
        print('Exit!')
        break
    if target == 4:
        print(adjustList)
        adjustProcess(adjustList)
        adjustList = []
        continue
    line = 0
    lineMax = adjustProcess.get_lines(target)
    while line < 1 or line > lineMax:
        print('please input the line of data to change( range:[1: {}], int)'.format(lineMax))
        line = int(input('line = '))
        if line < 1 or line > lineMax:
            print('{} out of range [1: {}]'.format(line, lineMax))

    adjustList.append({
        'target': target,
        'value': {},
        'line': line,
        'auto': True
    })
    # adjustList = [
    #     {
    #         'target': 'generators',
    #         'value': {
    #             'mark': 1
    #         },
    #         'line': 1,
    #         'auto': True
    #     },
    #     {
    #         'target': 'acLines',
    #         'value': {},
    #         'line': 3,
    #         'auto': True
    #     },
    #     {
    #         'target': 'loads',
    #         'value': {},
    #         'line': 3,
    #         'auto': True
    #     }
    # ]

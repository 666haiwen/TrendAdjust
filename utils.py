def Tk_range(data, buses, line):
    """
        calculate the Tk range of input data.
        @params:
            data: the one line data of transformer, type:list
            buses: the all buses data of trend data, type:list
            line: the index line of transformers
        @returns:
            min, max: float, the range of Tk adjusted
    """
    minV = float(data[26])
    maxLevel = int(data[27])
    minLevel = int(data[28])
    curLevel = int(data[29])
    levelDiff = float(data[30])
    Vj1 = (1-(minLevel - curLevel) * levelDiff) * minV
    Vj2 = (1-(maxLevel - curLevel) * levelDiff) * minV
    Vi = float(data[25])
    i = int(data[1])
    j = int(data[2])
    Vib = buses[i]['vBase']
    Vjb = buses[j]['vBase']
    if Vi == 0:
        print('Transformers({}) :\t Viact is zero!'.format(line))
        return 0, 0
    Tk1 = Vj1 / Vjb / Vi * Vib
    Tk2 = Vj2 / Vjb / Vi * Vib
    return min(Tk1, Tk2), max(Tk1, Tk2)


def params_range(x, vMin, vMax, content, typeName, line):
    """
        Justify the x vaule is in the range or not.
        params:
            x: the value to adjust, float
            vMin: the min value of x, float
            vMax: the max value of x, float
            content: the content of adjusted, [type, P, Q, V, Tk]
            typeName: the type name of node in the network, [generators, loads, transformers]
            line: the number of line in the input data
        return:
            res: True or False.
    """
    if vMax == vMin == 0:
        return True
    if x < vMin or x > vMax:
        print('{}({}): \t The {} = {} is out of range[{}, {}]'\
            .format(typeName, line, content, x, vMin, vMax))
        return False
    return True

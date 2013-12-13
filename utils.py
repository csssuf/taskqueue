def casefix(s):
    if type(s) != type('placeholder'):
        raise TypeError
    se = s.split('_')
    for i in range(len(se)):
        stemp = se[i]
        stemp = stemp[0].upper() + stemp[1:]
        se[i] = stemp
    if len(se) > 1:
        fs = ''
        for j in se:
            fs += j + ' '
        return fs[:len(fs)-1]
    else:
        return se[0]

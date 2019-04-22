import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
"""
signal --> 5 in a row
noise --> no 5 in a row

/more accurate or not/
hit --> choose 16.5 when hitting 5 in a row
false alarm --> choose 16.5 when not hitting 5 in a row

/choosing larger one or not/
hit --> choose larger one when hitting 5 in a row
false alarm --> choose larger when not hitting 5 in a row
"""

data = pd.read_csv('~/Desktop/untitled/data/second.csv')
rowcount = data.shape[0]

# data.plot()
# plt.show(block=True)


# class Subject:
#     def __init__(self, id, pretrial_sr):
#         self.id = id
#         self.baseline = pretrial_sr
#
# class Trial:
#     def __init__(self, trial_num, trial_sr, pair_num, oe, ue, ce):
#         self.trialnum = trial_num
#         self.trialsr = trial_sr
#         self.pairnum = pair_num
#         self.oe = oe
#         self.ue = ue
#         self.ce = ce
#
# class Pair:
#     def __init__(self, pair_id, opt1, opt2, result):
#         self.pairid = pair_id
#         self.opt1 = opt1
#         self.opt2 = opt2
#         self.result = result

# class Result:
#     def __init__(self, oe, ue, ce, cl, cs):
#         self.oe = oe
#         self.ue = ue
#         self.ce = ce
#         self.cl = cl
#         self.cs = cs

def checkPairNum(data,row):
    pairnum = 1
    isFirsttrial = np.all(pd.notnull(data.loc[[row], ['id']]))
    if np.all(pd.notnull(data.loc[[row], ['Trial number']])) or isFirsttrial:
        for i in range(8):
            # print(data.loc[[i+row+1], ['Trial number']])
            if isFirsttrial:
                target = i + row + 2
                # print("here:", row)
            else:
                target = i + row + 1
                # print("errr:", row)
            if (target < rowcount) and np.all(pd.isnull(data.loc[[target], ['Trial number', 'id']])):
                pairnum += 1
            else:
                break
    else:
        print('Not start of trial: ', row)
    # print('row: ', row)
    # print('pairnum:', pairnum)
    return pairnum

# def checkTrialNumber(data, row):
#     tn = 0
#     if np.all(pd.notnull(data.loc[[row],['id']])):
#         while

def checkOE(data, row, pairnum):
    oe = 0
    for i in range(pairnum):
        result = data.loc[[row+i], ['Type']].values
        # print('res: ', result)
        opt1 = data.loc[[row+i], ['Option 1']].values
        # print('opt1: ', opt1)
        opt2 = data.loc[[row+i], ['Option 2']].values
        # print('opt2: ', opt2)

        if (opt1 > 16.5 or opt2 > 16.5) and result == 0:
            oe += 1
    return oe


def checkUE(data, row, pairnum):
    ue = 0
    for i in range(pairnum):
        result = data.loc[[row+i],  ['Type']].values
        opt1 = data.loc[[row+i], ['Option 1']].values
        opt2 = data.loc[[row+i], ['Option 2']].values

        if (opt1 < 16.5 or opt2 < 16.5) and result == 0:
            ue += 1
    return ue


def checkCE(data, row, pairnum):
    ce = 0
    for i in range(pairnum):
        result = data.loc[[row+i], ['Type']].values
        if result == 1:
            ce += 1
    return ce


def chooseLarger(data, row, pairnum):
    cl = 0
    for i in range(pairnum):
        result = data.loc[[row+i], ['Type']].values
        opt1 = data.loc[[row + i], ['Option 1']].values
        opt2 = data.loc[[row + i], ['Option 2']].values

        if (opt1 < 16.5 or opt2 < 16.5) and result == 1:
            cl += 1
        elif (opt1 > 16.5 or opt2 > 16.5) and result == 0:
            cl += 1
    return cl


def chooseSmaller(data, row, pairnum):
    cs = 0
    for i in range(pairnum):
        result = data.loc[[row + i], ['Type']].values
        opt1 = data.loc[[row + i], ['Option 1']].values
        opt2 = data.loc[[row + i], ['Option 2']].values

        if (opt1 < 16.5 or opt2 < 16.5) and result == 0:
            cs += 1
        elif (opt1 > 16.5 or opt2 > 16.5) and result == 1:
            cs += 1
    return cs

def booLarger(data, row):
    boo = 0
    # print('current row:', row)
    if np.all(pd.notnull(data.loc[[row], ['id']])):
        print('Input is id line')
    else:
        result = data.loc[[row], ['Type']].values
        opt1 = data.loc[[row], ['Option 1']].values
        opt2 = data.loc[[row], ['Option 2']].values

        # choose smaller
        if ((opt1 < 16.5 or opt2 < 16.5) and result == 0) \
            or ((opt1 > 16.5 or opt2 > 16.5) and result == 1):
            boo = 0
        # choose larger
        elif ((opt1 < 16.5 or opt2 < 16.5) and result == 1) \
            or ((opt1 > 16.5 or opt2 > 16.5) and result == 0):
            boo = 1
    return boo

def addResult(data):
    resList = []
    for r in range(rowcount):
        if np.all(pd.isnull(data.loc[[r], ['Type']])):
            resList.append(0)
        else:
            type = data.loc[[r], ['Type']].values
            opt1 = data.loc[[r], ['Option 1']].values
            opt2 = data.loc[[r], ['Option 2']].values

            if type == 1:
                resList.append(16.5)
            elif type == 0 and opt1 == 16.5:
                resList.append(opt2)
            elif type == 0 and opt2 == 16.5:
                resList.append(opt1)
            else:
                print('errrr')
    data['Result'] = resList
    return


def perceivedTarget(data, row, pairnum):
    total = 0
    if np.all(pd.notnull(data.loc[[row], ['id']])):
        row += 1
    for i in range(pairnum):
        total += data.loc[[row+i], ['Result']].values
        # print('incre: ', data.loc[[row+i], ['Result']].astype('float64'))
        # print(total)
    return (total/pairnum).astype('float64')



# def readSubjects(data):
#     for row in rowcount:
#         sid = 0
#         if data.loc[row,'id'] != 0:
#             id = data.loc[row,'id']
#             baseline = data.loc[row,'Pretrial sr']
#             sid = Subject(id, baseline)
#         else:
#             continue
#         sid = sid + 1

# def findTrials(sid, trial_num):
#     for r in rowcount:
#         if (data.loc[[r],['id']] == sid) and (data.loc[[r],['Trial number']] == trial_num):
#             trialnum = data.loc[[r],['Trial number']]
#             trial_sr = data.loc[[r],['Trial sr']]
#             pairnum = checkPairNum(data, r)
#             oe = checkOE(data, r, pairnum)
#             ue = checkUE(data, r, pairnum)
#             ce = checkCE(data, r, pairnum)


def assignCurrentsr(r):
    cur_sr = 0
    if np.all(pd.isnull(data.loc[[r], ['Trial number']])):
        cur_sr = data.loc[[r], ['Pretrial sr']].values
    else:
        cur_sr = data.loc[[r], ['Trial sr']].values
    return cur_sr

def assignNextsr(r,pairnum):
    next_sr = 0
    # stop if exceeding rowcount
    if r + pairnum >= rowcount:
        next_sr = 6666
        # print('No next trial')
    # enter next person if all trials are accessed
    elif np.all(pd.notnull(data.loc[[r+pairnum], ['id']])):
        next_sr = 7777
    elif np.all(pd.isnull(data.loc[[r], ['Trial number']])) and r + pairnum < rowcount:
        next_sr = data.loc[[r+1], ['Trial sr']].values
        # print('1')
    elif np.all(pd.notnull(data.loc[[r], ['Trial number']])) and r + pairnum < rowcount:
        next_sr = data.loc[[r + pairnum], ['Trial sr']].values
        # print('2')
    return next_sr


def calculateNextAll():
    it = 0          # increase total
    ioit = 0        # increase prob of overestimate if sr increases
    iodt = 0
    dt = 0          # decrease total
    iudt = 0
    iuit = 0
    icdt = 0
    icit = 0

    ilit = 0        # increase prob of choosing larger if sr increases
    isit = 0        # increase prob of choosing smaller if sr increases
    ildt = 0
    isdt = 0

    ipit = 0        # perceived target size increased if sr increases
    dpdt = 0

    for r in range(rowcount):
        print('r: ', r)
        if np.all(pd.notnull(data.loc[[r], ['Trial number']])) or np.all(pd.notnull(data.loc[[r], ['id']])):
            pairnum = checkPairNum(data, r)
            cur_sr = assignCurrentsr(r)
            next_sr = assignNextsr(r, pairnum)
            # print('next_sr: ', next_sr)

            if next_sr == 7777:
                continue
            if next_sr != 6666:
                cur_oe = checkOE(data, r, pairnum)
                next_oe = checkOE(data, r + pairnum, pairnum)
                cur_ue = checkUE(data, r, pairnum)
                next_ue = checkUE(data, r + pairnum, pairnum)

                cur_cl = chooseLarger(data, r, pairnum)
                next_cl = chooseLarger(data, r + pairnum, pairnum)
                cur_cs = chooseSmaller(data, r, pairnum)
                next_cs = chooseSmaller(data, r + pairnum, pairnum)

                cur_pt = perceivedTarget(data, r, pairnum)
                next_pt = perceivedTarget(data, r + pairnum, pairnum)

                cur_ce = checkCE(data,r,pairnum)
                next_ce = checkCE(data, r+pairnum,pairnum)

                # print('r: ', r)
                # print('cur_oe', cur_oe)
                # print('next_oe', next_oe)
                # print('cur_cl: ', cur_cl)
                # print('next_cl: ', next_cl)
                # print('cur_cs: ', cur_cs)
                # print('next_cs: ', next_cs)

                if next_sr > cur_sr:
                    it += 1
                    # it += 1 * pairnum
                    if next_oe > cur_oe:
                        ioit += 1
                    elif next_ue > cur_ue:
                        iuit += 1
                    elif next_ce > cur_ce:
                        icit += 1

                    if next_cl > cur_cl:
                        ilit += 1
                    elif next_cs > cur_cs:
                        isit += 1

                    if next_pt > cur_pt:
                        ipit += 1

                elif next_sr < cur_sr:
                    dt += 1
                    # dt += 1 * pairnum
                    if next_oe > cur_oe:
                        iodt += 1
                    elif next_ue > cur_ue:
                        iudt += 1
                    elif next_ce > cur_ce:
                        icdt += 1

                    if next_cl > cur_cl:
                        ildt += 1
                    elif next_cs > cur_cs:
                        isdt += 1

                    if next_pt < cur_pt:
                        dpdt += 1
            else:
                break
        else:
            continue

    print('prob of increase chances of overestimation if success rate increases:', ioit/it)
    print('prob of increase chances of underestimation if success rate decreases:', iudt/dt)
    print('prob of increase chances of choosing the correct size if success rate increases:', icit/it)
    print('prob of increase chances of choosing the correct size if success rate decreases:', icdt/dt)

    # print('prob of increase oe if sr decreases: ', iodt/dt)
    # print('prob of increase ue if sr increases: ', iuit/it)

    print('prob of increase chances of choosing larger option if success rate increases:', ilit/it)
    print('prob of increase chances of choosing smaller option if success rate decreases:', isdt/dt)
    # print('prob of increase cl if sr decreases: ', ildt/dt)
    # print('prob of increase cs if sr increases: ', isit/it)

    print('prob of increased perceived target size if success rate increases:', ipit/it)
    print('prob of decreased perceived target size if success rate decreases:', dpdt/dt)


    # print('cl: ', ilit)
    # print('cs: ', isdt)


def calculateNextnf():
    it = 0          # increase total
    ioit = 0        # increase prob of overestimate if sr increases
    iodt = 0
    dt = 0          # decrease total
    iudt = 0
    iuit = 0
    icdt = 0
    icit = 0

    ilit = 0        # increase prob of choosing larger if sr increases
    isit = 0        # increase prob of choosing smaller if sr increases
    ildt = 0
    isdt = 0

    ipit = 0        # perceived target size increased if sr increases
    dpdt = 0

    for r in range(rowcount):
        print('r: ', r)
        if np.all(pd.notnull(data.loc[[r], ['Trial number']])) or np.all(pd.notnull(data.loc[[r], ['id']])):
            pairnum = checkPairNum(data, r)
            cur_sr = assignCurrentsr(r)
            next_sr = assignNextsr(r, pairnum)
            # print('cur_sr:', cur_sr)
            # print('next_sr:', next_sr)

            if next_sr == 7777:
                continue
            if next_sr != 6666:
                if data.loc[[r], ['Five hits']].values == 1 \
                        or data.loc[[r+1], ['Five hits']].values == 1\
                        or data.loc[[r+pairnum], ['Five hits']].values == 1:
                    continue
                else:
                    cur_oe = checkOE(data, r, pairnum)
                    next_oe = checkOE(data, r + pairnum, pairnum)
                    cur_ue = checkUE(data, r, pairnum)
                    next_ue = checkUE(data, r + pairnum, pairnum)

                    cur_cl = chooseLarger(data, r, pairnum)
                    next_cl = chooseLarger(data, r + pairnum, pairnum)
                    cur_cs = chooseSmaller(data, r, pairnum)
                    next_cs = chooseSmaller(data, r + pairnum, pairnum)

                    cur_pt = perceivedTarget(data, r, pairnum)
                    next_pt = perceivedTarget(data, r + pairnum, pairnum)

                    cur_ce = checkCE(data,r,pairnum)
                    next_ce = checkCE(data, r+pairnum,pairnum)

                    # print('r: ', r)
                    print('cur_sr:', cur_sr)
                    print('next_sr:', next_sr)
                    # print('cur_oe', cur_oe)
                    # print('next_oe', next_oe)
                    # print('cur_cl: ', cur_cl)
                    # print('next_cl: ', next_cl)
                    # print('cur_cs: ', cur_cs)
                    # print('next_cs: ', next_cs)

                    if next_sr > cur_sr:
                        it += 1
                        # it += 1 * pairnum
                        if next_oe > cur_oe:
                            ioit += 1
                        elif next_ue > cur_ue:
                            iuit += 1
                        elif next_ce > cur_ce:
                            icit += 1

                        if next_cl > cur_cl:
                            ilit += 1
                        elif next_cs > cur_cs:
                            isit += 1

                        if next_pt > cur_pt:
                            ipit += 1

                    elif next_sr < cur_sr:
                        dt += 1
                        # dt += 1 * pairnum
                        if next_oe > cur_oe:
                            iodt += 1
                        elif next_ue > cur_ue:
                            iudt += 1
                        elif next_ce > cur_ce:
                            icdt += 1

                        if next_cl > cur_cl:
                            ildt += 1
                        elif next_cs > cur_cs:
                            isdt += 1

                        if next_pt < cur_pt:
                            dpdt += 1
            else:
                break
        else:
            continue

    print('prob of increase chances of overestimation if success rate increases:', ioit/it)
    print('prob of increase chances of underestimation if success rate decreases:', iudt/dt)
    print('prob of increase chances of choosing the correct size if success rate increases:', icit/it)
    print('prob of increase chances of choosing the correct size if success rate decreases:', icdt/dt)

    # print('prob of increase oe if sr decreases: ', iodt/dt)
    # print('prob of increase ue if sr increases: ', iuit/it)

    print('prob of increase chances of choosing larger option if success rate increases:', ilit/it)
    print('prob of increase chances of choosing smaller option if success rate decreases:', isdt/dt)
    # print('prob of increase cl if sr decreases: ', ildt/dt)
    # print('prob of increase cs if sr increases: ', isit/it)

    print('prob of increased perceived target size if success rate increases:', ipit/it)
    print('prob of decreased perceived target size if success rate decreases:', dpdt/dt)


    # print('cl: ', ilit)
    # print('cs: ', isdt)


def sizePlotting(data, row):
    # r = start row of subject (id)
    if np.all(pd.notnull(data.loc[[row], ['id']])):
        if np.all(pd.notnull(data.loc[[row + 17], ['id']])):
            slicedf = data.loc[row+1:row + 16, ['Result']].copy().astype('float64')
            slicedf.plot()
            plt.show(block=True)
        else:
            slicedf = data.loc[row+1:row + 32, ['Result']].copy().astype('float64')
            print(slicedf)
            slicedf.plot()
            plt.show(block=True)


def avgSize():
    total_five, count_five = (0,0)
    total_nofive, count_nofive = (0,0)
    total_anf, total_bnf, count_anf, count_bnf = (0,0,0,0)
    total_fcl,total_nfcl = (0,0)
    total_fcs, total_nfcs = (0,0)
    total_anfcl, total_bnfcs = (0,0)
    total_anfcs, total_bnfcl = (0,0)

    for r in range(rowcount):
        if np.all(pd.isnull(data.loc[[r], ['Five hits']])):
            continue
        else:
            pairnum = checkPairNum(data, r)
            trialsr = data.loc[[r], ['Trial sr']].values
            for i in range(pairnum):
                larger = booLarger(data,r+i)
                if data.loc[[r], ['Five hits']].values == 1:
                    total_five += data.loc[[r+i],['Result']].values
                    # print('five: ', data.loc[[r+i],['Result']].values)
                    if larger == 1:
                        total_fcl += 1
                    else:
                        total_fcs += 1
                    count_five += 1
                else:
                    total_nofive += data.loc[[r + i], ['Result']].values
                    # print('nofive: ', data.loc[[r+i],['Result']].values)
                    if larger == 1:
                        total_nfcl += 1
                    else:
                        total_nfcs += 1
                    count_nofive += 1
                    # print('trialsr:', trialsr)
                    if trialsr >= 0.5:
                        total_anf += data.loc[[r + i], ['Result']].values
                        # print('anf: ', data.loc[[r + i], ['Result']].values)
                        if larger == 1:
                            total_anfcl += 1
                        else:
                            total_anfcs += 1
                        count_anf += 1
                    else:
                        total_bnf += data.loc[[r + i], ['Result']].values
                        # print('bnf: ', data.loc[[r + i], ['Result']].values)
                        if larger == 1:
                            total_bnfcl += 1
                        else:
                            total_bnfcs += 1
                        count_bnf += 1



    avg_five = (total_five / count_five).astype('float64')
    avg_nofive = (total_nofive / count_nofive).astype('float64')
    avg_anf = (total_anf / count_anf).astype('float64')
    avg_bnf = (total_bnf / count_bnf).astype('float64')

    prob_fcl = (total_fcl / count_five)
    prob_fcs = (total_fcs / count_five)
    prob_nfcl = (total_nfcl / count_nofive)
    prob_nfcs = (total_nfcs / count_nofive)
    prob_anfcl = (total_anfcl / count_anf)
    prob_anfcs = (total_anfcs / count_anf)
    prob_bnfcl = (total_bnfcl / count_bnf)
    prob_bnfcs = (total_bnfcs / count_bnf)

    print('Averaged perceived size when hitting 5 in a row: ', avg_five)
    print('Averaged perceived size when not hitting 5 in a row: ', avg_nofive)
    print('Averaged perceived size when for nf trials where sr > 0.5: ', avg_anf)
    print('Averaged perceived size when for nf trials where sr < 0.5: ', avg_bnf)

    print('Prob of choosing larger in streak trials: ', prob_fcl)
    print('Prob of choosing larger in non-streak trials: ', prob_nfcl)
    print('Prob of choosing smaller in streak trials: ', prob_fcs)
    print('Prob of choosing smaller in non-streak trials: ', prob_nfcs)
    print('Prob of choosing larger in nf trials where sr > 0.5: ', prob_anfcl)
    print('Prob of choosing larger in nf trials where sr < 0.5: ', prob_bnfcl)
    print('Prob of choosing smaller in nf trials where sr > 0.5: ', prob_anfcs)
    print('Prob of choosing smaller in nf trials where sr < 0.5: ', prob_bnfcs)




def accuracySDT(row, cutoff):
    fone,ftwo,fthree,ffour,ffive = (0,0,0,0,0)
    nfone, nftwo, nfthree, nffour, nffive = (0,0,0,0,0)

    anfone, anftwo, anfthree, anffour, anffive = (0, 0, 0, 0, 0)
    bnfone,bnftwo,bnfthree,bnffour,bnffive = (0,0,0,0,0)
    sid = 0

    if np.all(pd.isnull(data.loc[[row], ['id']])):
        print('Not at the first line of the subject')
    else:
        sid = data.loc[[row], ['id']].values
        row += 1
        for i in range(32):
            if np.all(pd.notnull(data.loc[[row+i], ['Five hits']])):
                print('Current analyzing trial is : ', row+i)
            if np.all(pd.notnull(data.loc[[row+i], ['id']])):
                print('Reached next subject: ', row+i)
                break

            result = data.loc[[row+i], ['Result']].values
            if np.all(pd.notnull(data.loc[[row+i], ['Trial sr']])):
                trialsr = data.loc[[row+i], ['Trial sr']].values
            if np.all(pd.notnull(data.loc[[row+i], ['Five hits']])):
                curfive = data.loc[[row+i], ['Five hits']].values

            if curfive == 1:
                if result == 16:
                    fone += 1
                elif result == 16.25:
                    ftwo += 1
                elif result == 16.75:
                    fthree += 1
                elif result == 17:
                    ffour += 1
                else:
                    ffive += 1
            else:
                if result == 16:
                    nfone += 1
                elif result == 16.25:
                    nftwo += 1
                elif result == 16.75:
                    nfthree += 1
                elif result == 17:
                    nffour += 1
                else:
                    nffive += 1

                if trialsr >= cutoff:
                    if result == 16:
                        anfone += 1
                    elif result == 16.25:
                        anftwo += 1
                    elif result == 16.75:
                        anfthree += 1
                    elif result == 17:
                        anffour += 1
                    else:
                        anffive += 1
                else:
                    if result == 16:
                        bnfone += 1
                    elif result == 16.25:
                        bnftwo += 1
                    elif result == 16.75:
                        bnfthree += 1
                    elif result == 17:
                        bnffour += 1
                    else:
                        bnffive += 1

    print('Subject id: ', sid)
    print('anf1: ', anfone)
    print('anf2: ', anftwo)
    print('anf3: ', anfthree)
    print('anf4: ', anffour)
    print('anf5: ', anffive)
    print('bnf1: ', bnfone)
    print('bnf2: ', bnftwo)
    print('bnf3: ', bnfthree)
    print('bnf4: ', bnffour)
    print('bnf5: ', bnffive)


def largerSDT(row, cutoff):
    fhit, ffa = (0,0)
    nfhit, nffa = (0, 0)
    sid = 0

    if np.all(pd.isnull(data.loc[[row], ['id']])):
        print('Not at the first line of the subject')
    else:
        sid = data.loc[[row], ['id']].values
        row += 1
        for i in range(32):
            if np.all(pd.notnull(data.loc[[row + i], ['Five hits']])):
                print('Current analyzing trial is : ', row + i)
            if np.all(pd.notnull(data.loc[[row + i], ['id']])):
                print('Reached next subject: ', row + i)
                break

            result = data.loc[[row + i], ['Result']].values
            larger = booLarger(data,row+i)
            if np.all(pd.notnull(data.loc[[row + i], ['Trial sr']])):
                trialsr = data.loc[[row + i], ['Trial sr']].values
            if np.all(pd.notnull(data.loc[[row + i], ['Five hits']])):
                curfive = data.loc[[row + i], ['Five hits']].values

            if curfive == 1:
                if larger == 1:
                    fhit += 1
            else:
                if larger == 1:
                    ffa += 1

                if trialsr >= cutoff:
                    if larger == 1:
                        nfhit += 1
                else:
                    if larger == 1:
                        nffa += 1

    print('Subject id:', sid)
    print('fhit: ', fhit)
    print('ffa: ', ffa)
    print('nfhit: ', nfhit)
    print('nffa: ', nffa)




addResult(data)

# largerSDT(0,0.5)
# largerSDT(33,0.5)
# largerSDT(50,0.5)
# largerSDT(83,0.5)
# largerSDT(116,0.5)

# print(booLarger(data,130))

# accuracySDT(0,0.5)
# accuracySDT(33,0.5)
# accuracySDT(50,0.5)
# accuracySDT(83,0.5)
# accuracySDT(116,0.5)

# calculateNextAll()
# calculateNextnf()

avgSize()

# sizePlotting(data,0)
# sizePlotting(data,33)
# sizePlotting(data,50)
# sizePlotting(data,83)
# sizePlotting(data,116)

# slicedf = data.loc[1:16, ['Result']].copy()
# slicedf.astype(str).astype(int)
# print(data['Result'])
# print(pd.to_numeric(data['Result'], errors='coerce'))

# r = 0
# pn = checkPairNum(data,r)
# next = assignNextsr(r,pn)
# print('next_sr: ', next)
# cur = assignCurrentsr(r)
# print(cur, ',', next)
# pt = perceivedTarget(data, r, pn)
# print(pt)
 # -*- coding: utf-8 -*-
"""This module contains the helper functions needed by the project"""
import time
import json
import random
import os
from psychopy import gui

def get_order(id_):
    """Return the order of 3 modulaties
    in which they will be presented"""
    assert type(id_) == int and id_ >= 0
    n = id_ % 6
    if n == 0:
        return ('v', 'a', 's')
    elif n == 1:
        return ('a', 's', 'v')
    elif n == 2:
        return ('s', 'a', 'v')
    elif n == 3:
        return ('v', 's', 'a')
    elif n == 4:
        return ('a', 'v', 's')
    else:
        return ('s', 'v', 'a')

def get_dominant_stimulie(id_):
    """Return value is of the form "ijk" where
    i,j,k are in {1,2}. The interpretation of
    return value "ijk" is that stim i is dominant
    for visual mode, j for auditory mode and k
    for semantic mode. There are 8 possible return 
    values, for id_ = 0 mod 8, "111" is returned, 
    for id_ = 1 mod 8, "112" and so on."""
    assert type(id_) == int and id_ >= 0
    n = id_ % 8
    encode = {"1": "0", "2": "1"}
    decode = {"0": "1", "1": "2"}
    if n == 0:
        return "111"
    last = "".join([encode[i] for i in 
                    get_dominant_stimulie(n-1)])
    rslt = add_1(last)
    return "".join([decode[i] for i in rslt])
    
def add_1(xs):
    """xs is a string representing a binary number.
    returns a result of a binary addition: xs + 1
    >>> add_1("11")
    100
    """
    if xs == "":
        return "1"
    elif xs[-1] == "0":
        return xs[0:-1] + "1"
    else:
        return add_1(xs[:-1]) + "0"

def timestamp():
    yr, mon, day, hr, min_, sec = map(str, time.localtime()[0:6])
    date = day + '-' + mon + '-' + yr 
    time_ = hr + "-" + min_ + "-" + sec
    return "{0}_{1}".format(date, time_)

def save_data(data, partial=False):
    """If partial is True then save partial data to insure against the crash."""
    id_ = data.get('id')
    run = data.get('run')
    play = data.get('play')
    date = timestamp()
    #dir_ = "../subjects_data/partial_data/" if partial else "../subjects_data/" 
    dir_ = os.path.join(os.path.dirname(__file__), '..', 'subjects_data')
    if partial: dir_ = os.path.join(dir_, 'partial_data')
    if run:
        file_ = "id-{0}_run-{1}_date-{2}_choice_data.json".format(id_, run, date)
    elif play:
        file_ = "id-{0}_date-{1}_play_data.json".format(id_, date)
    else:
        file_ = "id-{0}_date-{1}_training_data.json".format(id_, date)
    fl = open(os.path.join(dir_, file_),  "w")
    json.dump(data, fl)
    fl.close()

def dialog_box(choice_task = False):
    """Present the dialog box and wait for user to enter id and 
    run number if it is a choice task."""
    dlg = gui.Dlg(title="MMECON Experiment")
    dlg.addText('Subject info')
    dlg.addField("ID")
    if choice_task: dlg.addField("Run")
    dlg.show()  # show dialog and wait for OK or Cancel
    if dlg.OK:  # if the user pressed OK
        try:
            return map(int, dlg.data)
        except: # field not filled with integer.
            dialog_box(choice_task)
    else: # user pressed cancel
        return None

def get_outcomes(max_outcome):
    """Return a tuple (low, high), s.t 0 < low < high <= max_outcome.
    Subject will be given a choice between gambles low with 85% vs high with 65%.
    Constraints:
    1. 50% of the times high EV is associated with 85% chance and rest of the times
    with 65% times.
    2. 50% of the times EV of both the gambles is low, as well Del(EV) is also low.
    other 50% of the gambles should have Del(EV) high as well as one outcome
    is closer to max_outcome.
    3. The priority heuristic always chooses low with 85% over high with 65%, so
    choose (low, high) s.t EV of later is higher, to compare the two models.
   
    All 3 constraints can not be met, for a while (low, high) are such that, 20% of
    times ev ratio is high and 80% low, if ev ratio is low then 50% of times, higher
    ev is associated with weaker stim and 50% with dominant stim."""
    high_ev = 0.2 # proportion of trial with high ev ratio

    # higher ev ratio case
    # high is within 90% of max_outcome and low is 1/3 to 1/2 of high,
    # so ev ratio is between 1.5 to 2.3
    if random.uniform(0, 1) < high_ev: 
        high = random.choice(range(int(0.9*max_outcome), 
                                   max_outcome+1))
        low = random.choice(range(int(high/3.0), int(high/2.0)+1))
        return (low, high)

    # lower ev ratio case, high is high is between 50% to 80% of max
    high = random.choice(range(int(0.5*max_outcome), 
                               int(0.8*max_outcome)+1))
    # case1, higer ev is associated with dominant stim
    # i.e 0.85 * low > 0.65 * high, i.e low > 0.76*high
    if random.uniform(0, 1) < 0.5:
        low = random.choice(range(int(0.76*high), high))
    else: # case 2, higher ev is associated with weaker stim
        low = random.choice(range(int(0.6*high), int(0.76*high)+1))
    return low, high

def random_choices4play(id_, nchoice):
    """randomly select a run generated by the choice_task and from that
    randomly select nchoice choices from each modualies to be played 
    for real. The return value is a dictionary of a form:
    rslt['Visual'] = [{'stim': 1, 'amount': 10}, {'stim': 2, 'amount': 20}]
    """

    def extract_choices(trials):
        """helper function, trials is a list generated by choice_task for a 
        particular modulaty, returns a list of dictionary with keys 'stim'
        and 'amount'. """
        rslts = []
        other = {1: 2, 2: 1} # other[1] = 2, other[2] = 1
        for trial in trials:
            first_stim = trial.get('first_stim', 
                                   other.get(trial.get('second_stim')))
            second_stim = trial.get('second_stim', other[first_stim])
            rslt = {}
            # if the subjece did not pressed any key then she still gets 
            # to play the second_stim.
            if trial['key'] == "left":
                rslt['stim'] = first_stim
                rslt['amount'] = trial["left_outcome"]
            else:
                rslt['stim'] = second_stim
                rslt['amount'] = trial["right_outcome"]
            rslts.append(rslt)
        return rslts
    
    files = get_data_files(id_)
    if not files:
        print "Choice data not found, did you give the correct id?"
        return
    fl = random.choice(files) # choose a run randomly
    data = json.load(open("../subjects_data/" + fl))
    rslt = {}
    for block in ["Visual", "Auditory", "Semantic"]:
        rslt[block] = extract_choices(random.sample(data[block]['trials'], 
                                                    nchoice))
    return rslt

def get_data_files(id_, dir_="../subjects_data", ptrn="choice_data"):
    """Return data files of a subject with id=id_(either choice_data 
    or training_data) generated by the corresponding program."""
    return [fl for fl in os.listdir(dir_) if 
            fl.find("id-" + str(id_) + "_") != -1 and
            fl.find(ptrn) != -1]

def random_binary_generator(p, k=3):
    """return a function 'generator' which returns a 0 or 1, 1 is return with
    a probability p. After every k'th time, generator returns a binary number
    which makes the proportion of 1 returns so far closest to p"""
    assert p >=0 and p <= 1 and type(k) == int and k >=1
    history = []
    def generator():
        n = len(history)
        dist = lambda x, y: abs(x-y)
        if n % k == 0:
            rslt = 1 if dist(sum(history)+1, (n+1)*p) < \
                   dist(sum(history), (n+1)*p) else 0
        else:
            rslt = int(random.uniform(0, 1) < p)
        history.append(rslt)
        return rslt
    return generator

def random_binary_generator2(p, q=0.5):
    """return a function 'generator' which returns a 0 or 1.
    With probability 1 - q generator returns 1 with prob p and
    with probability q generator returns a binary number
    which makes the proportion of 1 returns so far closest to p"""
    assert p >=0 and p <= 1 and q >= 0 and q <= 1
    history = []
    def generator():
        n = len(history)
        dist = lambda x, y: abs(x-y)
        if random.uniform(0, 1) < q:
            rslt = 1 if dist(sum(history)+1, (n+1)*p) < \
                   dist(sum(history), (n+1)*p) else 0
        else:
            rslt = int(random.uniform(0, 1) < p)
        history.append(rslt)
        return rslt
    return generator

class SummaryChoiceData(object):
    def __init__(self, data):
        self.data = data
        self.dominant_stimulie = get_dominant_stimulie(data['id'])
        
    def main(self):
        #file_name = '../subjects_data/choice-summary-id-%s.txt'%self.data['id']
        dir_ = os.path.join(os.path.dirname(__file__), '..', 'subjects_data')
        file_name = 'choice-summary-id-%s.txt'%self.data['id']
        fl = open(os.path.join(dir_, file_name), 'a')
        fl.write("Dominant Stimulie: %s\n\n"%self.dominant_stimulie)
        fl.write("\t\tRun%s\n\t\t===\n"%self.data['run'])
        for i,mode in enumerate(["Visual", "Auditory", "Semantic"]):
            fl.write("%s\n========\n"%mode)
            fl.write(self._summary(mode, self.dominant_stimulie[i]))
        fl.write("\n\n")
            
    def _summary(self, mode, dominant_stimulus):
        rslt = ""
        trials = self.data[mode]['trials']
        for i, trial in enumerate(trials):
            rslt += "\t trial %s\n\t -------\n"%i
            pleft, pright = (0.85, 0.65) if \
                            dominant_stimulus == str(trial['first_stim']) else \
                            (0.65, 0.85)
            oleft, oright = trial['left_outcome'], trial['right_outcome']
            rslt += "({0}, {1})\t({2}, {3})\n".format(pleft, oleft, pright, oright)
            rslt += "EVS: {0} \t   {1}\n".format(pleft*oleft, pright*oright)
            rslt += "choice: %s\n"%trial['key']
            rslt += "first_stim: %s\n"%trial['first_stim']
        return rslt

class Delay(object):
    """jittered delay between 1.5-7.5 sec, average 2.5 sec.
    THERE WILL BE 28 TRIALS PER BLOCK (VISUAL, AUDITORY, SEMANTIC), 3 BLOCKS. """
    def __init__(self, isfmri=True, ntrial=28, trial_fixed_dur=4.5):
        self.delays = 2*sim_jitter_delays(ntrial) if isfmri else \
                      [1] * ntrial # TOdo need modification here
        self.counter = 0
        self.trial_fixed_dur = trial_fixed_dur

    def next(self):
        rslt = self.delays[self.counter]
        self.counter += 1
        return rslt
    
    def adjust(self, trial_dur):
        expected_dur = self.trial_fixed_dur + sum(self.delays[self.counter-2:
                                                              self.counter])
        excess = trial_dur - expected_dur
        try:
            self.delays[self.counter] -= excess/2.0
            self.delays[self.counter+1] -= excess/2.0
            return None
        except IndexError: # this was the last trial
            return excess

def sim_jitter_delays(n=28, mean=2.5, min_=1.5, max_=7.5):
    truncatedp = lambda x: min_ < x and x < max_
    average = lambda xs: sum(xs)/float(len(xs))
    def trunc_exp():
        rslt = random.expovariate(1.0/mean)
        if truncatedp(rslt):
            return rslt
        elif rslt < min_:
            return min_ + random.uniform(0, mean - min_)
        else:
            return max_ - random.uniform(0, max_ - mean)
    while True:
        rslt = [trunc_exp() for i in range(n-1)]
        nth = n * mean - sum(rslt)
        if truncatedp(nth):
            rslt.append(nth)
            return [round(x, 5) for x in rslt]

def sim_jitter_delays2(n=28, mean=2.5, min_=1.5, max_=7.5):

    truncatedp = lambda x: min_ < x and x < max_

    def trunc_exp():
        rslt = random.expovariate(1.0/mean)
        if truncatedp(rslt):
            return rslt
        elif rslt < min_:
            return min_ + random.uniform(0, mean - min_)
        else:
            return max_ - random.uniform(0, max_ - mean)

    rslt = [trunc_exp() for i in range(n-1)]
    nth = n * mean - sum(rslt)
    if truncatedp(nth):
        rslt.append(nth)
        return [round(x, 5) for x in rslt]
    else:
        return sim_jitter_delays(n, mean, min_, max_)
            

if __name__ == "__main__":
    print sim_jitter_delays(n=10)

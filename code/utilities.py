"""This module contains the helper functions needed by the project"""
import time
import json
import random
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
    time_ = hr + ":" + min_ + ":" + sec
    return "{0}_{1}".format(date, time_)

def save_data(data):
    id_ = data.get('id')
    run = data.get('run')
    date = timestamp()
    dir_ = "../subjects_data/"
    if run:
        file_ = "id:{0}_run:{1}_date:{2}_choice_data.json".format(id_, run, date)
    else:
        file_ = "id:{0}_date:{1}_training_data.json".format(id_, date)
    fl = open(dir_+file_, "w")
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
    Subject will be given a choice between gambles 85% low vs 65% high. 
    With 50% chance, return (low, hight) s.t EV of both gambles are low as well
    as both outcomes are much lower then max_outcome. With other 50% chance
    return gamble with high difference in EV as well as high is close to
    max_outcome.
    The priority heuristic always chooses low with 85% over high with 65%, so
    choose (low, high) s.t EV of later is higher, to compare the two models."""
    assert max_outcome > 10
    ev_ratio = random.choice(["big", "small"])
    if ev_ratio == 'big':
        # high is within 80% of max_outcome
        high = random.choice(range(int(0.8*max_outcome), max_outcome+1))
    else:
        # high is between 40% to 60% of max_outcome
        high = random.choice(range(int(0.4*max_outcome), int(0.6*max_outcome)+1))
    # For PH to have different prediction then EV, low should be 
    # s.t 0.85 * low < 0.65 * high
    low = random.choice(range(1, int(0.65 * high / 0.85)))
    return (low, high)


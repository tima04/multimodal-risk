"""This module contains the helper functions needed by the project"""
import time
import json
from psychopy import gui

def get_order(id_):
    """Return the order of 3 modulaties
    in which they will be presented"""
    assert type(id_) == int and id_ >= 0
    n = id_ % 6
    if n == 0:
        return ('v', 'a', 's')
    elif n == 1:
        return ('v', 's', 'a')
    elif n == 2:
        return ('s', 'a', 'v')
    elif n == 3:
        return ('s', 'v', 'a')
    elif n == 4:
        return ('a', 'v', 's')
    else:
        return ('a', 's', 'v')

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

def save_data(id_, data):
    date = timestamp()
    dir_ = "../subjects_data/"
    file_ = "training_id:{0}_date:{1}.json".format(id_, date)
    fl = open(dir_+file_, "w")
    json.dump(data, fl)
    fl.close()

def dialog_box():
    """Present the dialog box and wait for user to enter id"""
    dlg = gui.Dlg(title="MMECON Experiment")
    dlg.addText('Subject info')
    dlg.addField("ID")
    dlg.show()  # show dialog and wait for OK or Cancel
    if dlg.OK:  # if the user pressed OK
        info = dlg.data
        id_ = info[0]
        try:
            id_ = int(info[0])
        except:
            dialog_box()
    else:
        return None
    return id_

import random
import time
import training
from psychopy import core, visual, event, sound
from abc import ABCMeta, abstractmethod
from parameters import *
from pygame import mixer
from utilities import *

def main():
    data = {'start_time': timestamp()}
    try:
        data['id'] = dialog_box()[0]
    except:
        return None
    win = visual.Window([800, 600], allowGUI=True, units='deg',
                        color = "grey",fullscr=FULLSCREEN, monitor="testMonitor")
    dominant_stimulie = get_dominant_stimulie(data['id'])
    choices = random_choices()
    blocks =  [Visual(win, dominant_stimulie[0], choices["Visual"]),
               Auditory(win, dominant_stimulie[1], choices["Auditory"]), 
               Semantic(win, dominant_stimulie[1], choices["Semantic"])]
    for block in blocks:
        print block.play()

def random_choices():
    rslt = {}
    rslt['Visual'] = [{'stim': 1, 'amount': 10}, {'stim': 2, 'amount': 20}]
    rslt['Auditory'] = [{'stim': 1, 'amount': 15}, {'stim': 2, 'amount': 17}]
    rslt['Semantic'] = [{'stim': 2, 'amount': 18}, {'stim': 1, 'amount': 16}]
    return rslt

class Play(training.Training):
    def __init__(self, win, dominant_stimulus, choices):
        training.Training.__init__(self, win, dominant_stimulus)
        self.win = win
        self.choices = choices
        self.stimulus1_text = ""
        self.stimulus2_text = ""

    def play(self):
        corrects = []
        for choice in self.choices:
            self.show_choice_info(choice)
            stim = choice['stim']
            if stim == 1:
                self._render_stimulus(self.stimulus1)
            else:
                self._render_stimulus(self.stimulus2)
            key, duration = self._get_key()
            correctp = self._give_feedback(key, stim)
            corrects.append(correctp)
            self._show_inter_trial_win()
        return corrects
    
    def show_choice_info(self, choice):
        stim = self.stimulus1_text if choice['stim'] == 1 \
               else self.stimulus2_text
        txt = "You chose to play a gamble which pays Euro %s if you correctly \
        classify a %s. Please press any key to continue"%(choice['amount'], stim)
        visual.TextStim(self.win, text=txt, pos=(0, 0)).draw()
        self.win.flip()
        event.waitKeys()
        
class Visual(Play, training.Visual):
    def __init__(self, win, dominant_stimulus, stims):
        Play.__init__(self, win, dominant_stimulus, stims)
        training.Visual.__init__(self, win, dominant_stimulus)
        self.stimulus1_text = "blue egg"
        self.stimulus2_text = "red egg"

class Auditory(Play, training.Auditory):
    def __init__(self, win, dominant_stimulus, stims):
        Play.__init__(self, win, dominant_stimulus, stims)
        training.Auditory.__init__(self, win, dominant_stimulus)
        self.stimulus1_text = "ba sound"
        self.stimulus2_text = "lu sound"


class Semantic(Play, training.Semantic):
    def __init__(self, win, dominant_stimulus, stims):
        Play.__init__(self, win, dominant_stimulus, stims)
        training.Semantic.__init__(self, win, dominant_stimulus)
        self.stimulus1_text = "Herbivore"
        self.stimulus2_text = "Carnivore"


        
if __name__=="__main__":
    main()

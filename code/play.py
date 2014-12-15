# -*- coding: utf-8 -*-
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
    data['play'] = True
    try:
        data['id'] = dialog_box()[0]
    except:
        return None
    win = visual.Window([800, 600], allowGUI=True, units='deg',
                        color = "grey",fullscr=FULLSCREEN, monitor="testMonitor")
    dominant_stimulie = get_dominant_stimulie(data['id'])
    choices = random_choices(data['id'], NPLAY)
    blocks =  [Visual(win, dominant_stimulie[0], choices["Visual"]),
               Auditory(win, dominant_stimulie[1], choices["Auditory"]), 
               Semantic(win, dominant_stimulie[1], choices["Semantic"])]
    data['choices'] = choices
    data['total_win'] = 0
    for block in blocks:
        corrects = block.play()
        for i in range(0, len(corrects)):
            if corrects[i]:
                data['total_win'] += choices[str(block)][i]['amount']
            data['choices'][str(block)][i]['correctp'] = corrects[i]
    data['finish_time'] = timestamp()
    save_data(data)
    txt = u"You win 10 percent of \u20AC %s."%data['total_win']
    visual.TextStim(win, text=txt, pos=(0,0)).draw()
    win.flip()
    event.waitKeys()


class Play(training.Training):
    def __init__(self, win, dominant_stimulus, choices):
        training.Training.__init__(self, win, dominant_stimulus)
        self.win = win
        self.choices = choices

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
        txt = u"Correct classification in the next %s task will win you \u20AC%s. Please press any key to continue"%(self.__str__().lower(), choice['amount'])

        visual.TextStim(self.win, text=txt, pos=(0, 0)).draw()
        self.win.flip()
        event.waitKeys()

        
class Visual(Play, training.Visual):
    def __init__(self, win, dominant_stimulus, stims):
        Play.__init__(self, win, dominant_stimulus, stims)
        training.Visual.__init__(self, win, dominant_stimulus)


class Auditory(Play, training.Auditory):
    def __init__(self, win, dominant_stimulus, stims):
        Play.__init__(self, win, dominant_stimulus, stims)
        training.Auditory.__init__(self, win, dominant_stimulus)


class Semantic(Play, training.Semantic):
    def __init__(self, win, dominant_stimulus, stims):
        Play.__init__(self, win, dominant_stimulus, stims)
        training.Semantic.__init__(self, win, dominant_stimulus)

        
if __name__=="__main__":
    main()

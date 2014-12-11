"""
There are 3 modulaties, visual, auditory and semantic. The order in
which they are presented to a subject is determined by the subject's id.
The function get_order takes subject's id modulo 6 and returns the order.

For each modulaties there are 2 sitmulus, stim1 and stim2, stim1 (stim2) has
a higher probability of belonging to the left(right) dragon. One of the
stimulus is dominant and anther is weaker, meaning that given
a stimuls, probability of correctly classifying a dragon to which 
it belongs is higher for the dominant stimulus then for the weaker one. 
The dominant and weaker stimulus are a function of a subject's id.
Dominant stimulie are "ijk" meant that stim i is
dominant for visual mode, stim j for auditory and stim k for semantic,
(i, j, k are in {1, 2}). The function dominant_stimulie takes id modulo
8 as an argument and returns the dominant stimulus, eg: dominant_stimulie(0)
= "111".
stim1 is blue_egg for visual mode, herbivore for semantic mode
and dragon1_sound for auditory mode.
"""

import random
import time
from psychopy import core, visual, event, sound
from abc import ABCMeta, abstractmethod
from parameters_training import *
from pygame import mixer
from utilities import get_order, get_dominant_stimulie, timestamp, \
    save_data, dialog_box

def main():
    data = {'start_time': timestamp()}

    id_ = dialog_box()
    if not id_:
        return None
    data['id'] = id_
    
    win = visual.Window([800, 600], allowGUI=True, units='deg',
                        color = "grey",fullscr=False, monitor="testMonitor")
    mixer.init(channels=2)

    order = get_order(id_)
    dominant_stimulie = get_dominant_stimulie(id_)
    data['order'] = order
    data['dominant_stimulie'] = dominant_stimulie

    def init(arg):
        assert arg in ('v', 'a', 's')
        if arg == 'v': 
            return Visual(win, dominant_stimulie[0])
        elif arg == 's': 
            return Semantic(win, dominant_stimulie[1])
        else:
            return Auditory(win, dominant_stimulie[2])
    blocks = [init(arg) for arg in order]

    for block in blocks:
        rslt = block.start_trial()
        data[str(block)] = rslt

    data['finish_time'] = timestamp()
    save_data(id_, data)

    win.close()
    core.quit()

class Training(object):
    """
    Abstract class. Visual, auditory and semantic training are
    3 concrete representation.
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self, win, dominant_stimulus):
        "stimulus1 and 2 are to be defined in concrete classes"
        self.win = win
        # assigning the classification probabilities
        assert dominant_stimulus in "12"
        if dominant_stimulus == "1":
            self.prob_drg1_given_stim1, self.prob_drg2_given_stim2 \
                = MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_DOMINANT_STIM, \
                MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_WEAKER_STIM
        else:
            self.prob_drg1_given_stim1, self.prob_drg2_given_stim2 \
                = MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_WEAKER_STIM, \
                MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_DOMINANT_STIM
        self.prob_drg2_given_stim1 = 1 - self.prob_drg1_given_stim1
        self.prob_drg1_given_stim2 = 1 - self.prob_drg2_given_stim2

        # Following are defined in concrete classes.
        self.dragon1 = None
        self.dragon2 = None
        self.stimulus1 = None
        self.stimulus2 = None
        self.start_message = None  #image to be shown at the start \
                             # of the block, set by the concrete classes

        self.positive_feedback = visual.ImageStim(self.win, 
                                                  image="../design/positive.png", 
                                                  pos=(0, 0), size=2)
        self.negative_feedback = visual.ImageStim(self.win, 
                                                  image="../design/negative.png", 
                                                  pos=(0, 0), size=2)
        self.fixation = visual.TextStim(self.win, text="+", pos=(0,0))
        self.optimals = [] # list of booleans, i'th entry is 1 if i'th choice is \
                        # optimal else 0


    def start_trial(self):
        """This is the main api of the class, returns the dictionary data."""
        data = {} # This contains the data for this block, this is also \
               # the return value of this method. \
               #The keys are trials, total_time and learnp.
        trials = [] # This will be added to self.data, each element is a \
                      # dictionary with keys "stim", "key", "time" and 'feedback'
        learnp = False # represents if the subject learned in this block.
        start_time = time.time()

        # At the start show the message and
        # wait till the user presses any key
        self.start_message.draw() 
        self.win.flip()
        event.waitKeys()

        # start the training
        for ntrial in range(MAX_TRIAL):
            trial = {} # this will be added to data.
            stimulus = self.present_stimulus(trials)
            trial['stim'] = stimulus
            key, duration = self.get_key()
            trial['key'] = key
            trial["time"] = duration
            correctp = self.give_feedback(key, stimulus)
            trial['correctp'] = correctp
            trials.append(trial)
            if self.get_accuracy() > MIN_ACCURACY:
                learnp = True
                break
        # add to the data and return
        data['trials'] = trials
        data['learnp'] = learnp
        data['total_time'] = time.time() - start_time
        return data
        
    def get_accuracy(self):
        if len(self.optimals) < NTEST:
            return 0
        else:
            return sum(self.optimals[-NTEST:-1]) / float(NTEST)

    def present_stimulus(self, trials):
        """If in the last MAX_TRIAL, only one stimulus appeared then pick the
        other one else randomly pick one of them. Return 1 if stimuls 
        1 is picked 2 otherwise. Show the stimulus for time = stimulus time"""
        stim = None
        # check if in the last MAX_TRIAL same stim is picked, pick a different
        # one in that case otherwise pick randomly.
        if len(trials) >= MAX_STREAK:
            stims = [trial['stim'] for trial in trials[-MAX_STREAK:]]
            if len(set(stims)) == 1:
                stim = 1 if 2 in stims else 2
        stim = random.choice([1,2]) if not stim else stim
        # render the stimulus
        self.render_stimulus(self.stimulus1) if stim == 1 else \
            self.render_stimulus(self.stimulus2)
        return stim
    
    @abstractmethod
    def render_stimulus(self):
        "render stimulus on the window"
    
    @abstractmethod
    def render_dragons(self, highlight=""):
        '''render dragons on the window.
        argument highlight is in ["left", "right", ""].'''


    def get_key(self):
        """
        Show the dragons and ask the user to identify
        the one corresponding to the stimulus presented by the 
        present_stimulus method, by clicking left or right arrow.
        Return the key pressed(either left or right) and the time taken.
        If the user presses 'escape' then quit the experiment."""
        self.render_dragons()
        start_time = time.time()
        key = event.waitKeys(keyList=["left", "right", "escape"])[0]
        # quit the experiment if the user presses escape
        if key == 'escape':
            self.win.close()
            core.quit()

        # highlight the choice
        self.render_dragons(key)
        return (key, time.time() - start_time)
     
    def give_feedback(self, key, stimulus):
        # check the correctness of the user's choice
        if stimulus == 1:
            chance_correct = self.prob_drg1_given_stim1 if key == 'left' else \
                             self.prob_drg2_given_stim1
        else:
            chance_correct = self.prob_drg1_given_stim2 if key == "left" else \
                             self.prob_drg2_given_stim2
        
        self.optimals.append(chance_correct > 0.5)
        correctp = (chance_correct > random.uniform(0, 1))

        # give the feedback
        self.positive_feedback.draw() if correctp else \
            self.negative_feedback.draw()
        self.win.flip()
        core.wait(WAIT_TIME)
        return correctp


class Visual(Training):
    def  __init__(self, win, dominant_stimulus):
        Training.__init__(self, win, dominant_stimulus)
        self.dragon1 = visual.ImageStim(self.win, 
                                        image="../design/visual_dragon1_sm.jpg",
                                        pos=(-7.0, 0.0),
                                        color="white")
        self.dragon2 = visual.ImageStim(self.win, 
                                        image="../design/visual_dragon2_sm.jpg",
                                        pos=(7.0, 0.0),
                                        color="white")
        self.stimulus1 = visual.ImageStim(self.win, 
                                          image="../design/dragonegg_blue.png",
                                          pos=(0, 0))
        self.stimulus2 = visual.ImageStim(self.win, 
                                          image="../design/dragonegg_red.png",
                                          pos=(0, 0))
        self.start_message = visual.ImageStim(self.win,
                                              image="../design/visual_block.png",
                                              pos=(0, 0))
    
    def __str__(self):
        return "Visual"

    def render_stimulus(self, stimulus):
        "render stimuls on the window"
        stimulus.draw()
        self.fixation.draw()
        self.win.flip()
        core.wait(STIMULUS_TIME)
    
    def render_dragons(self, highlight=""):
        time = WAIT_TIME if highlight else 0
        if highlight == "left":
            self.dragon1.color="yellow"
        if highlight == "right":
            self.dragon2.color="yellow"
        self.dragon1.draw()
        self.dragon2.draw()
        self.fixation.draw()
        self.win.flip()
        core.wait(time)
        self.dragon1.color = self.dragon2.color = "white"


class Semantic(Training):
    def  __init__(self, win, dominant_stimulus):
        Training.__init__(self, win, dominant_stimulus)
        self.dragon1 = visual.TextStim(self.win,
                                       text="Gorun",
                                       pos=(-5,0),
                                       color="white")
        self.dragon2 = visual.TextStim(self.win,
                                       text="Fodur",
                                       pos=(5,0),
                                       color="white")
        self.stimulus1 = visual.TextStim(self.win, 
                                         text="HERBIVORE",
                                         pos=(0, 0))
        self.stimulus2 = visual.TextStim(self.win, 
                                         text="CARNIVORE",
                                         pos=(0, 0))
        self.start_message = visual.ImageStim(self.win,
                                              image="../design/semantic_block.png",
                                              pos=(0, 0))
    
    def __str__(self):
        return "Semantic"

    def render_stimulus(self, stimulus):
        "render stimuls on the window"
        stimulus.draw()
        self.win.flip()
        core.wait(STIMULUS_TIME)
    
    def render_dragons(self, highlight=""):
        time = WAIT_TIME if highlight else 0
        if highlight == "left":
            self.dragon1.color = "yellow"
        if highlight == "right":
            self.dragon2.color = "yellow"
        self.dragon1.draw()
        self.dragon2.draw()
        self.fixation.draw()
        self.win.flip()
        core.wait(time)
        self.dragon1.color = self.dragon2.color = "white"
        

class Auditory(Training):
    def __init__(self, win, dominant_stimulus):
        Training.__init__(self, win, dominant_stimulus)
        self.dragon1 = mixer.Sound("../design/sound_files/ba_00.wav")
        self.dragon2 = mixer.Sound("../design/sound_files/lu_00.wav")
        self.stimulus1 = mixer.Sound("../design/sound_files/dragon1.wav")
        self.stimulus2 = mixer.Sound("../design/sound_files/dragon2.wav")
        self.start_message = visual.ImageStim(self.win,
                                              image="../design/auditory_block.png",
                                              pos=(0, 0))
        self.speaker1 = visual.ImageStim(self.win,
                                    image="../design/speaker_symbol.png",
                                    color="white",
                                    pos=(-5,0))
        self.speaker2 = visual.ImageStim(self.win,
                                    image="../design/speaker_symbol.png",
                                    color="white",
                                    pos=(5,0))
    
    def __str__(self):
        return "Auditory"

    def render_stimulus(self, stimulus):
        self.fixation.draw()
        self.win.flip()
        channel = mixer.Channel(0)
        channel.set_volume(1,1)
        channel.play(stimulus)
        time.sleep(1.2) # Todo: setting it arbitrary current WAIT_TIME is not enough.
    
    def render_dragons(self, highlight=""):
        def play(drg1, drg2):
            """ Play drg1 from the left speaker and drg2 from the right.
            One of them can be an empty string then only play the other"""
            left = mixer.Channel(0)
            left.set_volume(1,0)
            right = mixer.Channel(1)
            right.set_volume(0,1)
            if drg1:
                left.play(drg1)
            if drg2:
                right.play(drg2)
            time.sleep(WAIT_TIME)
            
        if highlight == "left":
            self.speaker1.color = "yellow"
            drg1, drg2 = self.dragon1, ""
        elif highlight == "right":
            self.speaker2.color = "yellow"
            drg1, drg2 = "", self.dragon2
        else:
            drg1, drg2 = self.dragon1, self.dragon2
        self.speaker1.draw()
        self.speaker2.draw()
        self.fixation.draw()
        self.win.flip()
        play(drg1, drg2)
        self.speaker1.color = self.speaker2.color = "white"


if __name__ == "__main__":
    main()

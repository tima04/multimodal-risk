 # -*- coding: utf-8 -*-
import random
import time
from psychopy import core, visual, event, sound
from pygame import mixer
from abc import ABCMeta, abstractmethod
from utilities import *
from parameters import *

def main():
    data = {'start_time': timestamp()}
    
    info = dialog_box(choice_task=True)
    if not info: # user pressed cancel
        return None
    data['id'], data['run'] = info

    #require to calculate outcome of lotteries.
    dominants  = get_dominant_stimulie(data['id']) 

    win = visual.Window([800, 600], 
                        allowGUI=True, 
                        monitor='testMonitor', 
                        units='deg',
                        fullscr=FULLSCREEN,
                        color = "grey")
    mixer.init()

    blocks = [Visual(win, dominants[0]), 
              Auditory(win, dominants[1]),
              Semantic(win, dominants[2])] 
              
    random.shuffle(blocks)
    for block in blocks:
        # start the block and store the return value in data.
        data[str(block)] = block.start_block()

    data['finish_time'] = timestamp()
    save_data(data)
    SummaryChoiceData(data).main() # generate the summary of choice data


class ChoiceTask(object):
    """ Abstract class, Visual, Auditory and Semantic are
    3 concrete representation. start_block is the public method 
    of the class, which returns a list trials, elements of which 
    contain data of each trial."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, win, dominant_stimulus):
        self.win = win
        self.fixation = visual.TextStim(self.win, text="+", pos=(0, 0))
        # Concrete classes will define following attributes.
        self.stimulus1 = ""
        self.stimulus2 = ""
        self.start_message = ""
        self.dominant_stimulus = int(dominant_stimulus)
        # random num to determine which stim appears first.
        self.random_num_gen = random_binary_generator(0.5, k=4)

    def start_block(self):
        """This is the public method of the class. Returns a dictionary
        which has keys start_time, finish_time and a list trials, elements 
        of which contain data from each trial."""
        rslt = {'start_time': timestamp()} 
        self.start_message.draw()
        self.win.flip()
        core.wait(MESSAGE_DURATION)
        self._show_fixation_only(FIXATION_AFTER_MESSAGE_DURATION)
        trials = [] # this will be stored in the data.
        for ntrial in range(NTRIAL):
            # show stimulie in random order.
            start_time = time.time()
            random_num = self.random_num_gen() + 1
            if random_num == 1:
                first, second = [self.stimulus1, self.stimulus2] 
            else:
                first, second = [self.stimulus2, self.stimulus1] 
            self._show_stimulus(first)
            self._show_fixation_only(INTERSTIM_PERIOD)
            self._show_stimulus(second)
            self._show_fixation_only(STIM2_CHOICE_TIME)
            # present the choices such that low outcome is at left(right)
            # if dominant stimululs appear first(second).
            low, high = get_outcomes(MAX_OUTCOME)
            if random_num == self.dominant_stimulus: # dominant stimulus appeared first
                left, right = low, high
            else:
                left, right = high, low
            key, reaction_time = self._present_choices(left, right)
            self._show_fixation_only(AVERAGE_DELAY)
            # save information of this trial.
            trial = {} 
            trial['first_stim'] = random_num
            trial['left_outcome'], trial['right_outcome'] = left, right
            trial['key'], trial['reaction_time'] = key, reaction_time
            trial['time'] = time.time() - start_time
            trials.append(trial)
        rslt['trials'] = trials
        rslt['finish_time'] = timestamp()
        return rslt
    
    def _show_fixation_only(self, duration):
        # if duration is too small then don't draw, otherwise
        # it will be blurry.
        epsilon = 10**(-6)
        if duration < epsilon: 
            return None
        self.fixation.draw()
        self.win.flip()
        core.wait(duration)
        
    @abstractmethod
    def _show_stimulus(self, stim):
        """Concrete class will implement this."""
        return None
    
    def _present_choices(self, left, right):
        """Present the left and the right outcomes, first at the left
        and second at the right of fixation. Keep the choice screen for
        choice_screen_time time, if the user pressed  a left or right key
        then color the corresponding outcome. Returns the key pressed and
        the reaction time."""
        start_time = time.time()
        dist = NUMBER_FIXATION_DIST
        left_outcome = visual.TextStim(self.win, 
                                       text=u"\u20AC" + str(left) ,
                                       pos=(-dist, 0))
        right_outcome = visual.TextStim(self.win, 
                                        text=u"\u20AC" + str(right),
                                        pos=(dist, 0))
        self._render(left_outcome, right_outcome, self.fixation)
        try:
            key = event.waitKeys(maxWait=CHOICE_SCREEN_TIME,  
                                 keyList=["left", "right", "escape"])[0]
        except:
            key = "none"
        reaction_time = time.time() - start_time

        if key == "left":
            left_outcome.color = "yellow"
        elif key == "right":
            right_outcome.color = "yellow"
        elif key == "escape":
            self.win.close()
            core.quit()
        #if a key is pressed then show it in yellow for the remaining time.
        if key != 'none':
            self._render(left_outcome, right_outcome, self.fixation)
            time_elasped = time.time() - start_time
            core.wait(CHOICE_SCREEN_TIME - time_elasped)
        
        return key, reaction_time

    def _render(self, *args):
        for arg in args:
            arg.draw()
        self.win.flip()


class Visual(ChoiceTask):
    def __init__(self, win, dominant_stimulus):
        ChoiceTask.__init__(self, win, dominant_stimulus)
        self.stimulus1 = visual.ImageStim(self.win, 
                                          image=STIM1_VISUAL,
                                          pos=(0, 0))
        self.stimulus2 = visual.ImageStim(self.win, 
                                          image=STIM2_VISUAL,
                                          pos=(0, 0))
        self.start_message = visual.TextStim(self.win,
                                             text="SEHEN",
                                             pos=(0, 0))

    def __str__(self):
        return "Visual"
 
    def _show_stimulus(self, stim):
        self._render(stim, self.fixation)
        core.wait(STIMULUS_DURATION)


class Semantic(ChoiceTask):
    def __init__(self, win, dominant_stimulus):
        ChoiceTask.__init__(self, win, dominant_stimulus)
        self.stimulus1 = visual.TextStim(self.win, 
                                         text="HERBIVORE",
                                         pos=(0, 0))
        self.stimulus2 = visual.TextStim(self.win, 
                                         text="CARNIVORE",
                                         pos=(0, 0))
        self.start_message = visual.TextStim(self.win,
                                             text="LESEN",
                                             pos=(0, 0))

    def __str__(self):
        return "Semantic"
        
    def _show_stimulus(self, stim):
        self._render(stim)
        core.wait(STIMULUS_DURATION)


class Auditory(ChoiceTask):
    def __init__(self, win, dominant_stimulus):
        ChoiceTask.__init__(self, win, dominant_stimulus)
        self.stimulus1 = mixer.Sound(STIM1_AUDIO)
        self.stimulus2 = mixer.Sound(STIM2_AUDIO)
        self.start_message = visual.TextStim(self.win,
                                              text="HOREN",
                                              pos=(0, 0))
        self.speaker = visual.ImageStim(self.win,
                                        image=SPEAKER_SYMBOL,
                                        color="white",
                                        pos=(0, 0))
    
    def __str__(self):
        return "Auditory"

    def _show_stimulus(self, stim):
        self.speaker.draw()
        self.win.flip()
        stim.play()
        time.sleep(STIMULUS_DURATION)

    
if __name__ == "__main__":
    main()

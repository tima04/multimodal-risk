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
              Semantic(win, dominants[1]), 
              Auditory(win, dominants[2])]
    random.shuffle(blocks)
    for block in blocks:
        # start the block and store the return value in data.
        data[str(block)] = block.start_block()

    data['finish_time'] = timestamp()
    save_data(data)


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
        self.dominant_stimulus = dominant_stimulus

    def start_block(self):
        """This is the public method of the class. Returns
        a list trials, elements of which contain data from each
        trial."""
        self.start_message.draw()
        self.win.flip()
        core.wait(WAIT_TIME)
        trials = [] # this will be stored in the data.
        for ntrial in range(NTRIAL):
            # show stimulie in random order.
            random_num = random.choice([1,2])
            stims = [self.stimulus1, self.stimulus2]
            if random_num == 2: stims.reverse()
            self._show_stimulus(*stims)
            # present the choices such that low outcome is at left(right)
            # if dominant stimululs appear first(second).
            low, high = get_outcomes(MAX_OUTCOME)
            if random_num == self.dominant_stimulus: # dominant stimulus appeared first
                left, right = low, high
            else:
                left, right = high, low
            key, reaction_time = self._present_choices(left, right)
            self._show_inter_trial_win()
            # save information of this trial.
            trial = {} 
            trial['first_stim'] = random_num
            trial['left_outcome'], trial['right_outcome'] = left, right
            trial['key'], trial['time'] = key, reaction_time
            trials.append(trial)
        return trials
    
    def _show_inter_trial_win(self):
        """show this window between trials."""
        # if inter_trial_delay is too small then don't show, otherwise
        # it will be blurry.
        epsilon = 10**(-6)
        if INTER_TRIAL_DELAY < epsilon: 
            return None
        self.fixation.draw()
        self.win.flip()
        core.wait(INTER_TRIAL_DELAY)

    @abstractmethod
    def _show_stimulus(self, stim1, stim2):
        """Concrete class will implement this."""
        return None
    
    def _present_choices(self, left, right):
        """Present the left and the right outcomes, first at the left
        and second at the right of fixation. Keep the choice screen for
        choice_screen_time time, if the user pressed  a left or right key
        then color the corresponding outcome. Returns the key pressed and
        the reaction time."""
        start_time = time.time()
        left_outcome = visual.TextStim(self.win, 
                                       text=left,
                                       pos=(-5, 0))
        right_outcome = visual.TextStim(self.win, 
                                        text=right,
                                        pos=(5, 0))
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
        #if the key pressed then show it in yellow for the remaining time
        if key != 'none':
            self._render(left_outcome, right_outcome, self.fixation)
            time_elasped = start_time - time.time()
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
                                          image=VISUAL_DRAGON1,
                                          pos=(0, 0))
        self.stimulus2 = visual.ImageStim(self.win, 
                                          image=VISUAL_DRAGON2,
                                          pos=(0, 0))
        self.start_message = visual.TextStim(self.win,
                                             text="Visual Block",
                                             pos=(0, 0))

    def __str__(self):
        return "Visual"
 
    def _show_stimulus(self, stim1, stim2):
        self._render(stim1, self.fixation)
        core.wait(INTERSTIM_PERIOD)
        self._render(stim2, self.fixation)
        core.wait(INTERSTIM_PERIOD)


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
                                             text="Semantic Block",
                                             pos=(0, 0))

    def __str__(self):
        return "Semantic"
        
    def _show_stimulus(self, stim1, stim2):
        self._render(stim1)
        core.wait(INTERSTIM_PERIOD)
        self._render(stim2)
        core.wait(INTERSTIM_PERIOD)


class Auditory(ChoiceTask):
    def __init__(self, win, dominant_stimulus):
        ChoiceTask.__init__(self, win, dominant_stimulus)
        self.stimulus1 = mixer.Sound(STIM1_AUDIO)
        self.stimulus2 = mixer.Sound(STIM2_AUDIO)
        self.start_message = visual.TextStim(self.win,
                                              text="Auditory Block",
                                              pos=(0, 0))
        self.speaker = visual.ImageStim(self.win,
                                        image=SPEAKER_SYMBOL,
                                        color="white",
                                        pos=(0, 0))
    
    def __str__(self):
        return "Auditory"

    def _show_stimulus(self, stim1, stim2):
        self.speaker.draw()
        self.win.flip()
        stim1.play()
        time.sleep(INTERSTIM_PERIOD)
        stim2.play()
        time.sleep(INTERSTIM_PERIOD)

    
if __name__ == "__main__":
    main()

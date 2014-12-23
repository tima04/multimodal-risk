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
    
    if IS_FMRI:
        assert NTRIAL == 28, "nrial not 28 for fmri choice task"

    # preload Delay and Outcomes class, 
    Delay()
    Outcomes()


    # info = dialog_box(choice_task=True)
    # if not info: # user pressed cancel
    #     return None

    # data['id'], data['run'] = info
    data['id'], data['run'] = (1, 1)

    #require to calculate outcome of lotteries.
    dominants  = get_dominant_stimulie(data['id']) 
    data["dominant_stimulie"] = dominants

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
    data['block_order'] = [str(block) for block in blocks]

    # show the fixation and wait for the scanner trigger key
    fixation = visual.TextStim(win, text="+", pos=(0, 0))
    fixation.draw()
    win.flip()
    event.waitKeys(keyList=SCANNER_PULSE_KEYS)
    data["scanner_trigger_time"] = time.time()

    for block in blocks:
        # start the block and store the return value in data, and save
        # partial data to insure against a crash
        data[str(block)] = block.start_block()
        save_data(data, partial=True) 

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
        self.fixation = visual.TextStim(self.win, text="+", pos=(0, 0), color="black")
        self.slow_down_msg = visual.ImageStim(self.win, image=SLOW_DOWN_SYMBOL)
        self.too_slow_msg = visual.ImageStim(self.win, image=TOO_LATE_SYMBOL)
        self.dominant_stimulus = int(dominant_stimulus)
        # random num to determine which stim appears first.
        self.random_num_gen = random_binary_generator(0.5, k=4)
        # Concrete classes will define following attributes.
        self.stimulus1 = ""
        self.stimulus2 = ""
        self.start_message = ""

    def start_block(self):
        """This is the public method of the class. Returns a dictionary
        which has keys start_time, finish_time and a list trials, elements 
        of which contain data from each trial."""
        # trial durarion is sum of fixed and jittered durations. Fixed duration 
        # can vary if subject respond too early or too late. 
        trial_fixed_dur = 2 * STIM_DUR + INTERSTIM_PERIOD + CHOICE_SCREEN_DUR + \
                          CHOICE_SCREEN_DUR2
        rslt = {'start_time': time.time()}
        jitter_delay = Delay(IS_FMRI, trial_fixed_dur)
        outcomes = Outcomes(is_fmri=IS_FMRI)

        rslt['start_message_event'] = time.time()
        self.start_message.draw()
        self.win.flip()
        core.wait(MESSAGE_DUR)

        rslt['fixation_after_message_duration_event'] = time.time()
        self._show_fixation_only(FIXATION_AFTER_MESSAGE_DUR)

        trials = [] # this will be stored in the data.
        for ntrial in range(NTRIAL):
            o1, o2, is_sd, is_high = outcomes.next()
            is_sd, is_high = map(int, [is_sd, is_high]) #just to make sure, they \
                             # are int
            trial = {} # info about this trial, will be stored in this dict.
            trial['trial_start_event'] = time.time()
            
            # jitter fixation at a begining of a trial
            trial['first_jitter_fixation_event'] = time.time()
            self._show_fixation_only(jitter_delay.next(is_high))
            
            # show stimulie in random order.
            random_num = self.random_num_gen() + 1
            if random_num == 1:
                first, second = [self.stimulus1, self.stimulus2]
            else:
                first, second = [self.stimulus2, self.stimulus1]
            
            trial['first_stim_event'] = time.time()
            self._show_stimulus(first)
            
            trial['fixation_after_first_stim_event'] = time.time()
            self._show_fixation_only(INTERSTIM_PERIOD)
            
            trial['second_stim_event'] = time.time()
            self._show_stimulus(second)
            
            trial['jitter_fixation_after_second_stim_event'] = time.time()
            self._show_fixation_only(jitter_delay.next()) 

            # present the choices such that low outcome is at left(right), \
            # upon whether order of dominant_stimulus and if the lottery
            # is supposed to be stochastic dominance.
            low, high = min(o1, o2), max(o1, o2)
            if random_num == self.dominant_stimulus: # dominant stimulus appeared first
                left, right = (high, low) if is_sd else (low, high)
            else:
                left, right = (low, high) if is_sd else (high, low)

            trial['choice_screen_event'] = time.time()
            key = self._present_choices(left, right, trial)

            # save information of this trial.
            trial["is_sd"] = is_sd
            trial["is_high"] = is_high
            trial['first_stim'] = random_num
            trial['left_outcome'], trial['right_outcome'] = left, right
            trial['key'] = key
            trial['trial_finish_event'] = time.time()
            trials.append(trial)
            # adjust the next jitter times, 
            excess_dur = jitter_delay.adjust(time.time() - 
                                                   trial['trial_start_event'],
                                             is_high)
        # at the end of the block show fixation for last trial excess_dur
        self._show_fixation_only(excess_dur)
        rslt['trials'] = trials
        rslt['finish_time'] = time.time()
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
    
    def _present_choices(self, oleft, oright, trial):
        """Present the left and the right outcomes, first at the left
        and second at the right of fixation. After choice_screen_dur
        fixation cross is colored red for choice_screen_dur2, user has 
        to respond while the cross is red. If user respond before or after
        then show the slow-down or too-slow message, otherwise color the
        outcome pressed yellow for remaining duration. Store all the
        events in dictionary trial, which is an argument to the method.
        Return value is the key pressed."""
        trial['success'] = False # set to True if user responded on time.
        start_time = time.time()
        dist = NUMBER_FIXATION_DIST
        left_outcome = visual.TextStim(self.win, 
                                       text=u"\u20AC" + str(oleft) ,
                                       pos=(-dist, 0))
        right_outcome = visual.TextStim(self.win, 
                                        text=u"\u20AC" + str(oright),
                                        pos=(dist, 0))
        self._render(left_outcome, right_outcome, self.fixation)
        # wait for choice_screen_dur and check if user presses left or right key
        try:
            key = event.waitKeys(maxWait=CHOICE_SCREEN_DUR,
                                 keyList=[LEFT_KEY, RIGHT_KEY, ESC_KEY])[0]
        except:
            key = "none"
        #usr responded too early show her slow down message and return
        if key in [LEFT_KEY, RIGHT_KEY]:
            trial['slow_down_msg_event'] = time.time()
            trial['too_fast'] = True
            self._render(self.slow_down_msg, duration=SLOW_DOWN_MSG_DUR)
            return key
        if key == ESC_KEY:
            self.win.close()
            core.quit()
        # turn the fixation cross red and wait for 1 sec for a user to respond
        trial['fixation_color_red_event'] = time.time()
        self.fixation.color = "red"
        self._render(left_outcome, right_outcome, self.fixation)
        try:
            key = event.waitKeys(maxWait=CHOICE_SCREEN_DUR2,
                                 keyList=[LEFT_KEY, RIGHT_KEY])[0]
            trial['key_pressed_event'] = time.time()
        except:
            key = "none"
        self.fixation.color = "black"
        # user did not responded, show too slow msg and return.
        if key == "none":
            trial['too_slow'] = True
            trial['too_slow_msg_event'] = time.time()
            self._render(self.too_slow_msg, duration=TOO_SLOW_MSG_DUR)
            return key
        #show the pressed key in yellow for the remaining time.
        if key == LEFT_KEY:
            left_outcome.color = "yellow"
        elif key == RIGHT_KEY:
            right_outcome.color = "yellow"
        self._render(left_outcome, right_outcome, self.fixation)
        time_elasped = time.time() - start_time
        core.wait(CHOICE_SCREEN_DUR + CHOICE_SCREEN_DUR2 - time_elasped)
        return key

    def _render(self, *args, **kwargs):
        """kwargs if present then must be
        a dict with the key 'duration' and value float."""
        assert (not kwargs) or kwargs.get('duration')
        epsilon = 10**-6
        for arg in args:
            arg.draw()
        self.win.flip()
        if kwargs:
            core.wait(kwargs['duration'])

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
        core.wait(STIM_DUR)


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
        core.wait(STIM_DUR)


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
        time.sleep(STIM_DUR)

    
if __name__ == "__main__":
    main()

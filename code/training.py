import random
import time
from psychopy import core, visual, event, sound
from abc import ABCMeta, abstractmethod
from parameters import *


def main():
    global optimals # list of booleans, i'th entry is 1 if i'th choice is \
        # optimal else 0
    #parse_parameters()
    win = visual.Window([800, 600], allowGUI=True, 
                             monitor='testMonitor', 
                             units='deg',
                             fullscr=False)
    blocks = [Visual(win), Semantic(win), Auditory(win)]
    #blocks = [Auditory(win)] 
    random.shuffle(blocks)
    for block in blocks:
        optimals = []
        n = block.start_trial()
        if n == max_trial:
            print "subject did not learn"
        else:
            print "subject learned in %s trials"%n
    win.close()
    core.quit()

def parse_parameters():
    global ntrial, stimulus_time, wait_time, \
        prob_drg1_given_stim1, prob_drg1_given_stim2
    global prob_drg2_given_stim1, prob_drg2_given_stim2 # not present in parameter.csv
    # parse the parametes file, and obtain parameters
    lines = open("parameters.csv").readlines()
    def par_value(parameter, lines=lines):
        """Check for the first field in each line, if it contains the
        parameter then return the second field(by assumption it contains
        the value of the parameter)"""
        value = filter(lambda s: s.startswith(parameter), 
                       lines)[0].split(",")[1]
        return float(value)
    try:
        ntrial = int(par_value('ntrial'))
        prob_drg1_given_stim1 = par_value('prob_drg1_given_stim1')
        prob_drg1_given_stim2 = par_value('prob_drg1_given_stim2')
        stimulus_time = par_value('stimulus_time')
        wait_time = par_value('wait_time')
    except:
        print "Can not parse the parameters.csv"
        pass
    prob_drg2_given_stim1 = 1 - prob_drg1_given_stim1
    prob_drg2_given_stim2 = 1 - prob_drg1_given_stim2


class Training(object):
    """
    Abstract class. Visual, auditory and semantic training are
    3 concrete representation.
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self, win):
        "stimulus1 and 2 are to be defined in concrete classes"
        self.win = win
        
        # Following are defined in concrete classes.
        self.dragon1 = None
        self.dragon2 = None
        self.dragon1_highlighted = None
        self.dragon2_highlighted = None
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
        self.fixation = visual.TextStim(self.win,
                                                      text="+",
                                                      pos=(0,0))
        global optimals

    def start_trial(self):
        # At the start show the message and
        # wait till the user presses any key
        self.start_message.draw() 
        self.win.flip()
        event.waitKeys()
        
        # start the training
        for i in range(max_trial):
            stimulus = self.present_stimulus()
            key = self.get_key()
            self.give_feedback(key, stimulus)
            if self.get_accuracy() > min_accuracy:
                return i + 1
        return i + 1
        
    def get_accuracy(self):
        if len(optimals) < ntest:
            return 0
        else:
            return sum(optimals[-ntest:-1]) / float(ntest)

    def present_stimulus(self):
        """randomly pick one of the stimulus and return intger 1
        if stimuls 1 is picked 2 otherwise. Show the stimulus
        for time = stimulus time"""
        rand_num = random.choice([1,2])
        self.render_stimulus(self.stimulus1) if rand_num == 1 else \
            self.render_stimulus(self.stimulus2)
        return rand_num
    
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
        Return the key pressed(either left or right). If the user
        presses 'escape' then quit the experiment."""
        self.render_dragons()
        key = event.waitKeys(keyList=["left", 
                                       "right",
                                       "escape"])[0]
        # quit the experiment if the user presses escape
        if key == 'escape':
            self.win.close()
            core.quit()

        # highlight the choice
        self.render_dragons(key)
        return key
     
    def give_feedback(self, key, stimulus):
        # check the correctness of the user's choice
        if stimulus == 1:
            chance_correct = prob_drg1_given_stim1 if key == 'left' else \
                             prob_drg2_given_stim1
        else:
            chance_correct = prob_drg1_given_stim2 if key == "left" else \
                             prob_drg2_given_stim2
        
        optimals.append(chance_correct > 0.5)
        correctp = (chance_correct > random.uniform(0, 1))

        # give the feedback
        self.positive_feedback.draw() if correctp else \
            self.negative_feedback.draw()
        self.win.flip()
        core.wait(wait_time)


class Visual(Training):
    def  __init__(self, win):
        Training.__init__(self, win)
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
    def render_stimulus(self, stimulus):
        "render stimuls on the window"
        stimulus.draw()
        self.fixation.draw()
        self.win.flip()
        core.wait(stimulus_time)
    
    def render_dragons(self, highlight=""):
        time = wait_time if highlight else 0
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
    def  __init__(self, win):
        Training.__init__(self, win)
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

    def render_stimulus(self, stimulus):
        "render stimuls on the window"
        stimulus.draw()
        self.win.flip()
        core.wait(stimulus_time)
    
    def render_dragons(self, highlight=""):
        time = wait_time if highlight else 0
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
    def __init__(self, win):
        Training.__init__(self, win)
        self.dragon1 = sound.SoundPygame(value="../design/ru.wav")
        self.dragon2 = sound.SoundPygame(value="../design/lu.wav")
        self.stimulus1 = sound.SoundPygame(value="../design/sound1.wav")
        self.stimulus2 = sound.SoundPygame(value="../design/sound1.wav")
        self.start_message = visual.ImageStim(self.win,
                                              image="../design/auditory_block.png",
                                              pos=(0, 0))
        self.speaker1 = visual.ImageStim(self.win,
                                    image="../design/speaker.png",
                                    color="white",
                                    pos=(-5,0))
        self.speaker2 = visual.ImageStim(self.win,
                                    image="../design/speaker.png",
                                    color="white",
                                    pos=(5,0))

    def render_stimulus(self, stimulus):
        self.fixation.draw()
        self.win.flip()
        stimulus.play()
        time.sleep(3)
    
    def render_dragons(self, highlight=""):
        def play(drg):
            if drg:
                drg.play()
                time.sleep(wait_time)
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
        play(drg1)
        play(drg2)
        time.sleep(wait_time) 
        self.speaker1.color = self.speaker2.color = "white"

if __name__ == "__main__":
    main()

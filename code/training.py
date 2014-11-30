import random
from psychopy import core, visual, event, sound
from abc import ABCMeta, abstractmethod

def main():
#    import pdb; pdb.set_trace()
    global ntrial, stimulus_time, wait_time, prob_drg1_given_stim1, prob_drg1_given_stim2
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
        return
    prob_drg2_given_stim1 = 1 - prob_drg1_given_stim1
    prob_drg2_given_stim2 = 1 - prob_drg1_given_stim2
    win = visual.Window([800, 600], allowGUI=True, 
                             monitor='testMonitor', 
                             units='deg',
                             fullscr=True)
    blocks = [Visual(win), Semantic(win)]
    random.shuffle(blocks)
    for block in blocks:
        block.start_trial()
    win.close()
    core.quit()


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
        self.dragon1 = visual.ImageStim(self.win, 
                                        image="../design/visual_dragon1_sm.jpg",
                                        pos=(-7.0, 5.0))
        self.dragon2 = visual.ImageStim(self.win, 
                                        image="../design/visual_dragon2_sm.jpg",
                                        pos=(7.0, 5.0))

        # stimulie and block_image_path are defined in concrete classes
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
        self.message = visual.TextStim(self.win, 
                                       text="press left or right arrow key", 
                                       pos=(0, 0))

    def start_trial(self):
        # At the start show the message and
        # wait till user presses any key
        self.start_message.draw() 
        self.win.flip()
        event.waitKeys()
        
        # start the training
        for i in range(ntrial):
            stimulus = self.present_stimulus()
            key = self.get_key()
            self.give_feedback(key, stimulus)
        
    def present_stimulus(self):
        """randomly pick one of the stimulus and return intger 1
        if stimuls 1 is picked 2 otherwise. Show the stimulus
        for time = stimulus time"""
        rand_num = random.choice([1,2])
        self.render(self.stimulus1) if rand_num == 1 else \
            self.render(self.stimulus2)
        self.win.flip()
        core.wait(stimulus_time)
        return rand_num
    
    @abstractmethod
    def render(self):
        "render stimulus on the window"

    def get_key(self):
        """
        Show the dragons and ask the user to identify
        the one corresponding to the stimulus presented by the 
        present_stimulus method, by clicking left or right arrow.
        Return the key pressed(either left or right)"""

        # show the dragons and wait for
        # the user to press the key, keep
        # waiting untill the user presses left
        # or right key.
        self.dragon1.draw()
        self.dragon2.draw()
        self.message.draw()
        self.win.flip()
        event.clearEvents()
        core.wait(wait_time)
        keys = event.getKeys()
 
        # event.waitKeys() fun is somehow not working
        # next two lines simulates it recursively simulates that.
        if not (('left' in keys) or ('right' in keys)):
            return self.get_key()

        # highlight the choice
        # ask Flavia to send the highlighted dragons.
        return keys[0]
     
    def give_feedback(self, key, stimulus):
        # check the correctness of the user's choice
        if stimulus == 1:
            chance_correct = prob_drg1_given_stim1 if key == 'left' else \
                             prob_drg2_given_stim1
        else:
            chance_correct = prob_drg1_given_stim2 if key == "left" else \
                             prob_drg2_given_stim2

        correctp = (chance_correct > random.uniform(0, 1))

        # give the feedback
        self.positive_feedback.draw() if correctp else \
            self.negative_feedback.draw()
        self.win.flip()
        core.wait(wait_time)


class Visual(Training):
    def  __init__(self, win):
        Training.__init__(self, win)
        self.stimulus1 = visual.ImageStim(self.win, 
                                          image="../design/dragonegg_blue.png",
                                          pos=(0, 0))
        self.stimulus2 = visual.ImageStim(self.win, 
                                          image="../design/dragonegg_red.png",
                                          pos=(0, 0))
        self.start_message = visual.ImageStim(self.win,
                                              image="../design/visual_block.png",
                                              pos=(0, 0))
    def render(self, stimulus):
        "render stimuls on the window"
        stimulus.draw()


class Semantic(Training):
    def  __init__(self, win):
        Training.__init__(self, win)
        self.stimulus1 = visual.TextStim(self.win, 
                                         text="HERBIVORE",
                                         pos=(0, 0))
        self.stimulus2 = visual.TextStim(self.win, 
                                         text="CARNIVORE",
                                         pos=(0, 0))
        self.start_message = visual.ImageStim(self.win,
                                              image="../design/semantic_block.png",
                                              pos=(0, 0))

    def render(self, stimulus):
        "render stimuls on the window"
        stimulus.draw()


class Auditory(Training):
    def __init__(self, win):
        Training.__init__(self, win)
        self.stimulus1 = sound.SoundPygame(name="../sound1.mp3")
        self.stimulus1 = sound.SoundPygame(name="../sound1.mp3")
        self.start_message = visual.ImageStim(self.win,
                                              image="../design/auditory_block.png",
                                              pos=(0, 0))
    
    def render(self, stimulus):
        stimulus.play()


if __name__ == "__main__":
    main()


import random
import time
from psychopy import core, visual, event, sound
from abc import ABCMeta, abstractmethod

# globals
interstim_period = 0.5
delay = 1
choice_screen_time = 2.5 
ntrial = 5

def main():
    win = visual.Window([800, 600], 
                        allowGUI=True, 
                        monitor='testMonitor', 
                        units='deg',
                        fullscr=False,
                        color = "grey")
    blocks = [Visual(win), Semantic(win), Auditory(win)]
    #blocks = [Auditory(win)]
    random.shuffle(blocks)
    map(lambda block: block.start_block(), blocks)

class ChoiceTask(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, win):
        self.win = win
        self.fixation = visual.TextStim(self.win, text="+", pos=(0, 0))
        # Concrete classes will define following attributes.
        self.stimulus1 = ""
        self.stimulus2 = ""
        self.start_message = ""
    
    def start_block(self):
        self.start_message.draw()
        self.win.flip()
        core.wait(delay)
        for i in range(ntrial):
            self.show_stimulus(self.stimulus1, self.stimulus2)
            #self.show_stimulus(self.stimulus2)
            self.present_choices()
    
    @abstractmethod
    def show_stimulus(self, stim1, stim2):
        """Concrete class will implement it."""
        return None
    
    def present_choices(self):
        left_outcome = visual.TextStim(self.win, 
                                       text=random.choice(range(10,20)), 
                                       pos=(-5, 0))
        right_outcome = visual.TextStim(self.win, 
                                        text=random.choice(range(10,20)), 
                                        pos=(5, 0))
        self.draw(left_outcome, right_outcome, self.fixation)
        try:
            key = event.waitKeys(maxWait=choice_screen_time, 
                                 keyList=["left", "right", "escape"])[0]
        except:
            key = "none"
        print key
        if key == "left":
            left_outcome.color = "yellow"
        elif key == "right":
            right_outcome.color = "yellow"
        elif key == "escape":
            self.win.close()
            core.quit()
        else:
            return key
        self.draw(left_outcome, right_outcome, self.fixation)
        core.wait(delay)
        return key

    def draw(self, *args):
        for arg in args:
            arg.draw()
        self.win.flip()


class Visual(ChoiceTask):
    def __init__(self, win):
        ChoiceTask.__init__(self, win)
        self.stimulus1 = visual.ImageStim(self.win, 
                                          image="../design/dragonegg_blue.png",
                                          pos=(0, 0))
        self.stimulus2 = visual.ImageStim(self.win, 
                                          image="../design/dragonegg_red.png",
                                          pos=(0, 0))
        self.start_message = visual.TextStim(self.win,
                                             text="Visual Block",
                                             pos=(0, 0))

    def show_stimulus(self, stim1, stim2):
        self.draw(stim1, self.fixation)
        core.wait(interstim_period)
        self.draw(stim2, self.fixation)
        core.wait(interstim_period)


class Semantic(ChoiceTask):
    def __init__(self, win):
        ChoiceTask.__init__(self, win)
        self.stimulus1 = visual.TextStim(self.win, 
                                         text="HERBIVORE",
                                         pos=(0, 0))
        self.stimulus2 = visual.TextStim(self.win, 
                                         text="CARNIVORE",
                                         pos=(0, 0))
        self.start_message = visual.TextStim(self.win,
                                             text="Semantic Block",
                                             pos=(0, 0))
        
    def show_stimulus(self, stim1, stim2):
        self.draw(stim1)
        core.wait(interstim_period)
        self.draw(stim2)
        core.wait(interstim_period)


class Auditory(ChoiceTask):
    def __init__(self, win):
        ChoiceTask.__init__(self, win)
        self.stimulus1 = sound.SoundPygame(value="../design/sound1.wav")
        self.stimulus2 = sound.SoundPygame(value="../design/sound1.wav")
        self.start_message = visual.TextStim(self.win,
                                              text="Auditory Block",
                                              pos=(0, 0))
        self.speaker = visual.ImageStim(self.win,
                                        image="../design/speaker.png",
                                        color="white",
                                        pos=(0, 0))

    def show_stimulus(self, stim1, stim2):
        self.speaker.draw()
        self.win.flip()
        stim1.play()
        time.sleep(5)
        stim2.play()
        time.sleep(5)

    
if __name__ == "__main__":
    main()

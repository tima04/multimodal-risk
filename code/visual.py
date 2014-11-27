p"""
VISUAL:

1. Show red or blue egg for 1000 ms (make this a variable, so we can
change it; keep central parameters file).  2. choice screen with Gorun
picture to the left of fixation and Fodur picture to the right of
fixation. Subjects indicate either Left or Right (i.e. they guess
whether the egg is a Gorun or Fodur egg). [ NO TIME LIMIT HERE -- NEXT
SCREEN APPEARS ONLY AFTER SUBJECT PRESSES THE LEFT OR RIGHT
BUTTON. For invalid button, display INVALID RESPONSE ] 3. Subject
presses Left or Right arrow button; that stimulus is "highlighted"
(see pdf). 300 ms (?).  4. Feedback screen for 500 ms: either a green
check mark or a red cross. Feedback is probabilistic: - Red egg = 85%
Gorun 15% Fodur I.e. we draw from a random distribution between 0 and
1. If number < =.85 it is a Gorun we give positive feedback (see
below). If number > 0.85, give incorrect feedback: it is a Fiso.  -
Blue egg = 65 % Fodur, 35% Gorun.

"""

from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import psychopy as ppc
import time, numpy, random

#variable definition, put them in a csv file later
# dragon 1 is Gorun(the circular one) and dragon 2 is Fodur.
probRedEggDrg1 = 0.85 # probability of a red egg belonging to dragon1 and so on.
probBlueEggDrg1 = 0.35
probRedEggDrg2 = 1 - probRedEggDrg1
probBlueEggDrg2 = 1 - probBlueEggDrg1
eggTime = 0.5
#feedbackTime = 0.3
waitTime = 0.5 # other waiting time
ntrial = 4

# parse the parametes file, and obtain parameters
lines = open("parameters.csv").readlines()
try:
    probRedEggDrg1 = filter(lambda s: s.startsWith('probRedEggDrg1'), lines)[1]
    probBlueEggDrg1 = filter(lambda s: s.startsWith('probBlueEggDrg1'), lines)[1]
    eggTime = filter(lambda s: s.startsWith('eggTime'), lines)[1]
    waitTime = filter(lambda s: s.startsWith('waitTime'), lines)[1]
    ntrial = filter(lambda s: s.startsWith('ntrial'), lines)[1]
except:
    print "Can not parse the parameters.csv, is it comma separated?"
    pass


0.85 # probability of a red egg belonging to dragon1 and so on.

class VisualTraining():
    def __init__(self, ntrial):
        self.ntrial = ntrial
        self.win = visual.Window([800, 600], allowGUI=True, monitor='testMonitor',
                                 units='deg')
        self.dragon1 = visual.ImageStim(self.win, image="../design/visual_dragon1_sm.jpg",                                     
                                        pos=(-7.0, 5.0))
        self.dragon2 = visual.ImageStim(self.win, image="../design/visual_dragon2_sm.jpg",
                                        pos=(7.0, 5.0))
        self.blue_egg = visual.ImageStim(self.win, image="../design/dragonegg_blue.png",
                                         pos=(0, 0))
        self.red_egg = visual.ImageStim(self.win, image="../design/dragonegg_red.png",
                                        pos=(0, 0))
        self.positive_feedback = visual.ImageStim(self.win, image="../design/positive.png", 
                                                  pos=(0, 0), size=2)
        self.negative_feedback = visual.ImageStim(self.win, image="../design/negative.png", 
                                                  pos=(0, 0), size=2)
        self.message = visual.TextStim(self.win, text="press left or right arrow key", 
                                       posf=(0, 0))
        self.eggColor = "" # egg color randomly picked by the showEgg method.
    
    def startTrial(self):
        for i in range(self.ntrial):
            color = self.showEgg()
            key = self.getKey()
            self.giveFeedback(color, key)
        self.win.close()
        core.quit()

    def showEgg(self):
        """randomly pick a red or blue egg, set the value of the
        color picked in self.eggColor. Show the egg for time=eggTime
        which is a parameter set in the parameter file"""
        color = random.choice(['red', 'blue'])
        # self.eggColor = color
        egg = self.red_egg if color == 'red' else self.blue_egg
        egg.draw()
        self.win.flip()
        core.wait(eggTime)
        return color

    def getKey(self):
        """
        Show the dragons and ask the user to identify
        the mother, of the egg shown by the showEgg method,
        by clicking left or right arrow, return the key
        pressed(either left or right)"""
        # show the dragons and wait for
        # the user to press the key, keep
        # waiting untill the user presses left
        # or right key.
        self.dragon1.draw()
        self.dragon2.draw()
        self.message.draw()
        self.win.flip()
        event.clearEvents()
        core.wait(waitTime)
        keys = event.getKeys()

        # event.waitKeys() fun is somehow not working
        # next two lines simulates it recursively simulates that.
        if not (('left' in keys) or ('right' in keys)):
            return self.getKey()

        # highlight the choice
        # ask Flavia to send the highlighted dragons.
        return keys[0]

    def giveFeedback(self, color, key):
        # check the correctness of the user's choice
        if color == 'red':
            chance_correct = probRedEggDrg1 if key == 'left' else\
                             probRedEggDrg2
        else:
            chance_correct = probBlueEggDrg1 if key == 'left' else\
                             probBlueEggDrg2
        correctp = (chance_correct > random.uniform(0, 1))
        #print colorEgg, keys[0], chance_correct, correctp
        
        # give the feedback
        self.positive_feedback.draw() if correctp else\
            self.negative_feedback.draw()
        self.win.flip()
        core.wait(waitTime)
        
    def questionAndFeedback(self):
        """
        Show the dragons and ask the user to identify
        the mother by clicking left or right arrow, if 
        she does it corrrectly then give positive feedback
        else give a negative one.
        """
        # show the dragons and wait for
        # the user to press the key, keep
        # waiting untill the user presses left
        # or right key.
        self.dragon1.draw()
        self.dragon2.draw()
        self.message.draw()
        self.win.flip()
        event.clearEvents()
        core.wait(waitTime)
        keys = event.getKeys()
        
        # event.waitKeys() fun is somehow not working
        # next two lines simulates it recursively simulates that.
        if not (('left' in keys) or ('right' in keys)):
            return self.questionAndFeedback()
            
        # highlight the choice
        # ask Flavia to send the highlighted dragons.
        
        # check the correctness of the user's choice 
        if self.eggColor == 'red':
            chance_correct = probRedEggDrg1 if keys[0] == 'left' else\
                             probRedEggDrg2
        else:
            chance_correct = probBlueEggDrg1 if keys[0] == 'left' else\
                             probBlueEggDrg2
        correctp = (chance_correct > random.uniform(0, 1))
        #print colorEgg, keys[0], chance_correct, correctp
        
        # give the feedback
        self.positive_feedback.draw() if correctp else\
            self.negative_feedback.draw()
        self.win.flip()
        core.wait(waitTime)


def main():
    VisualTraining(ntrial).startTrial()

if __name__ == "__main__":
    main()

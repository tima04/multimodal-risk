"""
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

win = visual.Window([800,600], allowGUI=True, monitor='testMonitor', units='deg')
#win =visual.Window(size=[800,600], fullscr=False, units='norm', monitor='testMonitor') 

dragon1 = visual.ImageStim(win, image="../design/visual_dragon1_sm.jpg",
                              pos=(-7.0, 5.0))
dragon2 = visual.ImageStim(win, image="../design/visual_dragon2_sm.jpg",
                           pos = (7.0, 5.0))

blue_egg = visual.ImageStim(win, image="../design/dragonegg_blue.png",
                            pos = (0, 0))
red_egg = visual.ImageStim(win, image="../design/dragonegg_red.png",
                           pos = (0, 0))
positive_feedback = visual.ImageStim(win, image="../design/positive.png", 
                                     pos=(0,0), size=2)
negative_feedback = visual.ImageStim(win, image="../design/negative.png", 
                                     pos=(0,0), size=2)
message = visual.TextStim(win, text="press left or right arrow key", pos = (0,0))

def showEgg(time=eggTime):
    """randomly pick a red or blue egg, show it for time=time
    and return color picked"""
    color = random.choice(['red', 'blue'])
    egg = red_egg if color == 'red' else blue_egg
    egg.draw()
    win.flip()
    core.wait(time)
    return color

#def questionAndFeedback(colorEgg='red', feedbackTime=feedbackTime):
def questionAndFeedback(colorEgg='red'):
    """
    colorEgg: color of the egg shown by showEgg function.
    Show the dragons and ask the user to identify
    the mother by clicking left or right arrow, if 
    she does it corrrectly then give positive feedback
    else give a negative one.
    """
    # show the dragons and wait for
    # the user to press the key, keep
    # waiting untill the user presses left
    # or right key.
    dragon1.draw()
    dragon2.draw()
    message.draw()
    win.flip()
    event.clearEvents()
    core.wait(waitTime)
    keys = event.getKeys()

    # event.waitKeys() fun is somehow not working
    # next two lines simulates it recursively simulates that.
    if not ( ('left' in keys) or ('right' in keys) ):
        return questionAndFeedback(colorEgg)
    
    # highlight the choice
    # ask Flavia to send the highlighted dragons.
    
    # check the correctness of the user's choice 
    if colorEgg == 'red':
        chance_correct = probRedEggDrg1 if keys[0] == 'left' else\
                         probRedEggDrg2
    else:
        chance_correct = probBlueEggDrg1 if keys[0] == 'left' else\
                         probBlueEggDrg2
    correctp = (chance_correct > random.uniform(0,1))
    print colorEgg, keys[0], chance_correct, correctp

    # give the feedback
    positive_feedback.draw() if correctp else\
        negative_feedback.draw()
    win.flip()
    core.wait(waitTime)

def main():
    for i in range(ntrial):
        color = showEgg()
        questionAndFeedback(color)
    win.close()
    core.quit()

if __name__ == "__main__":
    main()

win.close()
core.quit()

"""
choose egg randomly
ask user to click left or right
if user click left:
   he is right with 85% prob if egg is red and 35% prob if egg is blue
   show the corr message
if user click right
   he is right with 15% prob for red egg and and 65% prob if egg is blue
  show corr message

repeat
"""        

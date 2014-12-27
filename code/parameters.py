#==================== Parameters for training task ====================

# if stim1 is dominant then:
# P(dragon1|stim1) = max_prob_correct_claasification_given_dominant_stim 
# P(dragon2|stim2) = max_prob_correct_claasification_given_weaker_stim 
MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_DOMINANT_STIM = 0.85
MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_WEAKER_STIM = 0.65

WAIT_TIME = 0.5 # All other waiting times like time till which feedback is shown.

# if in the last ntest trial proportion of
# accurate choices is more then min_accuracy 
#then learning phase is over.
NTEST, MIN_ACCURACY = 10, 0.8

MAX_TRIAL = 2 # if subject has not learned by max_trial then give up on him or her.
INTER_TRIAL_DELAY = 0.5

#==================== Resources ====================

# image and audio files
POSITIVE_FEEDBACK = "../design/positive.png"
NEGATIVE_FEEDBACK = "../design/negative.png"
# dragons
VISUAL_DRAGON1 = "../design/visual_dragon1_sm.jpg"
VISUAL_DRAGON2 = "../design/visual_dragon2_sm.jpg"
AUDIO_DRAGON1 = "../design/sound_files/ba_00.wav"
AUDIO_DRAGON2 = "../design/sound_files/lu_00.wav"
#stims
STIM1_VISUAL = "../design/dragonegg_blue.png"
STIM2_VISUAL = "../design/dragonegg_red.png"
STIM1_AUDIO = "../design/sound_files/dragon1.wav"
STIM2_AUDIO = "../design/sound_files/dragon2.wav"
#start message
START_MESSAGE_VISUAL = "../design/visual_block.txt"
START_MESSAGE_SEMANTIC = "../design/semantic_block.txt"
START_MESSAGE_AUDIO = "../design/auditory_block.txt"
#others
SPEAKER_SYMBOL = "../design/speaker_symbol.png"
FULLSCREEN = False # either True of False, should window be fullscreen.
SLOW_DOWN_SYMBOL = "../design/slowdown.png"
TOO_LATE_SYMBOL = "../design/toolate.png"
#================================================================================
#                       Parameters for the choice task                           
#================================================================================
#                     1: Durations
#                     -------------                    
INTERSTIM_PERIOD = 0.2 
STIM2_CHOICE_DUR = 0.2 # time for which fixation is shown after stim2 and choice.
CHOICE_SCREEN_DUR = 2 # choice screen is shown but subject can not choose yet.
CHOICE_SCREEN_DUR2 = 1 # now subject can choose.
SLOW_DOWN_MSG_DUR = 1.0
TOO_SLOW_MSG_DUR = 0.5
AVERAGE_DELAY = 1 # time between trials, will be jittered for fmri.
MESSAGE_DUR = 1.5 # duration of the block message at the start of the block.
FIXATION_AFTER_MESSAGE_DUR = 0.5 # after block msg fixation is shown for this time.
STIM_DUR =  0.65 #time in seconds for which stimulus is shown set it to 0.8 for 
# training and behavioral choice task.
FIXATION_AFTER_LAST_TRIAL_DUR = 2

#                     2: Keys:
#                      --------
SCANNER_PULSE_KEYS = ["space"]
LEFT_KEY = "left"
RIGHT_KEY = "right"
ESC_KEY = "escape"

#                    3: Others:
#                    ----------
IS_FMRI = False # if this is true then make sure that NTRIAL is 28
SCANNER_MODE = False # when this and IS_FMRI are true then scanner pulse
# starts the experiment otherwise pressing a key in SCANNER_PULSE_KEYS does.
NTRIAL = 2 # number of trials per block.
MAX_OUTCOME = 25
NPLAY = 2 # number of choices from each block to be played for 
# second argument of the function utilities.random_bianry_generator
K_FEEDBACK = 2
K = 2 # other place where this function is used

NUMBER_FIXATION_DIST = 5 # distance between the numbers and the fixation cross
SEMANTIC_STIM1 = "HERBIVORE"
SEMANTIC_STIM2 = "CARNIVORE"

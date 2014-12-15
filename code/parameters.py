# if stim1 is dominant then:
# P(dragon1|stim1) = max_prob_correct_claasification_given_dominant_stim 
# P(dragon2|stim2) = max_prob_correct_claasification_given_weaker_stim 
MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_DOMINANT_STIM = 0.85
MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_WEAKER_STIM = 0.65

STIMULUS_DURATION =  0.8 # time in seconds for which stimulus is shown
WAIT_TIME = 0.5 # All other waiting times like time till which feedback is shown.

# if in the last ntest trial proportion of
# accurate choices is more then min_accuracy 
#then learning phase is over.
NTEST, MIN_ACCURACY = 10, 0.8

MAX_TRIAL = 8 # if subject has not learned by max_trial then give up on him or her.
MAX_STREAK = 5 # maximum number of times a stimulus can appear in a row.
INTER_TRIAL_DELAY = 0.5

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
#==================== Parameters for the choice task====================
INTERSTIM_PERIOD = 0.2 
STIM2_CHOICE_TIME = 0.2 # time for which fixation is shown after stim2 and choice.
CHOICE_SCREEN_TIME = 2.5 
NTRIAL = 10 # number of trials per block.
MAX_OUTCOME = 25
NUMBER_FIXATION_DIST = 5 # distance between the numbers and the fixation cross
AVERAGE_DELAY = 1 # time between trials, will be jittered for fmri.
MESSAGE_DURATION = 1.5 # duration of the block message at the start of the block.
FIXATION_AFTER_MESSAGE_DURATION = 0.5 # after the block message fixation is shown
# for this time
#========================================================================
NPLAY = 2 # number of choices from each block to be played for 

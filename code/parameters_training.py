# if stim1 is dominant then:
# P(dragon1|stim1) = max_prob_correct_claasification_given_dominant_stim 
# P(dragon2|stim2) = max_prob_correct_claasification_given_weaker_stim 
MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_DOMINANT_STIM = 0.85
MAX_PROB_CORRECT_CLAASIFICATION_GIVEN_WEAKER_STIM = 0.65

STIMULUS_TIME =  0.5 # time in seconds for which stimulus is shown
WAIT_TIME = 0.5 # All other waiting times like time till which feedback is shown.

# if in the last ntest trial proportion of
# accurate choices is more then min_accuracy 
#then learning phase is over.
NTEST, MIN_ACCURACY = 5, 0.7
MAX_TRIAL = 6 # if subject has not learn by max_trial then give up on her.
MAX_STREAK = 5 # maximum number of times a stimulus can appear in a row.

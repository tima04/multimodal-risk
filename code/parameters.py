prob_drg1_given_stim1 = 0.85 # probability of the dragon1 given stimulus1 and so on
prob_drg1_given_stim2 = 0.35
prob_drg2_given_stim1 = 1 - prob_drg1_given_stim1
prob_drg2_given_stim2 = 1 - prob_drg1_given_stim2
stimulus_time =  0.5 # time in seconds for which stimulus is shown
wait_time = 0.5 # All other waiting times like time till which feedback is shown.
ntrial =  4 # number of learning trials

# if in the last ntest trial proportion of
# accurate choices is more then min_accuracy 
#then learning phase is over.
ntest, min_accuracy = 10, 0.7
max_trial = 20 # if subject has not learn by max_trial then give up on her. 

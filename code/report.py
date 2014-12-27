import os
from utilities import get_dominant_stimulie
# class SummaryChoiceData(object):
#     def __init__(self, data):
#         self.data = data
#         self.dominant_stimulie = get_dominant_stimulie(data['id'])
        
#     def main(self):
#         #file_name = '../subjects_data/choice-summary-id-%s.txt'%self.data['id']
#         dir_ = os.path.join(os.path.dirname(__file__), '..', 'subjects_data')
#         file_name = 'choice-summary-id-%s.txt'%self.data['id']
#         fl = open(os.path.join(dir_, file_name), 'a')
#         fl.write("Dominant Stimulie: %s\n\n"%self.dominant_stimulie)
#         fl.write("\t\tRun%s\n\t\t===\n"%self.data['run'])
#         for i,mode in enumerate(["Visual", "Auditory", "Semantic"]):
#             fl.write("%s\n========\n"%mode)
#             fl.write(self._summary(mode, self.dominant_stimulie[i]))
#         fl.write("\n\n")
            
#     def _summary(self, mode, dominant_stimulus):
#         rslt = ""
#         trials = self.data[mode]['trials']
#         for i, trial in enumerate(trials):
#             rslt += "\t trial %s\n\t -------\n"%i
#             pleft, pright = (0.85, 0.65) if \
#                             dominant_stimulus == str(trial['first_stim']) else \
#                             (0.65, 0.85)
#             oleft, oright = trial['left_outcome'], trial['right_outcome']
#             rslt += "({0}, {1})\t({2}, {3})\n".format(pleft, oleft, pright, oright)
#             rslt += "EVS: {0} \t   {1}\n".format(pleft*oleft, pright*oright)
#             rslt += "choice: %s\n"%trial['key']
#             rslt += "first_stim: %s\n"%trial['first_stim']
#             rslt += "Is High EV gap? %s\n"%trial['is_high']
#             rslt += "Is One lottery stochatiscally dominant? %s\n"%trial['is_sd']
#         return rslt


class Summary(object):
    def __init__(self, data, is_training):
        self.data = data
        self.dominant_stimulie = get_dominant_stimulie(data['id'])
        self.is_training = is_training
        
    def main(self):
        #file_name = '../subjects_data/choice-summary-id-%s.txt'%self.data['id']
        summary = self._summary_training if self.is_training else \
                  self._summary_choice
        dir_ = os.path.join(os.path.dirname(__file__), '..', 'subjects_data')
        fl_name = '%s-summary-id-%s.txt'%(["choice", "training"][self.is_training],
                                          self.data['id'])
        fl_mode = "w" if self.is_training else "a"
        fl = open(os.path.join(dir_, fl_name), fl_mode)
        fl.write("Dominant Stimulie: %s\n\n"%self.dominant_stimulie)
        if not self.is_training:
            fl.write("\t\tRun%s\n\t\t===\n"%self.data['run'])
        for i,mode in enumerate(["Visual", "Auditory", "Semantic"]):
            fl.write("%s\n========\n"%mode)
            fl.write(summary(mode, self.dominant_stimulie[i]))
        fl.write("\n\n")
            
    def _summary_choice(self, mode, dominant_stimulus):
        rslt = ""
        trials = self.data[mode]['trials']
        for i, trial in enumerate(trials):
            rslt += "\t trial %s\n\t -------\n"%i
            pleft, pright = (0.85, 0.65) if \
                            dominant_stimulus == str(trial['first_stim']) else \
                            (0.65, 0.85)
            oleft, oright = trial['left_outcome'], trial['right_outcome']
            rslt += "({0}, {1})\t({2}, {3})\n".format(pleft, oleft, pright, oright)
            rslt += "EVS: {0} \t   {1}\n".format(pleft*oleft, pright*oright)
            rslt += "choice: %s\n"%trial['key']
            rslt += "first_stim: %s\n"%trial['first_stim']
            rslt += "Is High EV gap? %s\n"%trial['is_high']
            rslt += "Is One lottery stochatiscally dominant? %s\n\n"%trial['is_sd']
        return rslt
        
    def _proportion_positive_feedback(self, trials, stim, key):
        correct  = [t for t in trials if t['correctp'] and 
                    t['stim'] == stim and t['key'] == key]
        total = [t for t in trials if t['stim'] == stim and 
                 t['key'] == key]
        try:
            return len(correct)/float(len(total))
        except ZeroDivisionError:
            return "NAN"
    
    def _summary_training(self, mode, dominant_stimulus):
        rslt = ""
        trials = self.data[mode]['trials']
        ntrials = len(trials)
        nstim1 = len([t for t in trials if t['stim']==1])
        nstim2 = ntrials - nstim1
        positive_feedback1 = self._proportion_positive_feedback(trials,
                                                               1, 'left')
        positive_feedback2 = self._proportion_positive_feedback(trials,
                                                               2, 'right')
        # proportion of +ive feedback when clicked non-optimally
        wrong_positive_feedback1 = self._proportion_positive_feedback(trials,
                                                                      1, 'right')
        wrong_positive_feedback2 = self._proportion_positive_feedback(trials,
                                                               2, 'left')
        rslt += "\t"*2 + mode + "\n" + "="*45 + "\n"
        rslt += "dominant stimulus: %s\n"%dominant_stimulus
        rslt += "Number of trials: %s\n"%ntrials
        rslt += "Number of times stimulus 1 appeared: %s\n"%nstim1
        rslt += "Number of times stimulus 2 appeared: %s\n"%nstim2
        txt = "Proportion of positive feedback when clicked optimally at stim"
        rslt += txt + "%s: %s\n"%(1, positive_feedback1)
        rslt += txt + "%s: %s\n"%(2, positive_feedback2)
        txt = "Proportion of positive feedback when clicked nonoptimally at stim"
        rslt += txt + "%s: %s\n"%(1, wrong_positive_feedback1)
        rslt += txt + "%s: %s\n"%(2, wrong_positive_feedback2)

        return rslt + "\n"

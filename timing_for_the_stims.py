from expyriment import design, control, stimuli
import numpy as np

exp = design.Experiment(name="Experiment", text_size=30)
# expyriment.control.set_develop_mode(True)  # commented because we need fullscreen


N_FLASHES_CATCHCONTROL = [1, 2, 3, 4]
N_BEEPS_CATCH = [1]
N_BEEPS_CONTROL = [0]

N_FLASHES_TEST = [1]
N_BEEPS_TEST = [2, 3, 4]

ALL_STIM_COMBINATIONS = []
STIM_COMBINATIONS_TEST = []
STIM_COMBINATIONS_CONTROL = []
STIM_COMBINATIONS_CATCH = []

CATCH = (N_FLASHES_CATCHCONTROL, N_BEEPS_CATCH, STIM_COMBINATIONS_CATCH)
CONTROL = (N_FLASHES_CATCHCONTROL, N_BEEPS_CONTROL, STIM_COMBINATIONS_CONTROL)
TEST = (N_FLASHES_TEST, N_BEEPS_TEST, STIM_COMBINATIONS_TEST)

CONDITIONS = [CATCH, CONTROL, TEST]

def fill_stim_combinations_lists (condition):
    for N_flash in condition[0] :
        for N_beep in condition[1] :
            ALL_STIM_COMBINATIONS.append((N_flash,N_beep))
            condition[2].append((N_flash,N_beep))

for cond in CONDITIONS:
    fill_stim_combinations_lists(cond)

N_TRIALS_PER_STIM_COMBINATION = 5
control.initialize(exp)



circle_radius = 60
circle_colour= (0,0,0)
screen_colour = (255,255,255)
x_circle,y_circle = 0,0
circle_position = (x_circle, y_circle)
circle_line_width= 0
circle_duration = 10
time_bw_circles = 50
beep_duration = 10
beep_frequency = 3500
beep_db = 80
time_bw_beeps = 57


def get_amplitude_from_intensity(intensity):
	amplitude = 10**(intensity/20)
	return amplitude

beep_amplitude = get_amplitude_from_intensity(beep_db)

cross_cue = stimuli.FixCross(size=(50, 50), line_width=4)

blankscreen = stimuli.BlankScreen(screen_colour)

circle_stim = stimuli.Circle(circle_radius, circle_colour, circle_line_width, circle_position)

beep_stim = stimuli.Tone(beep_duration, beep_frequency, beep_amplitude)

circle_stim.preload()
beep_stim.preload()

for n in range(max(max(N_FLASHES_CATCHCONTROL), max(N_FLASHES_TEST))):
	maxlist_onset_times_flashes.append([(circle_duration+time_bw_circles)*n, 'flash'])

for n in range(max(max(N_BEEPS_CATCH), max(N_BEEPS_CONTROL), max(N_BEEPS_TEST))):
	maxlist_onset_times_beeps.append([(beep_duration+time_bw_beeps)*n, 'beep'])


print(maxlist_onset_times_beeps)
print(maxlist_onset_times_flashes)

block = design.Block()
for condition in CONDITIONS :
    for combination in (condition[2] * N_TRIALS_PER_STIM_COMBINATION):
        t = design.Trial()
        t.set_factor('number_of_flashes', combination[0])
        t.set_factor('number_of_beeps', combination[1])
        t.set_factor('condition', str(condition))
        t.add_stimulus(circle_stim)
        t.add_stimulus(beep_stim)
        block.add_trial(t)

block.shuffle_trials(max_repetitions=1)


exp.add_data_variable_names(
    ['condition','number_of_flashes', 'number_of_beeps', 'respkey', 'RT'])

 
control.start(skip_ready_screen=True)

def present_circle(circle_stim):
    blankscreen.present()
    circle_stim.present()
    reset_stopwatch()
    while property stopwatch_time ==! circle_duration:

    else:
        blankscreen.present()

def present_the_right_trial_stim():
    if onset_times_allstims[index][1] == 'beep':
        trial.stimuli[1].present()
    elif onset_times_allstims[index][1] == 'flash':
        trial.stimuli[0].present()

def erase_potential_visual_stim_from_previous_trial_after_duration(duration):
    exp.clock.wait(duration)
    blankscreen.present()



for trial in block.trials:
    blankscreen.present()
    exp.clock.wait(1000)
    cross_cue.present()
    exp.clock.wait(500)

    onset_times_beeps = maxlist_onset_times_beeps[range(trial.get_factor('number_of_beeps'))]
    onset_times_flashes = maxlist_onset_times_flashes[range(trial.get_factor('number_of_flashes'))]
    onset_times_allstims = onset_times_flashes + onset_times_beeps
    onset_times_allstims.sort(key = lambda i: i[0])

    for index in range(len(onset_times_allstims)):
        if onset_times_allstims[index][0] == 0 :
            present_the_right_trial_stim()
        elif (onset_times_allstims[index][0] - onset_times_allstims[index-1][0]) < circle_duration:
            exp.clock.wait(onset_times_allstims[index][0] - onset_times_allstims[index-1][0])
            present_the_right_trial_stim()
            if onset_times_allstims[index-1][1] == 'flash' and onset_times_allstims[index][1] == 'beep' :
                erase_potential_visual_stim_from_previous_trial_after_duration(circle_duration - (onset_times_allstims[index][0] - onset_times_allstims[index-1][0]))
                onset_times_allstims[index+1][0] = onset_times_allstims[index+1][0] - circle_duration #check later if right formula
        else:
            erase_potential_visual_stim_from_previous_trial_after_duration(circle_duration)
            wait(onset_times_allstims[index][0] - onset_times_allstims[index-1][0])
            present_the_right_trial_stim()






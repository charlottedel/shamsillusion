from expyriment import design, control, stimuli
import numpy as np

exp = design.Experiment(name="Experiment", text_size=30)
# expyriment.control.set_develop_mode(True)  # commented because we need fullscreen

control.initialize(exp)


WHITE = (255, 255, 255)
BLACK = (0,0,0)



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

circle_radius = 60
circle_colour=WHITE
screen_colour = BLACK
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


onset_time_of_flashes = []

for flash_index in range(max(max(N_FLASHES_CATCHCONTROL), max(N_FLASHES_TEST))):
    onset_time_of_flashes.append(flash_index*(circle_duration+time_bw_circles))

onset_time_of_beeps = []

for beep_index in range(max(max(N_BEEPS_CATCH), max(N_BEEPS_CONTROL), max(N_BEEPS_TEST))):
    onset_time_of_beeps.append(beep_index*(beep_duration+time_bw_beeps))

## preparation
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

for trial in block.trials:
    blankscreen.present()
    exp.clock.wait(1000)
    cross_cue.present()
    exp.clock.wait(500)

    for x in range(trial.get_factor('number_of_flashes')):
        exp.clock.wait(circle_duration)
        blankscreen.present()
        exp.clock.wait(time_bw_circles)	
        for y in range(trial.get_factor('number_of_beeps')):
            trial.stimuli[1].present()
            exp.clock.wait(time_bw_beeps)trial.stimuli[0].present()


    	


### insert here some code to present the stimuli and record responses

control.end()


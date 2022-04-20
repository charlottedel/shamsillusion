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
STIM_COMBINATIONS = []

for i in N_FLASHES_CATCHCONTROL:
	for j in N_BEEPS_CONTROL:
		STIM_COMBINATIONS.append((i,j))
for i in N_FLASHES_CATCHCONTROL:
	for j in N_BEEPS_CATCH:
		STIM_COMBINATIONS.append((i,j))
for i in N_FLASHES_TEST:
	for j in N_BEEPS_TEST:
		STIM_COMBINATIONS.append((i,j))

N_TRIALS_PER_STIM_COMBINATION = 5

circle_radius = 60
circle_colour=WHITE
screen_colour = BLACK
x_circle,y_circle = 0,0
circle_position = (x_circle, y_circle)
circle_line_width= 0
beep_duration = 10
beep_frequency = 3500
beep_db = 80


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


def repeat stimulus N times (stim, N, ):
    for _ in range(N):






## preparation
block = design.Block()
for combination in (STIM_COMBINATIONS * N_TRIALS_PER_STIM_COMBINATION):
    t = design.Trial()
    t.set_factor('number_of_flashes', combination[0])
    t.set_factor('number_of_beeps', combination[1])
    t.add_stimulus(circle_stim)
    t.add_stimulus(beep_stim)
    block.add_trial(t)

block.shuffle_trials(max_repetitions=1)


exp.add_data_variable_names(
    ['number_of_flashes', 'number_of_beeps', 'respkey', 'RT'])


 
control.start(skip_ready_screen=True)

for trial in block.trials:
    blankscreen.present()
    exp.clock.wait(1000)
    cross_cue.present()
    exp.clock.wait(500)

    for x in range(trial.get_factor('number_of_flashes')):
    	trial.stimuli[0].present()
    	exp.clock.wait(10)
    	blankscreen.present()
    	exp.clock.wait(50)
    	for y in range(trial.get_factor('number_of_beeps')):
    		trial.stimuli[1].present()
    		exp.clock.wait(57)
    	


### insert here some code to present the stimuli and record responses

control.end()


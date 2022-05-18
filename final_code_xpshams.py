from expyriment import design, control, stimuli, misc
import numpy as np

exp = design.Experiment(name="Shams Illusion Experiment", text_size=30)
#control.set_develop_mode(True)

control.initialize(exp)


numbers_of_flashes_for_test_trials = [1]
numbers_of_beeps_for_test_trials = [2, 3, 4]

numbers_of_flashes_for_control_trials = [1, 2, 3, 4]
numbers_of_beeps_for_control_trials = [0]

numbers_of_flashes_for_catch_trials = [1, 2, 3, 4]
numbers_of_beeps_for_catch_trials = [1]

numbers_of_flashes_for_each_condition = [numbers_of_flashes_for_test_trials, numbers_of_flashes_for_control_trials, numbers_of_flashes_for_catch_trials]
numbers_of_beeps_for_each_condition = [numbers_of_beeps_for_test_trials, numbers_of_beeps_for_control_trials, numbers_of_beeps_for_catch_trials]

stim_combinations_for_test_trials = []
stim_combinations_for_control_trials = []
stim_combinations_for_catch_trials = []

all_stim_combinations = []

TEST = (numbers_of_flashes_for_test_trials, numbers_of_beeps_for_test_trials, stim_combinations_for_test_trials, 'test')
CONTROL = (numbers_of_flashes_for_control_trials, numbers_of_beeps_for_control_trials, stim_combinations_for_control_trials, 'control')
CATCH = (numbers_of_flashes_for_catch_trials, numbers_of_beeps_for_catch_trials, stim_combinations_for_catch_trials, 'catch')

CONDITIONS = [TEST, CONTROL, CATCH]


def fill_stim_combinations_lists (CONDITION):
    for flash_number in CONDITION[0] :
        for beep_number in CONDITION[1] :
            CONDITION[2].append((flash_number, beep_number))
            all_stim_combinations.append((flash_number,beep_number))

for CONDITION in CONDITIONS:
    fill_stim_combinations_lists(CONDITION)


trials_per_stim_combination = 5


WHITE = (255, 255, 255)
BLACK = (0,0,0)

screen_color = BLACK

x_circle,y_circle = 0,0
circle_position = (x_circle, y_circle)
circle_radius = 60
circle_color= WHITE
circle_line_width= 0
flash_duration = 10
time_bw_flashes = 50

beep_duration = 10
time_bw_beeps = 57
beep_frequency = 3500
beep_intensity = 80

def get_amplitude_from_intensity(intensity):
    amplitude = 10**(intensity/20)
    return amplitude

beep_amplitude = get_amplitude_from_intensity(beep_intensity)

cross_cue_size= (50,50)
cross_cue_line_width=4

circle_stim = stimuli.Circle(circle_radius, circle_color, circle_line_width, circle_position)
beep_stim = stimuli.Tone(beep_duration, beep_frequency, beep_amplitude)

circle_stim.preload()
beep_stim.preload()

cross_cue = stimuli.FixCross(cross_cue_size, line_width=cross_cue_line_width)
blankscreen = stimuli.BlankScreen(screen_color)


instructions = stimuli.TextScreen("Instructions",

    f"""When you see a disk flashing on the screen, your task is to report how many times it flashed in a row by pressing the right number key.

    You will hear beeping sounds during this experiment, which you don't have to pay attention to. 

    There will be {trials_per_stim_combination*len(all_stim_combinations)} trials in total. 

    Press the space bar to start.""")


exp.add_data_variable_names(['condition','number_of_flashes', 'number_of_beeps', 'respkey', 'RT'])

#instead of number stim : combination?


block = design.Block()
for CONDITION in CONDITIONS :
    for stim_combination in (CONDITION[2] * trials_per_stim_combination):
        t = design.Trial()
        t.set_factor('number_of_flashes', stim_combination[0])
        t.set_factor('number_of_beeps', stim_combination[1])
        t.set_factor('condition', CONDITION[3])
        t.add_stimulus(circle_stim)
        t.add_stimulus(beep_stim)
        block.add_trial(t)

block.shuffle_trials(max_repetitions=1)

def get_maximal_number_of_a_stim_in_trials(numbers_of_the_stim_for_each_condition):
    maximal_stim_number_in_trials = max(max(numbers_of_the_stim_for_each_condition[0]), max(numbers_of_the_stim_for_each_condition[1]), max(numbers_of_the_stim_for_each_condition[2]))
    return maximal_stim_number_in_trials

maximal_flash_number = get_maximal_number_of_a_stim_in_trials(numbers_of_flashes_for_each_condition)
maximal_beep_number = get_maximal_number_of_a_stim_in_trials(numbers_of_beeps_for_each_condition)

flash_onset_times_for_maximal_trial = []
flash_offset_times_for_maximal_trial = []
beep_onset_times_for_maximal_trial = []

for flash_index in range(maximal_flash_number):
        flash_onset_times_for_maximal_trial.append(((flash_duration + time_bw_flashes)*flash_index, 'flash', 'onset'))
        flash_offset_times_for_maximal_trial.append(((flash_duration + time_bw_flashes)*flash_index + flash_duration, 'flash', 'offset'))

for beep_index in range(maximal_beep_number):
        beep_onset_times_for_maximal_trial.append(((beep_duration + time_bw_beeps)*beep_index, 'beep', 'onset'))



control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait_char(" ")

max_response_delay = 1200


for trial in block.trials:

    flash_onset_times_for_trial = flash_onset_times_for_maximal_trial[0 : trial.get_factor('number_of_flashes')]
    flash_offset_times_for_trial = flash_offset_times_for_maximal_trial[0 : trial.get_factor('number_of_flashes')]
    beep_onset_times_for_trial = beep_onset_times_for_maximal_trial[0 : trial.get_factor('number_of_beeps')]
    onset_times_all_stims_for_trial = flash_onset_times_for_trial + beep_onset_times_for_trial
    onset_times_all_stims_for_trial.sort(key = lambda i: i[0])

    timed_stim_events_for_trial = flash_onset_times_for_trial + flash_offset_times_for_trial + beep_onset_times_for_trial
    timed_stim_events_for_trial.sort(key = lambda i: i[0])

    first_onset_time = onset_times_all_stims_for_trial[0][0]
    times_bw_events_in_trial= [first_onset_time]

    for event_index in range(len(timed_stim_events_for_trial)-1):
        times_bw_events_in_trial.append(timed_stim_events_for_trial[event_index + 1][0] - timed_stim_events_for_trial[event_index][0])

    onset_times_all_stims_for_trial = flash_onset_times_for_trial + beep_onset_times_for_trial
    onset_times_all_stims_for_trial.sort(key = lambda i: i[0])

    blankscreen.present()
    exp.clock.wait(300)
    cross_cue.present()
    exp.clock.wait(1000)

    for event_index in range(len(timed_stim_events_for_trial)):
        exp.clock.wait(times_bw_events_in_trial[event_index])
        if timed_stim_events_for_trial[event_index][2] == 'onset':
            if timed_stim_events_for_trial[event_index][1] == 'flash':
                trial.stimuli[0].present()
            elif timed_stim_events_for_trial[event_index][1]== 'beep':
                trial.stimuli[1].present()
        elif timed_stim_events_for_trial[event_index][2] == 'offset':
            blankscreen.present()


    possible_respkeys = [misc.constants.K_ALL_DIGITS + misc.constants.K_ALL_KEYPAD_DIGITS]
    key, rt = exp.keyboard.wait(duration=max_response_delay)

    exp.data.add([
        trial.get_factor('condition'),
        trial.get_factor('number_of_flashes'), 
        trial.get_factor('number_of_beeps'),
        key, rt])

    exp.clock.wait(max_response_delay)



control.end()













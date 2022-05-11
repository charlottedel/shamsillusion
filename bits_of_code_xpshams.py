from expyriment import design, control, stimuli
import numpy as np

exp = design.Experiment(name="Shams Illusion Experiment", text_size=30)
# expyriment.control.set_develop_mode(True)

control.initialize(exp)


flash_numbers_for_test = [1]
beep_numbers_for_test = [2, 3, 4]

flash_numbers_for_control = [1, 2, 3, 4]
beep_numbers_for_control = [0]

flash_numbers_for_catch = [1, 2, 3, 4]
beep_numbers_for_catch = [1]

flash_numbers_for_each_condition = [flash_numbers_for_test, flash_numbers_for_control, flash_numbers_for_catch]
beep_numbers_for_each_condition = [beep_numbers_for_test, beep_numbers_for_control, beeep_numbers_for_catch]

flash_beep_combinations_for_test = []
flash_beep_combinations_for_control = []
flash_beep_combinations_for_catch = []

all_flash_beep_combinations = []

TEST = (flash_numbers_for_test, beep_numbers_for_test, flash_beep_combinations_for_test)
CONTROL = (flash_numbers_for_control, beep_numbers_for_control, flash_beep_combinations_for_control)
CATCH = (flash_numbers_for_catch, beep_numbers_for_catch, flash_beep_combinations_for_catch)

CONDITIONS = [TEST, CONTROL, CATCH]



def fill_stim_combinations_lists (CONDITION):
    for flash_number in CONDITION[0] :
        for beep_number in CONDITION[1] :
            CONDITION[2].append((flash_number, beep_number))
            all_flash_beep_combinations.append((flash_number,beep_number))

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

cross_cue = stimuli.FixCross(cross_cue_size, cross_cue_line_width)
blankscreen = stimuli.BlankScreen(screen_color)


instructions = stimuli.TextScreen("Instructions",

    f"""Whenever you see a disk flashing on the screen, your task is to report how many times it flashed in a row by pressing the right number key.

    You will also hear some beeping sounds during this experiment; you don't have to pay attention to them. 

    There will be {trials_per_stim_combination*len(range(all_flash_beep_combinations))} in total. 

    Press the space bar to start.""")


exp.add_data_variable_names(['condition','number_of_flashes', 'number_of_beeps', 'respkey', 'RT'])

#instead of number stim : combination?


block = design.Block()
for CONDITION in CONDITIONS :
    for combination in (CONDITION[2] * trials_per_stim_combination):
        t = design.Trial()
        t.set_factor('number_of_flashes', combination[0])
        t.set_factor('number_of_beeps', combination[1])
        #t.set_factor('flash_beep_combination', combination)
        t.set_factor('condition', str(CONDITION))
        t.add_stimulus(circle_stim)
        t.add_stimulus(beep_stim)
        block.add_trial(t)

block.shuffle_trials(max_repetitions=1)

def get_maximal_stim_number_for_a_trial(stim_numbers_for_each_condition):
    maximal_stim_number_for_a_trial = max(max(stim_numbers_for_each_condition[0]), max(stim_numbers_for_each_condition[1]), max(stim_numbers_for_each_condition[2]))
    return maximal_stim_number_for_a_trial

maximal_flash_number_for_a_trial = get_maximal_stim_number_for_a_trial(flash_numbers_for_each_condition)
maximal_beep_number_for_a_trial = get_maximal_stim_number_for_a_trial(beep_numbers_for_each_condition)


for flash_index in range(maximal_flash_number_for_a_trial):
        flash_onset_times_for_maximal_trial.append((flash_duration + time_bw_flashes)*flash_index, 'flash')

for beep_index in range(maximal_beep_number_for_a_trial):
        beep_onset_times_for_maximal_trial.append((beep_duration + time_bw_beeps)*beep_index, 'beep')


control.start(skip_ready_screen=True)
instructions.present()
exp.keyboard.wait_char(" ")

max_response_delay = flash_duration+time_bw_flashes


for trial in block:

    flash_onset_times_for_trial = flash_onset_times_for_maximal_trial[range(trial.get_factor('number_of_flashes'))]
    beep_onset_times_for_trial = beep_onset_times_for_maximal_trial[range(trial.get_factor('number_of_beeps'))]
    onset_times_all_stims_for_trial = flash_onset_times_for_trial + beep_onset_times_for_trial
    onset_times_all_stims_for_trial.sort(key = lambda i: i[0])

    def present_the_right_trial_stim():
        if onset_times_all_stims_for_trial[index][1] == 'flash':
            trial.stimuli[0].present()
        elif onset_times_all_stims_for_trial[index][1] == 'beep':
            trial.stimuli[1].present()

    def erase_potential_previous_circle_stim_after_duration(duration):
        exp.clock.wait(duration)
        blankscreen.present()

    blankscreen.present()
    exp.clock.wait(1000)
    cross_cue.present()
    exp.clock.wait(500)

    for stim_index in (trial.get_factor('number_of_flashes')+trial.get_factor('number_of_beeps')):
        stim_onset_is_zero = (onset_times_all_stims_for_trial[stim_index][0] == 0)
        if stim_onset_is_zero :
            present_the_right_trial_stim()
        else:
            interval_bw_previous_stim_onset_and_current_stim_onset = onset_times_all_stims_for_trial[stim_index][0] - onset_times_all_stims_for_trial[stim_index-1][0]
            new_stim_starts_before_potential_previous_circle_is_erased = (interval_bw_previous_stim_onset_and_current_stim_onset < flash_duration)
            previous_stim_is_flash_and_new_stim_is_beep = (onset_times_all_stims_for_trial[stim_index-1][1] == 'flash' and onset_times_all_stims_for_trial[stim_index][1] == 'beep')
            if new_stim_starts_before_potential_previous_circle_is_erased:
                exp.clock.wait(interval_bw_previous_stim_onset_and_current_stim_onset)
                present_the_right_trial_stim()
                if previous_stim_is_flash_and_new_stim_is_beep :
                    erase_potential_previous_circle_stim_after_duration(flash_duration - interval_bw_previous_stim_onset_and_current_stim_onset)
                    onset_times_all_stims_for_trial[stim_index+1][0] = onset_times_all_stims_for_trial[stim_index+1][0] - (flash_duration - interval_bw_previous_stim_onset_and_current_stim_onset)
                    #pb: by correcting the onset time of the next stim so that it is presented at the right time,
                    #we are changing the interval between the next stim and the stim after this next stim, making it wrong). 

            else:
                erase_potential_previous_circle_stim_after_duration(flash_duration)
                wait(interval_bw_previous_stim_onset_and_current_stim_onset - flash_duration)
                present_the_right_trial_stim()


    possible_respkeys = misc.constants.K_ALL_DIGITS + misc.constants.K_ALL_KEYPAD_DIGITS
    key, rt = exp.keyboard.wait_char(possible_respkeys,
                                     duration=max_response_delay)

    exp.data.add([
        trial.get_factor('condition'),
        trial.get_factor('number_of_flashes'), 
        trial.get_factor('number_of_beeps'),
        key, rt])



control.end()
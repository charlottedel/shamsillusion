### Sham's description of the XP:

> Flashing a uniform *white
disk* (subtending 2 degrees at 5 degrees
eccentricity) for a variable number of times
(*1 to 4, 50 milliseconds apart*) on a *black background.*
Flashes were accompanied by a
variable number of *beeps (0 to 4), each spaced 57
milliseconds apart*. Observers were *asked to
judge* how many visual flashes were presented
on each trial. The trials were randomized
and *each stimulus combination* was run *five times* on eight naive observers.
Surprisingly, observers consistently and
incorrectly reported seeing multiple flashes
whenever a single flash was accompanied
by more than one beep. *Control
conditions (= no beep)* and *catch trials (= single beep)*
indicate that the illusory flashing phenomenon
is a perceptual illusion and is not due
to the difficulty of the task, cognitive bias or
other factors. 

> We next investigated the temporal properties
of this illusion by *varying the relative
timing of visual and auditory stimuli.* The
illusory flashing effect declined from *70
milliseconds* separation onwards. However,
illusory flashing occurred as long as the
beep and flash were within approximately
*100 milliseconds* of each other, which is
consistent with the integration time of polysensory
neurons in the brain1,2


> Across studies, the most commonly used parameters include a 2° white disk presented 5° below fixation for *10ms*, accompanied by two *80dB*, *3500Hz* tones presented for *10ms* each. The first tone is usually presented at the same time as the visual stimulus, or ∼23ms prior to the visual stimulus (Shams et al., 2002). The SOA between the first and the second tone systematically alters the strength of the illusion, therefore the selection of these parameters has important consequences for performance.

## Conditions:

Conditions|Beeps/Flashes | 1 | 2 | 3 | 4 
--- | --- | --- | --- | --- | --- 
Control |0 | |||
Catch |1 | |||
Test|2 | |x|x|x
Test |3 | |x|x|x
Test |4 | |x|x|x

20 combinations, 5 times : 100 trials

But as shown by the crosses in the table indicating the combinations we won't need in the analysis, we actually only have 11 combinations, thus 55 trials. 

Our different conditions are: control (0 beep, 1-4 flashes); catch (1 beep, 1-4 flashes); test (2-4 beeps, 1 flash) 
-> 4x5 control trials, 4x5 catch trials, 3x5 test trials. 


## All the things to solve:

- i don't get the angle values used for the circle stim in shams' description (notably: "subtending 2 degrees at 5 degrees eccentricity"). right now i chose to just drop it and generate the disk i want in my own way, but i could go back to it later. 
- what is the best way to generate the right factor combinations (i.e. the (beep_number, flash_number) pairs)? or do i just import them directly?
- thus: do i generate trials with expyriment, or import trials from csv file?
- how do i present simultaneous audio and image stims correctly? how/where in the code do i repeat them according to factors for each trial, cleanly?
- how do i analyse the data that i get, which is RT, answered number of flashes, and the factors (number of flashes, number of beeps). 
- do i split the trials between catch trials, controls and test trials for data analysis, and how? do i make it a factor?

## Pieces of code to add:

- initialise an experiment on expyriment

- background

- a trial

- circle flash stim

- auditory stim

- randomization












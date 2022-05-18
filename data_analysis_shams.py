from expyriment import design, control, stimuli, misc
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import scipy
import pandas as pd
import glob
import os

files_joined = os.path.join(os.getcwd(), "data/bits_of_code_xpshams2_*.xpd")
list_subject_results_files = glob.glob(files_joined)
df_list =[]

for file in list_subject_results_files:
	df_list.append(pd.read_csv(file,lineterminator='\n',comment='#'))

results_df = pd.concat(df_list, ignore_index=True)

results_df_nonone = results_df[(results_df.RT != 'None') & (results_df.respkey != 'None')]

row_difference = len(results_df.index) - len(results_df_nonone.index)

print('\n' + str(row_difference) + ' trials were deleted because of missing response data.\n ')

for digit in range(10):
	results_df_nonone['respkey'] = results_df_nonone['respkey'].replace(to_replace= str(misc.constants.K_ALL_DIGITS[digit]), value=digit)
	results_df_nonone['respkey'] = results_df_nonone['respkey'].replace(to_replace= str(misc.constants.K_ALL_KEYPAD_DIGITS[digit]), value=digit)

results_df_nonone['respkey'] = results_df_nonone['respkey'].astype(int)
results_df_nonone['RT'] = results_df_nonone['RT'].astype(int)


mean_RT = results_df_nonone['RT'].mean()
print('The mean Response Time is:' + str(mean_RT) + '. Here is a description of the response data by condition:')
print(results_df_nonone.groupby(results_df_nonone.condition)[["RT"]].describe())
print(results_df_nonone.groupby(results_df_nonone.condition)[["respkey"]].describe())

test_trials_2_beeps = results_df_nonone.query('number_of_flashes == 1 & number_of_beeps ==2')
control_or_catch_trials_2_flashes = results_df_nonone.query('number_of_flashes == 2 & (number_of_beeps == 0 | number_of_beeps == 1)')
control_or_catch_trials_1_flash = results_df_nonone.query('number_of_flashes == 1 & (number_of_beeps == 0 | number_of_beeps == 1)')


test_for_experience_of_shams_effect = scipy.stats.ttest_ind(test_trials_2_beeps['respkey'], control_or_catch_trials_1_flash['respkey'])

print(test_for_experience_of_shams_effect)

if test_for_experience_of_shams_effect[1] < 0.05:
	print('\n The difference between test trials with 2 beeps and catch and control trials with 1 flash is significant at the 0.05 level. The beeps seem to have an influence on the perceived number of flashes.\n ')
else:
	print('\n The difference between test trials with 2 beeps and catch and control trials with 1 flash is not significant at the 0.05 level. We cannot claim that the beeps have an influence on the perceived number of flashes.\n ')


test_for_level_of_shams_effect = scipy.stats.ttest_ind(test_trials_2_beeps['respkey'], control_or_catch_trials_2_flashes['respkey'])


print(test_for_level_of_shams_effect)

if test_for_level_of_shams_effect[1] < 0.05:
	print('\n The difference between test trials with 2 beeps and catch and control trials with 2 flashes is significant at the 0.05 level. In the Shams effect trials, people do not seem to perceive the flashes as if there were as many as the beeps.\n ')
else:
	print('\n The difference between test trials with 2 beeps and catch and control trials with 2 flashes is not significant at the 0.05 level. In the Shams effect trials, people seem to perceive the flashes as if there were as many as the beeps.\n ')



print("The present code generates a boxplot to compare RTs between conditions, a plot illustrating our first t-test by showing how the number of beeps affects visual perception in test trials vs. non-test trials, and a plot illustrating our second t-test by showing to what extent people correctly (= linearly) perceive flashes in function of their number in non-test trials, vs. with numerous beeps.")


RT_boxplot = sns.boxplot(x='condition', y='RT', hue='condition', data=results_df_nonone)
RT_boxplot.set_xlabel("Condition", fontsize = 10)
RT_boxplot.set_ylabel("Distribution of RT", fontsize = 10)
plt.title('Reaction time ~ condition')



fig, axes = plt.subplots(2, 1)

mean_respkeys_by_beep_number_for_1_flash = results_df_nonone[results_df_nonone['number_of_flashes'] == 1].groupby(results_df_nonone.number_of_beeps)[["respkey"]].mean()
mean_respkeys_by_beep_number_for_1_flash_df = pd.DataFrame(mean_respkeys_by_beep_number_for_1_flash)


results_df_nonone_notest = results_df_nonone[(results_df_nonone.condition != 'test')]
results_df_nonone_nocatchcontrol = results_df_nonone[(results_df_nonone.condition == 'test')]

mean_respkeys_by_flash_number = results_df_nonone_notest.groupby(['number_of_flashes', 'condition'])[["respkey"]].mean()
mean_respkeys_by_flash_number_df = pd.DataFrame(mean_respkeys_by_flash_number)

mean_respkeys_by_flash_number_test = results_df_nonone_nocatchcontrol.groupby(['number_of_flashes', 'condition'])[["respkey"]].mean()
mean_respkeys_by_flash_number_test_df = pd.DataFrame(mean_respkeys_by_flash_number_test)


plot_shams_effect_1flash = sns.lineplot(x='number_of_beeps', y='respkey', data=mean_respkeys_by_beep_number_for_1_flash_df, ax=axes[0])
axes[0].set_title('Perceived flashes ~ Beeps, for a single flash')
plot_shams_effect_1flash.set_xlabel("Number of beeps", fontsize = 10)
plot_shams_effect_1flash.set_ylabel("Number of perceived flashes", fontsize = 10)
axes[0].set_xticks([0,1,2,3,4])

plot_shams_effect_by_condition = sns.lineplot(x='number_of_flashes', y='respkey', ax=axes[1], hue='condition', data=mean_respkeys_by_flash_number)
plot_shams_effect_by_condition_test_point = sns.scatterplot(x='number_of_flashes', y='respkey', ax=axes[1], hue='condition', palette=['g'], data=mean_respkeys_by_flash_number_test)
axes[1].set_title('Perceived flashes ~ Flashes')
plot_shams_effect_by_condition.set_xlabel("Number of flashes", fontsize = 10)
plot_shams_effect_by_condition.set_ylabel("Number of perceived flashes", fontsize = 10)
axes[1].set_xticks([0,1,2,3,4])



plt.show()






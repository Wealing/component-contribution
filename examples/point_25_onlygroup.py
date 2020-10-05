# this script runs the validation against the feist data. it takes precalculated data from "point_23_4_function" and
# just does some filtering to properly match with Fiest data

import pandas, re

in_filename ='pH72_I01_edited'

comp_contr = pandas.DataFrame.from_csv('../examples/' + in_filename + ".txt", sep='\t',header=0)
comp_contr_group = pandas.DataFrame.from_csv('../examples/' + 'pH72_I01_edited_noRC' + ".txt", sep='\t',header=0)

feist = pandas.DataFrame.from_csv("../../validation/feist_all_reaction_data.tsv", sep='\t', header=0)


# get all the reaction names in the SBML file
with open('../../validation/' + 'allreac_names' + '.txt', 'r') as fp:
    allreac_names = fp.readlines()
allreac_names = [x.strip() for x in allreac_names]


# match reactions
feist_reac_ids = list(feist.index)
matching_ids = [feist_reac_ids.index(reac) for i,reac in enumerate(allreac_names) if reac in feist_reac_ids]
match_ids_feist = feist.iloc[matching_ids, :]


comp_reac_ids = list(comp_contr.index)
matching_ids2 = [i for i,reac in enumerate(allreac_names) if reac in feist_reac_ids]
match_ids_comp = comp_contr.iloc[matching_ids2, :]
match_ids_comp_group = comp_contr_group.iloc[matching_ids2, :]

#transfer over index
match_ids_feist.index=list(match_ids_comp.index)



# identify reactions that component contrib did not calculate for
zeros_and_nans = (match_ids_comp['model.dG0'].isnull() | match_ids_comp['model.dG0'].isin([0]))
zeros_and_nans_group = (match_ids_comp['model.dG0'].isnull() | match_ids_comp['model.dG0'].isin([0]) | match_ids_comp_group['model.dG0'].isnull() | match_ids_comp_group['model.dG0'].isin([0]))

tolerable_error = (match_ids_comp['dG0_std'] < 50)
#non_crazy_values = (match_ids_comp['model.dG0'] < 900 & match_ids_comp['model.dG0'] > -900)
all_rows = (-zeros_and_nans & tolerable_error)
all_rows_group = (-zeros_and_nans_group & tolerable_error)

# match_ids_comp[,'dG0_prime']


a = pandas.concat([match_ids_comp_group.dG0_prime, match_ids_comp_group.dGm_prime,match_ids_comp.dG0_prime, match_ids_comp.dGm_prime,match_ids_feist.deltaGpH72, match_ids_feist.mMdeltaGpH72], axis=1)

a = a[all_rows_group]

# filter out crazy values
#a = a[(a.dG0_prime < 900) & (a.dG0_prime > -900)]

a.to_csv('noRC' + '_data_editing.csv')
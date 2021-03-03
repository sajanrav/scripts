'''
    Script to identify income group of a country and calculate 
    sum of population of each income group. The script ignore's
    countries without an income group. 
'''

import pandas as pd

pop_url = 'https://raw.githubusercontent.com/edomt/owid-tests/main/unwpp_2020.csv'
grouping_url = 'http://databank.worldbank.org/data/download/site-content/CLASS.xls'

if __name__ == "__main__":
    pop_df = pd.read_csv(pop_url)
    group_df = pd.read_excel(grouping_url, sheet_name='List of economies', header=[4], nrows=219, usecols=[0,2,3,5,6,7,8], names=['Id', 'Economy', 'Code', 'Region', 'Income group', 'Lending category', 'Other']).drop([0]).reset_index(drop=True)
    pop_df = pd.merge(pop_df, group_df[['Code', 'Income group']], left_on='iso_code', right_on='Code', how='left')
    pop_df.loc[len(pop_df)] = ['Low income', 'n/a', 2020, pop_df[pop_df['Income group'] == 'Low income']['population'].sum(skipna=True), 'n/a', 'n/a']
    pop_df.loc[len(pop_df)] = ['Low middle income', 'n/a', 2020, pop_df[pop_df['Income group'] == 'Lower middle income']['population'].sum(skipna=True), 'n/a', 'n/a']
    pop_df.loc[len(pop_df)] = ['Upper middle income', 'n/a', 2020, pop_df[pop_df['Income group'] == 'Upper middle income']['population'].sum(skipna=True), 'n/a', 'n/a']
    pop_df.loc[len(pop_df)] = ['Upper income', 'n/a', 2020, pop_df[pop_df['Income group'] == 'High income']['population'].sum(skipna=True), 'n/a', 'n/a']
    pop_df.drop(['Code', 'Income group'], axis=1).to_csv('population_groups.csv', index=False)


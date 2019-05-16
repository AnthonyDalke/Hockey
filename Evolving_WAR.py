# Install necessary packages

import pandas as pd
import numpy as np
import os

# Set working director
os.getcwd()
os.chdir('/Users/anthony/Documents/Hockey')

# Import data
war = pd.read_csv("EvolvingWAR.csv")

# Preview data
war.columns
war.info

# Create pivot table of total WAR and games played by team, season and position
war_pivot = pd.pivot_table(data = war,
                     values = 'WAR',
                     index = ['Team', 'season'],
                     columns = 'position',
                     aggfunc = np.sum,
                     margins = True,
                     fill_value = 0)

war_pivot_calc = pd.concat([war_pivot, war_pivot['D'] / war_pivot['All']], axis = 1)
war_pivot_calc.reset_index(inplace = True)

# Import team totals by season
file_names = ['Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-2.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-3.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-4.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-5.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-6.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-7.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-8.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-9.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-10.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-11.csv',
             'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-12.csv']

file_list = []

for filename in file_names:
    df = pd.read_csv(filename, index_col = None, header = 0)
    file_list.append(df)

teams_seasons = pd.concat(file_list, axis = 0, ignore_index = True)

teams_seasons.head()
war_pivot_calc.head()

# Scrape standings

import requests

response_2019 = requests.get('https://www.nhl.com/standings/2018/conference')
content_2019 = response_2019.content

from bs4 import BeautifulSoup

parser_2019 = BeautifulSoup(content_2019, 'html.parser')
parser_2019.body

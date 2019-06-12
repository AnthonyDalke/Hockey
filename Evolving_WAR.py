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

war_pivot_calc = pd.concat([war_pivot, 
                            war_pivot['D'] / war_pivot['All']], 
                            axis = 1)
war_pivot_calc.reset_index(inplace = True)
war_pivot_calc.columns = ['Team',
                         'Season',
                         'D_WAR',
                         'F_WAR',
                         'All_WAR',
                         'D_Pct']

# Import team Expected Goals totals by season
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

# Create list of unique seasons
seasons_list = teams_seasons['season'].unique().tolist()

### JOIN WAR_PIVOT_CALC AND TEAMS_SEASONS xG_diff ON TEAM AND SEASON 

# Scrape standings

import requests

hf_url = [
        'https://www.hockey-reference.com/leagues/NHL_2019_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2018_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2017_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2016_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2015_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2014_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2013_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2012_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2011_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2010_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2009_standings.html',
        'https://www.hockey-reference.com/leagues/NHL_2008_standings.html'
        ]

response = requests.get('https://www.hockey-reference.com/leagues/NHL_2019_standings.html')
content = response.content

from bs4 import BeautifulSoup as soup

html = soup(content, 'html.parser')
table = html.find_all('tr', attrs = {'class': 'full_table'})

team_tag = []
season_counter = 0
for i in range(0, len(table)):
    team_tag.append(table[i].find('a')['href'])
    str(team_tag[i])
    team_tag[i] = team_tag[i].split('/')
    team_tag[i][0] = seasons_list[season_counter]

points = html.find_all('td', attrs = {'data-stat': 'points'})
points_list = []
for i in range(0, len(points)):
    points_list.append(points[i].text.strip())

season_counter += 1

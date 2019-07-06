# Install necessary packages

import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup as soup
import requests
from pandas import DataFrame
import matplotlib.pyplot as plt
from scipy import stats

# Set working directory
os.getcwd()
os.chdir('/Users/anthony/Documents/Hockey')

# Import data
war = pd.read_csv("EvolvingWAR.csv")

# Preview data
war.columns
war.head()
war.info

# Create pivot table of total WAR and games played by team, season and position
war_pivot = pd.pivot_table(data = war, values = 'WAR', index = ['Team', 'season'], columns = 'position', aggfunc = np.sum, margins = True, fill_value = 0)

# Add calculation of percentage of total WAR contributed by defensemen
war_df = pd.concat([war_pivot, war_pivot['D'] / war_pivot['All'] * 100], axis = 1)
war_df.reset_index(inplace = True)
war_df.columns = ['Team', 'Season', 'D_WAR', 'F_WAR', 'All_WAR', 'D_Pct']

# Import team Expected Goals totals by season
xgoals_files = ['Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-2.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-3.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-4.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-5.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-6.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-7.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-8.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-9.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-10.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-11.csv', 'Evolving_Hockey_standard_team_stats_All_no_adj_2019-05-01-12.csv']
xgoals_data = []

for filename in xgoals_files:
    df = pd.read_csv(filename, index_col = None, header = 0)
    xgoals_data.append(df)

xgoals_df = pd.concat(xgoals_data, axis = 0, ignore_index = True)
xgoals_df.columns = ['Team', 'Season', 'TOI', 'GP', 'GF', 'GA', 'G_Diff', 'xGF', 'xGA', 'xG_Diff', 'SF', 'SA', 'S_Diff', 'FF', 'FA', 'F_Diff', 'CF', 'CA', 'C_Diff']

# Create list of unique seasons
seasons_list = xgoals_df['Season'].unique().tolist()

# Merge war_df and xgoals_df
stats_df1 = pd.merge(war_df[['Team', 'Season', 'All_WAR', 'D_Pct']], xgoals_df[['Team', 'Season', 'G_Diff', 'xG_Diff']], left_on = ['Team', 'Season'], right_on = ['Team', 'Season'])

# Scrape standings
team_season_df = pd.DataFrame()
points_tag = []
season_counter = 0

hf_url = ['https://www.hockey-reference.com/leagues/NHL_2019_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2018_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2017_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2016_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2015_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2014_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2013_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2012_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2011_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2010_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2009_standings.html', 'https://www.hockey-reference.com/leagues/NHL_2008_standings.html']

for url in hf_url:    
    team_tag = []
    response = requests.get(url)
    content = response.content

    html = soup(content, 'html.parser')
    table = html.find_all('tr', attrs = {'class': 'full_table'})
    
    for i in range(0, len(table)):
        team_tag.append(table[i].find('a')['href'])
        str(team_tag[i])
        team_tag[i] = team_tag[i].split('/')
        team_tag[i][0] = seasons_list[season_counter]
    
    points = html.find_all('td', attrs = {'data-stat': 'points'})
    for i in range(0, len(points)):
        points_tag.append(points[i].text.strip())
  
    team_df = DataFrame.from_records(team_tag)
    team_season_df = team_season_df.append(team_df)
    season_counter += 1    

points_df = pd.DataFrame(points_tag, columns = ['Points'])
team_season_df.columns = ['Season', 'DF_Name', 'Team', 'HTML']

# Concatenate points_df and team_season_df
team_season_df.reset_index(inplace = True, drop = True)
points_df.reset_index(inplace = True, drop = True)
stats_df2 = pd.concat([team_season_df, points_df], axis = 1)
stats_df2.drop(['DF_Name', 'HTML'], axis = 1, inplace = True)

# Compare unique values of Seaason and Team columns
df2_season = sorted(stats_df2['Season'].unique().tolist())
df1_season = sorted(stats_df1['Season'].unique().tolist())
df2_team = sorted(stats_df2['Team'].unique().tolist())
df1_team = sorted(stats_df1['Team'].unique().tolist())

season_check = []
team_check = []
for i in range(0, len(df2_season) - 1):
    season_check.append(df2_season[i] == df1_season[i])
for i in range(0, len(df2_team) - 1):
    team_check.append(df2_team[i] == df1_team[i])

# Replace stats_df2 team names that don't match stats_df1

stats_df2['Team'].replace(['LAK', 'NJD', 'SJS', 'TBL', 'VEG', 'PHX'], ['L.A', 'N.J', 'S.J', 'T.B', 'VGK', 'ARI'], inplace = True)

# Create final analysis dataframe

analysis_df = pd.merge(stats_df1, stats_df2, left_on = ['Team', 'Season'], right_on = ['Team', 'Season'])
analysis_df['Points'] = pd.to_numeric(analysis_df['Points'])

# Plot D_Pct against Points
plt.scatter(analysis_df['D_Pct'], analysis_df['Points'])
plt.xlabel('Percentage of WAR from Defensemen')
plt.ylabel('Points')
plt.yticks(np.arange(36, 128, step = 10))
plt.show()

# Investigate and remove outliers
analysis_df[analysis_df['D_Pct'] < -100]
analysis_df[analysis_df['D_Pct'] > 100]
analysis_df_reduced = analysis_df[analysis_df['D_Pct'] > -100]
analysis_df_reduced = analysis_df_reduced[analysis_df_reduced['D_Pct'] < 100]

# Plot D_Pct against Points without outliers
plt.scatter(analysis_df_reduced['D_Pct'], analysis_df_reduced['Points'], c = 'b', edgecolors = 'y')
plt.xlabel('Percentage of WAR from Defensemen')
plt.ylabel('Points')
plt.show()

# Add linear trendline to plot

slope, intercept, r_value, p_value, std_err = stats.linregress(analysis_df_reduced['D_Pct'], analysis_df_reduced['Points'])
line = slope * analysis_df_reduced['D_Pct'] + intercept
plt.plot(analysis_df_reduced['D_Pct'], analysis_df_reduced['Points'], 'o', analysis_df_reduced['D_Pct'], line, mfc = 'b', mec = 'y')
plt.xlabel('Percentage of WAR from Defensemen')
plt.ylabel('Points')
plt.show()
print('r-squared: ', r_value ** 2)

# Plot All_WAR against Points
plt.scatter(analysis_df_reduced['All_WAR'], analysis_df_reduced['Points'], c = 'g', edgecolors = 'y')
plt.xlabel('Total Team WAR')
plt.ylabel('Points')
plt.show()

# Plot G_Diff and xG_Diff against Points
plt.scatter(analysis_df_reduced['G_Diff'], analysis_df_reduced['Points'], c = 'c', edgecolors = 'm')
plt.xlabel('Goal Differential')
plt.ylabel('Points')
plt.show()

plt.scatter(analysis_df_reduced['xG_Diff'], analysis_df_reduced['Points'], c = 'y', edgecolors = 'k')
plt.xlabel('Expected Goal Differential')
plt.ylabel('Points')
plt.show()

# Plot D_Pct against G_Diff and xG_Diff
plt.scatter(analysis_df_reduced['D_Pct'], analysis_df_reduced['G_Diff'], c = 'y', edgecolors = 'b')
plt.xlabel('Percentage of WAR from Defensemen')
plt.ylabel('Goal Differential')
plt.show()

plt.scatter(analysis_df_reduced['D_Pct'], analysis_df_reduced['xG_Diff'], c = 'r', edgecolors = 'b')
plt.xlabel('Percentage of WAR from Defensemen')
plt.ylabel('Expected Goal Differential')
plt.show()

### Extra code
#from sklearn import preprocessing as pp

## Normalized D_Pct and Points fields
#plot_array = analysis_df_reduced[['D_Pct', 'Points']]
#min_max_scaler = pp.MinMaxScaler()
#plot_array = min_max_scaler.fit_transform(plot_array)

## Plot normalized D_Pct against normalized Points
#plt.scatter(plot_array[:, 0], plot_array[:, 1])
#plt.xlabel('Percentage of Normalized WAR from Defensemen')
#plt.ylabel('Normalized Points')
#plt.show()

## Plot trendline of normalized D_Pct vs. Points
#slope, intercept, r_value, p_value, std_err = stats.linregress(plot_array[:,0], plot_array[:,1])
#line = slope * plot_array[:, 0] + intercept
#plt.plot(plot_array[:,0], plot_array[:,1], 'o', plot_array[:,0], line)

#season_check.index(season_check == 'False')
#team_check.index(team_check == 'False')

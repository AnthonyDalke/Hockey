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
                     index = ['season', 'Team'],
                     columns = 'position',
                     aggfunc = np.sum,
                     margins = True,
                     fill_value = 0)

war_pivot_calc = pd.concat([war_pivot, war_pivot['D'] / war_pivot['All']], axis = 1)
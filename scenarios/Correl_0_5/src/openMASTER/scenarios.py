"""Scenario management"""

import os
import shutil
import time
from datetime import datetime

from openMASTER.utils import copy_and_overwrite




# Output Index config file path
excel_path     = "./data/input/openMASTER_Data.xlsm"                
# Loading the Output Index config
index_config   = pd.read_excel(excel_path, sheet_name="Output")

# Scenarios file path
scenarios_path = "./.scenarios"

# Data file path
data_path      = "./data"

# Source file path
src_path       = "./src"



# Loading the scenario name
index_config_columns = list(index_config.columns)                       # Loading all the colums from the "Output" sheet
scenario_column = index_config_columns.index("Scenario name:") + 1      # Finding the scenario name in the list of columns
scenario_name = index_config_columns[scenario_column]                   # Extracting the scenario name

# Loading the scenario description
for row in index_config.index:
    for col_idx, col in enumerate(index_config.columns[:-1]):
        if "Scenario description" in str(index_config.at[row, col]):
            next_column   = index_config.columns[col_idx + 1     ]
            scenario_desc = index_config.at     [row, next_column]

# Loading the actual timestamp
current_timestamp = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")

# Generatinf a Scenario ID
scenarioID = scenario_name+"_"+current_timestamp

# Extracting the sceneario general information
scenario_info = {"ScenarioID": scenarioID , "Scenario name": scenario_name, "Scenario description": scenario_desc}
df_scenario_info = pd.DataFrame.from_dict(scenario_info, orient='index').transpose()

# Creating a folder with the name of the scenario
scenario_folder = os.path.join(scenarios_path, scenarioID)           # Path of the new scenario folder

try:
    # Try to create the folder for the new scenario
    os.mkdir(scenario_folder)
except FileExistsError:
    # If the folder already exists, print a warning message
    print(f"The folder {scenario_folder} already exists in the specified path. Content may be overwritten.")

# Copying the contents from the data folder to the scenario folder
copy_and_overwrite(data_path, scenario_folder)

# Copying the contents from the srcfolder to the scenario folder
copy_and_overwrite(src_path, scenario_folder)



# Scenario Index File Path
scenario_index_path = "./.scenarios/scenarios_index.csv"

# Adding the new scenario to the index of scenarios
if os.path.exists(scenario_index_path):
    
    # If the file exists, load it into a DataFrame
    df_scenario_index = pd.read_csv(scenario_index_path)
    df_scenario_index = pd.concat([df_scenario_index, df_scenario_info], axis=0, ignore_index=True)
else:
    # If the file doesn't exist, create a new DataFrame with the desired columns
    df_scenario_index = df_scenario_info.copy()

df_scenario_index.to_csv(scenario_index_path, index=False)

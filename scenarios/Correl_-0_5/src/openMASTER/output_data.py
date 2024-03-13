# Libraries
import pandas as pd
import math
from pyomo.environ import Var
import os


# =========
# Functions
# =========

# def list_to_excel_table(data, index_dim, output_path, file_name, sheet_name):
#     """
#     Converting a Dataframe containing a Output Variable from a Pyomo model into a
#     more comprehensive Excel table.
# 
#     INPUTS
#     ======
#     data: Pandas Dataframe. Table containing the output variable info
#     index_dim: list. Desired dimensions for the data indexes: index_dim[0]: row index dimensions
#                                                               index_dim[1]: col index dimensions
#     output_path: str. Path to the Output folder.
#     file_name: str. Name of the Excel file to create or where to concatenate new sheets.
#     sheet_name: str. Name of the Excel sheet name where to store the variable info. Usually corresponds to the name of the variable.
#     concatenate_to_table: bool. If True, the results are concatenated to the Excel table indicated in the "output_path",
#                                 but in a new Excel sheet named after the variable "name".
# 
#     """
#     # Set names of the Pyomo Variable
#     set_names = list(data.columns)[:-1]
#     # Sets belonging to the rows
#     row_sets = [set_names[index] for index in range(index_dim[0])]
#     # Sets belonging to the columns
#     column_sets = [set_names[index+index_dim[0]] for index in range(index_dim[1])]
#     if index_dim[0] == 0 and index_dim[1] == 0:
#         pivoted = data.copy()
#     else:
#         # Creating a pivot table index by the row and column sets
#         pivoted = pd.pivot_table(data, index=row_sets, columns=column_sets)
#         pivoted.reset_index(inplace=True)
# 
#     ## Changing the name and position of the indexes
#     if index_dim[0] > 0 and index_dim[1] > 0:
#         # Column indexes
#         col_index_tuple = pivoted.columns.names
#         new_col_index_tuple = tuple([None]*len(col_index_tuple))
#         pivoted.columns.names = new_col_index_tuple
#         # Row indexes
#         for i in range(index_dim[0]):
#             # Changing the value of the indexes
#             pivoted.columns.values[i] = tuple([""]) + tuple([col_index_tuple[j+1] for j in range(index_dim[1]-1)]) + tuple([pivoted.columns[i][0] + " / " + col_index_tuple[index_dim[1]]])
#             # Chaging the name of the indexes
#             pivoted.rename(columns = {pivoted.columns[i]: pivoted.columns.values[i]}, inplace=True)
# 
#     # Eliminating the index from the pivoted table
#     pivoted.index = [""] * len(pivoted)
#     pivoted.rename(columns={"index": ""}, inplace=True)
# 
#     # Excel File Path
#     output_file_path = os.path.join(output_path, file_name)
#     # Checking if the Excel file is already created
#     if os.path.exists(output_file_path):
#         with pd.ExcelWriter(output_file_path, mode='a', engine='openpyxl') as writer:
#             pivoted.to_excel(writer, sheet_name=sheet_name)
#     else:
#         pivoted.to_excel(output_file_path, sheet_name=sheet_name)
#------


def export_model_to_csv(path, output_path, sheetname, m_instance):
    """
    Extracting the information for each Output Variable in a Pyomo model.

    INPUTS
    ======
    path: str. Path of the Excel file containing the variable data.
    output_path. Path to the output folder.
    sheetname: str. Excel sheetname containing the name of the sets for each variable.
    m_instance: Pyomo model instance. 

    RETURNS
    =======
    d_vars: dict. Dictionary containing the values for each variable in the model.
                  {<Variable Name>: dataframe}
    """
    # Dictionary for storing the sets of each variable
    d_vars_sets = {}
    # Dictionary for storing the info of each variable
    d_vars = {}

    # Loading variables info
    df_vars = pd.read_excel(path, sheet_name=sheetname)
    # Setting the first column (variable name) as index
    df_vars.set_index(df_vars.columns[0], inplace=True)


    # Extracting the sets from the Excel file
    for index, row in df_vars.iterrows():
        col_values = list(row[[col for col in df_vars.columns if "DIM_" in col and "ROW" not in col and "COL" not in col]].values)
        col_values = [value for value in col_values if not ((isinstance(value, float) and math.isnan(float(value))) or value.replace(" ","") == "")]
        d_vars_sets[index] = col_values

    # Make the folder if does not exist
    os.makedirs(output_path, exist_ok=True)
    # Iterating all variables in the instance of the model
    for v in m_instance.component_objects(Var):
        if (v.name) in df_vars.index:
            # Extracting variable values
            x_vals = pd.Series(v.extract_values(), name=v.name)
            # Converting the variable data to a dataframe
            df = x_vals.to_frame()
            # Variable index names
            index_names = d_vars_sets[v.name]
            if len(index_names) == 0:
                df = df.reset_index(drop=True)
            else:
                df = df.reset_index()
                df.columns = d_vars_sets[v.name] + [v.name]
            # Updating the variables dictionary with the complete variable info
            d_vars[v.name] = df

            # Exporting the variable info to csv
            df.to_csv(output_path + "/" + v.name + ".csv", index=False)

    return d_vars

#------


def import_results_from_csv(path):
    """
    Load all the csv files corresponding to Variable data, convert them to Pandas Dataframe
    and store them in a Python dictionary.

    INPUT
    =====
    path: str. Path of the folder containing the csv files.

    RETURN
    ======
    d_vars: dict. Dictionary containing the values for each variable in the model.
                  {<Variable Name>: dataframe}
    """
    # Dictionary for storing the info of each variable
    d_vars = {}

    # Extracting the filename of all the files in the folder and
    # processing those that correspond to variables.
    for dir in os.listdir(path):
        # Checking if the file corresponds to a variable
        if dir.startswith("v"):
            # Extracting the name of the variable
            var_name = dir.split(".")[0].strip()
            # Converting the csv file to a Python Dataframe
            df = pd.read_csv(path + "/" + dir)
            # Storing the variable info in a Python dictionary
            d_vars[var_name] = df
    
    return d_vars
            


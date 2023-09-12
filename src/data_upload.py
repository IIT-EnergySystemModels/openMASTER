def input_data():
        
    # Librerías
    import pandas as pd
    import yaml
    import csv

    # Tratamiento de paths
    from pathlib import Path
    with open("config.yaml", 'r') as file:
        cfg = yaml.safe_load(file)
    path_model_in  = Path(cfg['path_model_in' ])
    path_model_out = Path(cfg['path_model_out'])


    # FUNCTIONS
    # =========

    def excel_table_to_list(path, sheetname, index_dim):
        
        # Número de índices de fila
        n_row_index = index_dim[0]
        # Número de índices de columna 
        n_col_index = index_dim[1]

        # Realizamos una carga preliminar del archivo excel para determinar el comienzo y final de los datos
        raw_data = pd.read_excel(path, sheet_name = sheetname, header = None)
        # Buscamos la posición de aquellas celdas que delimiten los márgenes de los datos (KEYWORD: ~BOUNDS~)
        raw_data = pd.melt(raw_data.reset_index(), id_vars=['index'])
        is_bounds = raw_data['value'] == "~BOUNDS~"
        bounds = raw_data.loc[is_bounds, ['index', 'variable']].sort_values(['index', 'variable'])
        # Cambiamos el nombre de las columnas
        bounds.columns = ['row', 'column']

        # Extraemos los márgenes de los datos
        # Recordar que los índice de Python empiezan en 0. Si quisieramos extraer el número de fila o columna real, debemos sumarle 1 a los valores propuestos.
        start_row = min(bounds['row'])                            # Fila inicial
        end_row   = max(bounds['row'])                            # Fila final
        start_col = min(bounds['column']) + 1                     # Columna inicial
        end_col   = max(bounds['column']) - 1                     # Columna final

        # Cargamos la tabla de datos con los márgenes delimitados anteriormente
        data = pd.read_excel(path, sheet_name = sheetname, skiprows=start_row, header=list(range(0,max(1,n_col_index)))).iloc[:end_row-(start_row+max(0,n_col_index-1)),start_col:end_col+1]

        # Nombres de todos los índices
        index_names = list(data.columns[list(range(0,n_row_index))])

        # Nombres de los índices de las filas y columnas
        if n_col_index == 0:
            # Nombres de los índices de las filas
            row_index_names = index_names
            # Nombres de los índices de las columas
            col_index_names = []
        elif n_col_index == 1:
            # Nombres de los índices de las filas
            row_index_names = [name.split("/")[0].strip() for name in index_names]
            # Nombres de los índices de las columnas
            col_index_names = [index_names[0].split("/")[1].strip()]
        elif n_col_index > 1:
            # Nombres de los índices de las filas
            row_index_names = [name[-1].split("/")[0].strip() for name in index_names]
            # Nombres de los índices de las columnas
            col_index_names = [name.split("/")[0].strip() for name in index_names[0][:-1]] + [index_names[0][-1].split("/")[1].strip()]

        # Nombre de las columnas (que no son indices)
        param_column_names = list(data.columns)[n_row_index:]

        # Nombre de los Sets (indices)
        set_names = row_index_names + col_index_names

        # Si se trata de un parámetro, existirá una columna de valores
        if len(param_column_names) > 0:

            # Dataframe donde ir añadiendo los datos reformateados
            new_columns = set_names + [sheetname]
            data_list = pd.DataFrame(columns = new_columns)

            # Dataframe temporal para ir almacenando el valor de los indices y sus parametros
            # Inicializamos el Dataframe con el valor de los índices de las filas
            temp_values = pd.DataFrame(data.iloc[:,list(range(0,n_row_index))])
            temp_values.columns = temp_values.columns.to_flat_index()
            temp_values.columns = row_index_names

            # Extraemos los valores de las columnas (que no son indices)
            for i in range(len(param_column_names)):
                # Nombre de la columna actual
                current_column = param_column_names[i]
                # Extraemos SOLO la columna actual 
                current_column_values = pd.DataFrame(data[current_column])
                # Extraemos los valores de los índices de las columnas
                if n_col_index == 0:
                    col_index_values = []
                elif n_col_index == 1:
                    col_index_values = list(current_column_values.columns)
                elif n_col_index > 1:
                    col_index_values = list(current_column_values.columns)[0] 
                # Añadimos los valores de los índices de las columnas al Dataframe temporal
                for i in range(len(col_index_values)):
                    temp_values[col_index_names[i]] = col_index_values[i]
                # Añadimos el valor de los parámetros
                temp_values[sheetname] = current_column_values.values
                # Rellenamos los valores de los parámetros vacíos con 0.0
                temp_values[sheetname].fillna(0.0, inplace = True)
                # Concatenamos los datos obtenidos a la lista de datos final (data_list)
                data_list = pd.concat([data_list, temp_values], ignore_index=True)
        
        # Si se trata de un Set, NO existirá una columna de valores
        else:
            # Creamos un Dataframe con la información de los índices del Set
            data_list = data.copy()

        # Path donde se encuentra el modelo
        path_model_in = Path(cfg['path_model_in'])
        # Path del fichero a exportar
        filename=str(path_model_in.joinpath(sheetname))+".csv"
        # Exportado de los datos en formato .csv
        data_list.to_csv(filename, index = False)

        return set_names
    #--------


    def main(excel_filepath, csv_file_path):
        """
        Conversión archivo de datos Excel a csv.

        INPUT
        =====
        excel_filepath: Path to the Excel Input file
        csv_filepath: Path to the csv Output file

        """
        # Loading the INDEX page
        index_sheetname = "INDEX"
        index_sheet = pd.read_excel(excel_filepath, sheet_name=index_sheetname)

        # Create new columnn to store the index names
        index_sheet['index_names'] = None
        index_sheet['index_names'] = index_sheet['index_names'].astype(object)

        # Getting the names of Sets and parameters
        sets_and_parameters = index_sheet[(index_sheet.TYPE == "Set") | (index_sheet.TYPE == "Parameter")]

        for index, row in sets_and_parameters.iterrows():
            # Extracting Set & Parameters info from the INDEX Table
            sheetname = row["NAME"]
            dim_row = row["DIM_ROW"]
            dim_col = row["DIM_COL"]
            index_dim = [dim_row, dim_col]

            # Converting the Excel Table to csv
            index_names = excel_table_to_list(excel_filepath, sheetname, index_dim)
            index_sheet.loc[index, 'index_names'] = ",".join(index_names)

            # Saving the Index Config File
            index_sheet.to_csv(csv_file_path)

        

    # EXECUTION
    # =========

    # Path Excel file to convert
    excel_filepath = "./data/input/openMASTER_Data.xlsm" 
    # Path where to store the output csv file
    csv_filepath = "./data/tmp/input/INDEX.csv" 

    # Execute conversion to csv
    main(excel_filepath, csv_filepath)





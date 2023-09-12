###########
# IMPORTS #
###########
import pandas as pd
import os
import plotly.graph_objects as go

#############
# FUNCTIONS #
#############
def create_sankey_diagram(source, target, value, node_labels, link_labels, node_colors, link_colors,
                          node_pad=15, node_thickness=20, line_color="black", line_width=0.5,
                          font_size=10, font_color="black", font_family="Arial",
                          plot_bgcolor=None, paper_bgcolor=None,
                          plot_title = "", units = "GWh"):
    """
    Create a Sankey diagram using Plotly graph_objects.
    
    Args:
        source (list): List of source node indices.
        target (list): List of target node indices.
        value (list): List of values representing the flow between source and target nodes.
        node_labels (list): List of labels for each node.
        link_labels (list): List of labels for each link.
        node_colors (list): List of colors for each node.
        link_colors (list): List of colors for each link.
        
    Returns:
        plotly.graph_objects.Sankey: Sankey diagram object.

    """
    sankey = go.Sankey(
        valueformat = ".0f",                                  # Number Format
        valuesuffix = units,                                  # Energy Units
        node=dict(
            pad=node_pad,                                     # Padding between nodes
            thickness=node_thickness,                         # Thickness of the node
            line=dict(color=line_color, width=line_width),    # Node border line properties
            label=node_labels,                                # Labels for each node
            color=node_colors                                 # Colors for each node
        ),
        link=dict(
            source=source,                                    # List of source node indices
            target=target,                                    # List of target node indices
            value=value,                                      # List of values representing the flow between source and target nodes
            label=link_labels,                                # Labels for each link
            color=link_colors                                 # Colors for each link
        )
    )

    # Creating a Plotly Figure for the Sankey Diagram
    figure = go.Figure(data=[sankey])

    # Updating the Layout of the Plotly Figure
    figure.update_layout(
        hovermode = 'x',
        title=plot_title,
        font=dict(size = font_size, color = font_color, family= font_family),
        plot_bgcolor=plot_bgcolor,
        paper_bgcolor=paper_bgcolor
    )
    
    return figure
#------


def sum_values_by_technology(df, selected_year, pe_column, ce_column, value_column):
    # Select rows for the specified year
    df_selected_year = df[df['sYear'] == selected_year]

    # Sum values by Technology and specified columns
    sum_by_technology = df_selected_year.groupby([pe_column, ce_column])[value_column].sum().reset_index()

    return sum_by_technology
#------


def energy_sankey_figure(year, MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH, plot_title=""):

    # Year
    # ####
    selected_year = str(year)

    # Set Mappings 
    ###############
    sPE = pd.read_csv(MAPPINGS_DATA_PATH + "/sPE_mapping.csv")
    SPE_dict = dict(zip(sPE['SPE'].values, sPE['DESCRIPTION'].values))

    CEPri = pd.read_csv(MAPPINGS_DATA_PATH + "/CEPri_mapping.csv")
    CEPri_dict = dict(zip(CEPri['SCE'].values, CEPri['Technology'].values))

    CESec = pd.read_csv(MAPPINGS_DATA_PATH + "/CESec_mapping.csv")
    CESec_dict = dict(zip(CESec['SCE'].values, CESec['Technology'].values))

    TE = pd.read_csv(MAPPINGS_DATA_PATH + "/TE_mapping.csv")
    TE_dict = dict(zip(TE['TE'].values, TE['Fuel'].values))

    def assign_sector(sST):
        if sST.startswith("sST_DSTRA"):
            return "Transportation"
        elif sST.startswith("sST_DSIND"):
            return "Industry"
        elif sST.startswith("sST_DSOTH"):
            return "Residential and Commercial"
        else:
            return "Other"
        
    ST = pd.read_csv(os.path.join(INPUT_DATA_PATH,"sST.csv"))
    ST["Sector"] =  ST["sST"].apply(assign_sector)
    ST_dict = dict(zip(ST['sST'].values, ST['Sector'].values))

    # PE-CEPri / CEPri-TE
    #####################

    # PE - CEPRI
    # ==========
    vQCEPriIN = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQCEPriIN.csv"))
    vQCEPriIN['DESCRIPTION'] = vQCEPriIN['sPE'].map(SPE_dict)
    vQCEPriIN['Technology'] = vQCEPriIN['sCE'].map(CEPri_dict)
    vQCEPriIN['sYear'] = vQCEPriIN['sYear'].str[1:]

    pe_cepri= sum_values_by_technology(vQCEPriIN, selected_year, "DESCRIPTION", "Technology", "vQCEPriIN")

    # CEPRI - TE
    # ==========
    vQCEPriOUT = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQCEPriOUT.csv"))
    vQCEPriOUT['Fuel'] = vQCEPriOUT['sTE'].map(TE_dict)
    vQCEPriOUT['Technology'] = vQCEPriOUT['sCE'].map(CEPri_dict)
    vQCEPriOUT['sYear'] = vQCEPriOUT['sYear'].str[1:]

    cepri_te= sum_values_by_technology(vQCEPriOUT, selected_year, "Fuel", "Technology", "vQCEPriOUT")

    # Dummies
    # =======
    pe_cepri_dummy = pe_cepri[pe_cepri["Technology"].str.contains("Dummy")]
    cepri_te_dummy = cepri_te[cepri_te["Technology"].str.contains("Dummy")]

    cepri_dummy = pd.merge(pe_cepri_dummy,cepri_te_dummy, on ="Technology")[["DESCRIPTION", "Fuel", "vQCEPriIN"]]

    # Dummy Nodes
    cepri_dummy_nodes = list(cepri_dummy['DESCRIPTION'].values)
    cepri_dummy_nodes.extend(list(cepri_dummy['Fuel'].values))
    cepri_dummy_values = list(cepri_dummy['vQCEPriIN'].values)

    # No Dummies
    # ==========
    pe_cepri = pe_cepri[~pe_cepri["Technology"].str.contains("Dummy")]
    cepri_te = cepri_te[~cepri_te["Technology"].str.contains("Dummy")]

    # No Dummy Nodes
    pe_cepri_nodes = list(pe_cepri['DESCRIPTION'].values)
    pe_cepri_nodes.extend(list(pe_cepri['Technology'].values))
    pe_cepri_values = list(pe_cepri['vQCEPriIN'].values)

    cepri_te_nodes = list(cepri_te['Fuel'].values)
    cepri_te_nodes.extend(list(cepri_te['Technology'].values))
    cepri_te_values = list(cepri_te['vQCEPriOUT'].values)

    # TE-CESec
    # ########
    vQCESecIn = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQCESecIn.csv"))
    vQCESecIn['Fuel'] = vQCESecIn['sTE'].map(TE_dict)
    vQCESecIn['Technology'] = vQCESecIn['sCE'].map(CESec_dict)
    vQCESecIn['sYear'] = vQCESecIn['sYear'].str[1:]

    te_cesec = sum_values_by_technology(vQCESecIn, selected_year, "Technology", "Fuel", "vQCESecIN")

    te_cesec_nodes = list(te_cesec['Fuel'].values)
    te_cesec_nodes.extend(list(te_cesec['Technology'].values))

    te_cesec_values = list(te_cesec['vQCESecIN'].values)

    # CESec-TE
    ##########
    vQCESecOut = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQCESecOut.csv"))
    vQCESecOut['Fuel'] = vQCESecOut['sTE'].map(TE_dict)
    vQCESecOut['Technology'] = vQCESecOut['sCE'].map(CESec_dict)
    vQCESecOut['sYear'] = vQCESecOut['sYear'].str[1:]

    cesec_te = sum_values_by_technology(vQCESecOut, selected_year, "Technology", "Fuel", "vQCESecOUT")

    cesec_te_nodes = list(cesec_te['Technology'].values)
    cesec_te_nodes.extend(list(cesec_te['Fuel'].values))

    cesec_te_values = list(cesec_te['vQCESecOUT'].values)

    # TE-CE_Sto
    ###########
    vQCEStoIn = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQCEStoIn.csv"))
    vQCEStoIn['Fuel'] = vQCEStoIn['sTE'].map(TE_dict)
    vQCEStoIn['Technology'] = vQCEStoIn['sCE'].map(CESec_dict)
    vQCEStoIn['sYear'] = vQCEStoIn['sYear'].str[1:]

    te_cesto = sum_values_by_technology(vQCEStoIn, selected_year, "Technology", "Fuel", "vQCEStoIN")

    te_cesto_nodes = list(te_cesto['Technology'].values)
    te_cesto_nodes.extend(list(te_cesto['Fuel'].values))

    te_cesto_values = list(te_cesto['vQCEStoIN'].values)

    # CE_Sto-TE
    ###########
    vQCEStoOut = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQCEStoOut.csv"))
    vQCEStoOut['Fuel'] = vQCEStoOut['sTE'].map(TE_dict)
    vQCEStoOut['Technology'] = vQCEStoOut['sCE'].map(CESec_dict)
    vQCEStoOut['sYear'] = vQCEStoOut['sYear'].str[1:]

    cesto_te = sum_values_by_technology(vQCEStoOut, selected_year, "Technology", "Fuel", "vQCEStoOUT")

    cesto_te_nodes = list(cesto_te['Technology'].values)
    cesto_te_nodes.extend(list(cesto_te['Fuel'].values))

    cesto_te_values = list(cesto_te['vQCEStoOUT'].values)

    # TE-ST
    #######
    vQSTInTE = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQSTInTE.csv"))
    vQSTInTE['Fuel'] = vQSTInTE['sTE'].map(TE_dict)
    vQSTInTE['Sector'] = vQSTInTE['sST'].map(ST_dict)
    vQSTInTE['sYear'] = vQSTInTE['sYear'].str[1:]
    vQSTInTE.rename(columns={"vQSTInTE": "value"}, inplace=True)

    te_st = sum_values_by_technology(vQSTInTE, selected_year, "Fuel", "Sector", "value")

    te_st_nodes = list(te_st['Fuel'].values)
    te_st_nodes.extend(list(te_st['Sector'].values))

    te_st_values = list(te_st['value'].values)

    # Plot Preparation
    ##################
    node_labels = list(set(pe_cepri_nodes + cepri_te_nodes + te_cesec_nodes + cesec_te_nodes + te_cesto_nodes + cesto_te_nodes + te_st_nodes + cepri_dummy_nodes))
    link_values = pe_cepri_values + cepri_te_values + te_cesec_values + cesec_te_values + te_cesto_values + cesto_te_values + te_st_values + cepri_dummy_values

    link_sources = []
    link_targets = []

    for i in range(len(pe_cepri_values)):
        link_sources.append(node_labels.index(list(pe_cepri['DESCRIPTION'].values)[i]))
        link_targets.append(node_labels.index(list(pe_cepri['Technology'].values)[i]))

    for i in range(len(cepri_te_values)):
        link_sources.append(node_labels.index(list(cepri_te['Technology'].values)[i]))
        link_targets.append(node_labels.index(list(cepri_te['Fuel'].values)[i]))

    for i in range(len(te_cesec_values)):
        link_sources.append(node_labels.index(list(te_cesec['Fuel'].values)[i]))
        link_targets.append(node_labels.index(list(te_cesec['Technology'].values)[i]))

    for i in range(len(cesec_te_values)):
        link_sources.append(node_labels.index(list(cesec_te['Technology'].values)[i]))
        link_targets.append(node_labels.index(list(cesec_te['Fuel'].values)[i]))

    for i in range(len(te_cesto_values)):
        link_sources.append(node_labels.index(list(te_cesto['Fuel'].values)[i]))
        link_targets.append(node_labels.index(list(te_cesto['Technology'].values)[i]))

    for i in range(len(cesto_te_values)):
        link_sources.append(node_labels.index(list(cesto_te['Technology'].values)[i]))
        link_targets.append(node_labels.index(list(cesto_te['Fuel'].values)[i]))

    for i in range(len(te_st_values)):
        link_sources.append(node_labels.index(list(te_st['Fuel'].values)[i]))
        link_targets.append(node_labels.index(list(te_st['Sector'].values)[i]))

    for i in range(len(cepri_dummy_values)):
        link_sources.append(node_labels.index(list(cepri_dummy['DESCRIPTION'].values)[i]))
        link_targets.append(node_labels.index(list(cepri_dummy['Fuel'].values)[i]))

    red_mappings= list(SPE_dict.values()) + list(TE_dict.values())
    node_colors = ['rgba(255,0,0,0.8)' if node in red_mappings else 'rgba(0,255,0,0.8)' for node in node_labels]    

    node_colors = node_colors.copy()
    link_colors = ["rgba(0,0,96,0.2)"] * len(link_values)
    link_labels = [""] * len(link_values)

    sankey_data = {}
    sankey_data['node_labels'] = node_labels
    sankey_data['node_colors'] = node_colors
    sankey_data['link_sources'] = link_sources
    sankey_data['link_targets'] = link_targets
    sankey_data['link_values'] = link_values
    sankey_data['link_colors'] = link_colors
    sankey_data['link_labels'] = link_labels

    # Plot
    ######

    return create_sankey_diagram(link_sources, link_targets, link_values, node_labels, link_labels, node_colors, link_colors, plot_title=plot_title)
#------
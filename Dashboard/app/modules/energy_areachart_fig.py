###########
# IMPORTS #
###########
import pandas as pd
import os
import plotly.express as px

#############
# FUNCTIONS #
#############
def create_stacked_area_chart(df, x, y, color, title='', x_axis_title='', y_axis_title='Energy (GWh)',
                              plot_bg_color='white', chart_width=None, barmode='stack',
                              legend_orientation='h', legend_x=0.5, legend_y=-0.4):
    # Create the area chart using Plotly Express
    fig = px.area(df, x=x, y=y, color=color, title=title)

    # Make the area chart stacked
    fig.update_layout(barmode=barmode)

    # Label the axes
    fig.update_layout(xaxis=dict(title=x_axis_title), yaxis=dict(title=y_axis_title))

    # Show the legend under the graph and customize legend appearance
    fig.update_layout(
        legend=dict(
            orientation=legend_orientation,
            yanchor='middle',
            y=legend_y,  
            xanchor='center',
            x=legend_x,
            title=None,  
            traceorder='normal',
        )
    )

    # Hide the axis
    fig.update_layout(
        xaxis=dict(
            showline=False,
            showticklabels=True,
            showgrid=False,
        ),
        yaxis=dict(
            showline=False,
            showticklabels=True,
            showgrid=False,
        )
    )

    # Set a background color for the plot
    fig.update_layout(
        plot_bgcolor=plot_bg_color,
        width=chart_width
    )

    # Show the chart
    return fig
#------

def assign_sector(sST):
    if sST.startswith("sST_DSTRA"):
        return "Transportation"
    elif sST.startswith("sST_DSIND"):
        return "Industry"
    elif sST.startswith("sST_DSOTH"):
        return "Residential and Commercial"
    else:
        return "Other"
#------

def energy_area_chart_figure(MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH, title='Primary energy consumption'):

    # Data Preprocessing
    ####################
    sPE = pd.read_csv(MAPPINGS_DATA_PATH + "/sPE_mapping.csv")
    SPE_dict = dict(zip(sPE['SPE'].values, sPE['DESCRIPTION'].values))

    vQPEDom = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQPEDom.csv"))
    vQPEDom.rename(columns={"vQPEDom": "value"}, inplace=True)
    vQPEDom['Description'] = vQPEDom['sPE'].map(SPE_dict)
    vQPEDom['sYear'] = vQPEDom['sYear'].str[1:]

    vQPEImp = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQPEImp.csv"))
    vQPEImp.rename(columns={"vQPEImp": "value"}, inplace=True)
    vQPEImp['Description'] = vQPEImp['sPE'].map(SPE_dict)
    vQPEImp['sYear'] = vQPEImp['sYear'].str[1:]

    # Concatenate the dataframes
    primary_energies_grouped = pd.concat([vQPEDom, vQPEImp]).groupby(['Description', 'sYear']).sum('value').reset_index()
    primary_energies_grouped['value'] = primary_energies_grouped['value']/1000
    #primary_energies_grouped = primary_energies_grouped[primary_energies_grouped['sYear'] < "2031"]

    # Plot
    # ====
    return create_stacked_area_chart(primary_energies_grouped, 'sYear', 'value', color='Description', title=title)


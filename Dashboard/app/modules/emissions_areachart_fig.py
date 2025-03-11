###########
# IMPORTS #
###########
import pandas as pd
import os
import plotly.express as px

#############
# FUNCTIONS #
#############
def create_stacked_area_chart(df, x, y, color, title='', x_axis_title='', y_axis_title='CO2 Emissions (Mt)',
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

def emissions_area_chart_figure(MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH, title='Sector-wise CO2 Emission Over Time'):

    # Data Preprocessing
    ####################
    vEmiCO2ST = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vEmiCO2ST.csv"))
    vEmiCO2ST.rename(columns={"vEmiCO2ST":"value"}, inplace=True)
    vEmiCO2ST['Sector'] = vEmiCO2ST['sST'].apply(assign_sector)
    vEmiCO2ST = vEmiCO2ST[["sYear", "Sector", "value"]]
    vEmiCO2ST['sYear'] = vEmiCO2ST['sYear'].str[1:]

    vEmiCO2CE = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vEmiCO2CE.csv"))
    vEmiCO2CE['Sector'] = "Generation"
    vEmiCO2CE.rename(columns={"vEmiCO2CE":"value"}, inplace=True)
    vEmiCO2CE = vEmiCO2CE[["sYear", "Sector", "value"]]
    vEmiCO2CE['sYear'] = vEmiCO2CE['sYear'].str[1:]

    # Concatenate the dataframes
    df_combined = pd.concat([vEmiCO2CE, vEmiCO2ST])

    # Group by 'sYear' and 'Sector' and sum 'value'
    df_grouped = df_combined.groupby(['sYear', 'Sector'])['value'].sum().reset_index()
    df_grouped['value'] = df_grouped['value'] / 1000

    # Plot
    # ====
    return create_stacked_area_chart(df_grouped, 'sYear', 'value', color='Sector', title=title)


###########
# IMPORTS #
###########
import pandas as pd
import os
import plotly.express as px


#############
# FUNCTIONS #
#############
def process_data(df, group_by_cols, sum_col):
    # Group by provided columns, sum the provided column
    df_grouped = df.groupby(group_by_cols)[sum_col].sum().reset_index()

    return df_grouped
#------


def create_donut_chart(df, year, values_col, names_col, hole_size=0.3, 
                       title_text='', center_text='', font_size=20, opacity=0.7, 
                       legend_orientation='v', legend_x=None, legend_y=0.6, 
                       chart_width=500):
    # Filter data for the selected year
    df_year = df[(df['sYear'] == str(year)) & (df[values_col]>0)]

    # Create donut chart
    fig = px.pie(df_year, values=values_col, names=names_col, hole=hole_size, 
                 title=title_text.format(year))

    # Add a text in the center of the donut chart
    fig.add_annotation(
        text=center_text.format(year),
        x=0.5, y=0.5,
        showarrow=False,
        font_size=font_size,
        opacity=opacity
    )

    # Show the legend under the graph and customize legend appearance
    fig.update_layout(
        legend=dict(
            orientation=legend_orientation,
            yanchor='bottom',
            y=legend_y,
            xanchor='center',
            x=legend_x,
            title=None,  
            traceorder='normal',
        )
    )

    # Add a title to the graph
    fig.update_layout(width=chart_width)

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


def energy_pie_chart_figure(year, MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH, title_text = "Renewable Energy Consumption", chart_width=None):

    # Data Preprocessing
    ####################
    sPE = pd.read_csv(MAPPINGS_DATA_PATH + "/sPE_mapping.csv")
    SPE_dict = dict(zip(sPE['SPE'].values, sPE['DESCRIPTION'].values))

    vQPEDom = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQPEDom.csv"))
    vQPEDom.rename(columns={"vQPEDom": "value"}, inplace=True)
    vQPEDom['Description'] = vQPEDom['sPE'].map(SPE_dict)
    vQPEDom['sYear'] = vQPEDom['sYear'].str[1:]

    grouped_df = process_data(vQPEDom, ['Description', 'sYear'], 'value')  

    # Plot
    # ####
    return create_donut_chart(grouped_df, year, 'value', 'Description', title_text= title_text +   " for Year {}", center_text="{}", hole_size=0.45, font_size=25, chart_width=chart_width)    
#------






###########
# IMPORTS #
###########
import pandas as pd
import os
import plotly.express as px

#############
# FUNCTIONS #
#############
def create_stacked_bar_chart(df, x, y, color, title='', x_axis_title='', y_axis_title='Energy (GWh)',
                             plot_bg_color='white', plot_paper_bgcolor='white', 
                             font_size=12, font_color='black', barmode='stack',
                             legend_orientation='v', legend_x=0.5, legend_y=-0.4):
    # Create the bar chart using Plotly Express
    fig = px.bar(df, x=x, y=y, color=color)

    # Make the bar chart stacked
    fig.update_layout(barmode=barmode)

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
            font=dict(
                size=font_size,
                color=font_color
            )
        )
    )

    # Add a title to the graph
    fig.update_layout(title=title)

    # Label the axes
    fig.update_layout(xaxis=dict(title=x_axis_title), yaxis=dict(title=y_axis_title))

    # Set appearance of the axis
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showticklabels=True,
            showgrid=True,
            tickfont=dict(
                size=font_size,
                color=font_color
            )
        ),
        yaxis=dict(
            showline=True,
            showticklabels=True,
            showgrid=True,
            tickfont=dict(
                size=font_size,
                color=font_color
            )
        )
    )

    # Set a background color for the plot and the plot's paper
    fig.update_layout(
        plot_bgcolor=plot_bg_color,
        paper_bgcolor=plot_paper_bgcolor
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


def energy_barchart_figure(MAPPINGS_DATA_PATH, INPUT_DATA_PATH, OUTPUT_DATA_PATH, title='Final energy consumpition'):

    # Data Preprocessing
    ####################
    vQSTInTE = pd.read_csv(os.path.join(OUTPUT_DATA_PATH,"vQSTInTE.csv"))
    vQSTInTE.rename(columns={"vQSTInTE":"value"}, inplace=True)
    vQSTInTE['Sector'] = vQSTInTE['sST'].apply(assign_sector)
    vQSTInTE = vQSTInTE[["sYear", "Sector", "value"]]
    vQSTInTE['sYear'] = vQSTInTE['sYear'].str[1:]
    vQSTInTE = vQSTInTE.groupby(['sYear', 'Sector']).sum()['value'].reset_index()
    vQSTInTE['value'] = vQSTInTE['value']/1000
    #vQSTInTE = vQSTInTE[vQSTInTE['sYear'] < "2031"]
    #vQSTInTE = vQSTInTE[~(vQSTInTE['Sector'] == "Industry")]
    
    # Plot
    ######
    return create_stacked_bar_chart(vQSTInTE, 'sYear', 'value', 'Sector', title=title, x_axis_title='Year', y_axis_title= "Consumption (GWh)", plot_bg_color='white')


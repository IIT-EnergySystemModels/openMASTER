###########
# IMPORTS #
###########
import pandas as pd
import plotly.express as px

#############
# FUNCTIONS #
#############
def process_data(df, group_by_cols, sum_col):
    # Group by provided columns, sum the provided column
    df_grouped = df.groupby(group_by_cols)[sum_col].sum().reset_index()

    return df_grouped

def create_donut_chart(df, year, values_col, names_col, hole_size=0.3, 
                       title_text='', center_text='', font_size=20, opacity=0.7, 
                       legend_orientation='h', legend_x=0.5, legend_y=-0.5, 
                       chart_width=600):
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
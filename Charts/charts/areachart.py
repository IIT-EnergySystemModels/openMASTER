###########
# IMPORTS #
###########
import pandas as pd
import plotly.express as px

#############
# FUNCTIONS #
#############
def create_stacked_area_chart(df, x, y, color, title='', x_axis_title='', y_axis_title='',
                              plot_bg_color='white', chart_width=None, barmode='stack',
                              legend_orientation='h', legend_x=0.5, legend_y=-0.45):
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
    fig.show()
###########
# IMPORTS #
###########

import plotly.graph_objects as go


#############
# FUNCTIONS #
#############

def create_sankey_diagram(source, target, value, node_labels, link_labels, node_colors, link_colors,
                          node_pad=15, node_thickness=20, line_color="black", line_width=0.5,
                          font_size=10, font_color="black", font_family="Arial",
                          plot_bgcolor="white", paper_bgcolor="white",
                          plot_title = "", units = "TWh"):
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
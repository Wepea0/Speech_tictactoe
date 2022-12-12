"""
The purpose of this file is to visualize the data obtained from the class_respones.csv file. This file is used to create a graph that shows the relationship between the different variables in the data set. This file is used to create the graph that is shown in the README.md file.
"""


import pandas as pd
import plotly
import plotly.graph_objs as go

# Read cars data from csv
data = pd.read_csv("class_responses.csv")

# Set marker properties
markersize = data["Going Out"]
markercolor = data["Dogs"]

# Make Plotly figure
fig1 = go.Scatter3d(
    x=data["Sports"],
    y=data["Anime"],
    z=data["Twitter"],
    marker=dict(
        size=markersize,
        color=markercolor,
        opacity=0,
        reversescale=True,
        colorscale="balance",
    ),
    line=dict(width=2),
    mode="markers",
)

# Make Plot.ly Layout
mylayout = go.Layout(
    scene=dict(
        xaxis=dict(title="Sports"),
        yaxis=dict(title="Anime"),
        zaxis=dict(title="Twitter"),
    ),
)

# Plot and save html
plotly.offline.plot(
    {"data": [fig1], "layout": mylayout}, auto_open=True, filename="5D Plot.html"
)

# some code obtained from: https://github.com/ostwalprasad/PythonMultiDimensionalPlots/blob/master/src/5D.py

# %% [markdown]
# ## BUILT LAYOUT

# %%
# import dependencies

from dash import Dash, html, dcc, Input, Output, callback, dash_table
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from dash import dash_table as dt

# %%
# reading in my data
df = pd.read_csv('data.csv')

# %%
df.head()

# %%
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet

app = Dash(__name__, external_stylesheets=stylesheets) # initialize the app

# %%
app = Dash(__name__)
server = app.server

genres = df.track_genre.unique().tolist()

# here I am specifying the number columns I want to use in my datatable
num_columns = ['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'valence', 'tempo', 'time_signature']

app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Spotify Data Center: Get to Know the Numbers Behind the Songs', className="app-header--title") # creating the title of the page 
        ]
    ),
    html.Div(
        children=html.Div([
            html.H1('Description'), # header for our overview below
            html.Div('''
                This dashboard is an interactive interface
                     allowing users to interact with spotify data... 
            ''')
        ])
    ),
    dcc.Dropdown(
        id="filter_dropdown",
        options=[{"label": st, "value": st} for st in df['track_genre'].unique()], # want each genre to be a selection
        placeholder="-Select a Genre-",
        multi=True,
        value=[], # no default value
    ),
    html.Div([
        dash_table.DataTable(
            id="table-container",
            columns=[{"name": i, "id": i} for i in df.columns[:5]], # only want 5 columns to appear (will play with which)
            page_size= 10,
        )
    ], style={'width': '100%'}),
    html.Div(id='datatable-interactivity-container'),
    html.Div([
        dcc.RadioItems(
                num_columns,
                'danceability', # default yaxis is danceability
                id='yaxis-column',
                inline=True # makes them horizontally inline with each other 
            )
    ],style={'width': '49%', 'display': 'inline-block'}), # half the page
    html.Div([
      dcc.RadioItems(
                num_columns,
                'energy', # default xaxis is energy 
                id='xaxis-column',
                inline=True # makes them horizontally inline with each other 
            )
    ],style={'width': '49%', 'display': 'inline-block'}), # half the page inline with the other 
    dcc.Dropdown(
        id='group-by-dropdown',
        options=[{'label': col, 'value': col} for col in df['track_genre'].unique()], # only want options from the genre column
        value=['acoustic'], # default value 
        multi=True,
    ),
    dcc.Graph(id='indicator-graphic')
])


@app.callback(
    Output("table-container", "data"),
    [Input("filter_dropdown", "value")]
)
def update_table(selected_genres):
    if not selected_genres:
        return []
    else:
        filtered_data = pd.concat([df[df['track_genre'] == genre].sample(5) for genre in selected_genres]) # showing a sample of 5 tracks 
        return filtered_data.to_dict("records")

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('yaxis-column', 'value'), # multiple inputs here from the radio items and genre drop down
     Input('xaxis-column', 'value'),
     Input('group-by-dropdown', 'value')])
def update_graph(yaxis_column_name, xaxis_column_name, selected_genres):
    if not selected_genres: # making sure in our genres 
        return {'data': [], 'layout': {}}
    
    fig = px.scatter(df[df['track_genre'].isin(selected_genres)], x=xaxis_column_name, y=yaxis_column_name, color='track_genre',
                     labels={'x': xaxis_column_name, 'y': yaxis_column_name}) # building the scatterplot 
    return fig

if __name__ == "__main__":
    app.run_server(jupyter_mode = 'tab', debug=True)



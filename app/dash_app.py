
import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import uproot

import dash_daq as daq

# from pages.page1 import layout as page1_layout

app = Dash(__name__, use_pages=True)



app.layout = html.Div([
	# html.H1('Multi-page app with Dash Pages'),

    # html.Div(
    #     [
    #         html.Div(
    #             dcc.Link(
    #                 f"{page['name']} - {page['path']}", href=page["relative_path"]
    #             )
    #         )
    #         for page in dash.page_registry.values()
    #     ]
    # ),

	dash.page_container,
    html.Div(id='outer', children=[
    html.Div(id='inner', children=[
        daq.ToggleSwitch(
    label='Kaon from Xic',
    labelPosition='bottom',
    value=True,
    style={'float': 'left','margin': 'auto'},
    id="kaon_button"
),
 daq.ToggleSwitch(
    label='Proton from Xic',
    labelPosition='bottom',
    value=True,
    style={'float': 'left','margin': 'auto'},
    id="proton_button"
),
 daq.ToggleSwitch(
    label='Pion from Xic',
    labelPosition='bottom',
    value=True,
    style={'float': 'left','margin': 'auto'},
    id="pion_button"
),
 daq.ToggleSwitch(
    label='Kaon from Omega_c',
    labelPosition='bottom',
    value=False,
    style={'float': 'left','margin': 'auto'},
    id="kaon2_button"
),
    ], style={'width': '100%', 'display': 'flex','align-items': 'center', 'justify-content': 'center'})
])
])




if __name__ == '__main__':
   app.run_server(debug=True,port=5000,host="0.0.0.0")
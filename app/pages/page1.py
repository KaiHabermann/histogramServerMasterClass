import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np
import uproot
import os
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import curve_fit
from pages.constants import collumn_names, ranges_for_mass_combinations


NBINS = 100
NBINS_MASS = 200
NSTEPS = 20

dash.register_page(__name__,path='/',title='Task 1',
    name='Task 1',top_nav=True,)

local_path=os.path.dirname( 
    os.path.dirname(
        os.path.dirname(__file__)
        )
    )

MY_DATA = os.path.join(local_path,"data/MasterClassAllCuts.root")

df_ = uproot.open(MY_DATA)["DecayTree"].arrays(library="numpy")
# print(df_.keys())
for p in "XYZE":
    df_[f"lab0_P{p}"] = df_[f"lab0_P{p}_DTF_Xic"]
df_[f"lab0_M"] = df_[f"lab0_M_DTF_Xic"]

ranges = {
    "lab0_CHI2NDOF_DTF_Xic": [0,50],
    "lab3_ProbNNk": [0,1],
    "lab2_ProbNNp": [0,1],
    "lab5_ProbNNk": [0,1],
    "lab1_IP_OWNPV": [0,0.09],
    "lab1_IPCHI2_OWNPV": [0,30],
    "lab1_FDCHI2_OWNPV": [0,500],
    "mass_component": [2415,2520],
    "lab1_FD_OWNPV": [min(df_["lab1_FD_OWNPV"]),80],
    "lab0_PT": [min(df_["lab0_PT"]),25000],
    "lab0_M": [min(df_["lab0_M"]),max(df_["lab0_M"])],
    "lab1_M": [min(df_["lab1_M"]),max(df_["lab1_M"])]

}

cuts = {
    "lab3_ProbNNk": None,
    "lab2_ProbNNp": None,
    "lab5_ProbNNk": None,
    "lab1_IPCHI2_OWNPV": None,
    "lab1_FD_OWNPV": None,
    "lab0_PT": None
}

def get_data(mask, key="lab1_IPCHI2_OWNPV"):
    dat = df_[key][mask]
    n, bins = np.histogram(dat, bins=np.linspace(ranges[key][0],ranges[key][1],NBINS if not key == "mass_component" else NBINS_MASS))
    bin_centers = 0.5*(bins[1:] + bins[:-1])
    return bin_centers, n

def get_mask(keys, values):
    mask = np.ones(len(df_["lab1_IPCHI2_OWNPV"]), dtype=bool)
    for key, cut in zip(keys, values):
        lower, upper = cut
        mask = mask & (df_[key] < upper) & (df_[key] > lower)
    return mask

def calculate_mass(mass_particles):
    x = sum([df_[f"lab{i}_PX"]for i in mass_particles])
    Y = sum([df_[f"lab{i}_PY"]for i in mass_particles])
    Z = sum([df_[f"lab{i}_PZ"]for i in mass_particles])
    E = sum([df_[f"lab{i}_PE"]for i in mass_particles])
    mass = np.sqrt(E**2 - x**2 - Y**2 - Z**2)
    if mass_particles == (2,3,4,5):
        # here we want the DTF calculated mass for the Omega_c states
        # DTF will fix the mass of the Xi_c to the PDG value
        mass = df_["lab0_M"]
    return mass

def get_callback(cuts, particle_list):
    def callaback_figures(*args):
        cut_values = args[:len(cuts)]
        cut_keys = list(cuts.keys())
        mask = get_mask(cut_keys, cut_values)

        # select particles, which are toggled on
        particle_toggels = args[len(cuts):]
        particles = tuple( sorted([p[0] for p, v in zip(particle_list, particle_toggels) if v]) )
        output_figures = []
        for cut in cuts:
            e,n = get_data(mask, key=cut)
            df = pd.DataFrame({
            collumn_names[cut]["x"]: e, collumn_names[cut]["y"]: n   
            })
            fig = px.bar(df, x=collumn_names[cut]["x"], y=collumn_names[cut]["y"],log_y=False, range_x = ranges[cut])
            output_figures.append(fig)
        
        mass = calculate_mass(particles)[mask]
        n, bins = np.histogram(mass, bins=NBINS_MASS)
        bin_centers = 0.5*(bins[1:] + bins[:-1])
        df = pd.DataFrame({
        collumn_names["mass_component"]["x"]: bin_centers, collumn_names["mass_component"]["y"]: n   
        })
        fig = px.bar(df, x=collumn_names["mass_component"]["x"], y=collumn_names["mass_component"]["y"],log_y=False)
        output_figures.append(fig)
        return output_figures
    
    return callaback_figures

particle_list = [(3,"kaon"), (2,"proton"), (4,"pion"),(5,"kaon2")]
callback(
    *[Output(f'{cut}_graph', 'figure') for cut in cuts], Output("M_graph", 'figure'),
    *[Input(f'{c}_slider', 'value') for c in cuts], 
    *[Input(f'{name}_button', 'value') for particle_number, name in particle_list])(
        get_callback(cuts, particle_list)
    )

keys = list(cuts.keys())
subplots = [
        html.Div(children=[
        html.Div(children=[dcc.Graph(id=f"{key1}_graph"),
        html.Div( children=[dcc.RangeSlider(*ranges[key1], step=None, tooltip={"placement": "bottom", "always_visible": True}, marks=None,
                value=ranges[key1],
                id=f'{key1}_slider',
                allowCross=False
        )],style={"width":'40vw'}),], style={"width":'45vw', "margin": 0, 'display': 'inline-block',"position": "relative"}),
       html.Div(children=[html.Div( children=[dcc.Graph(id=f"{key2}_graph"),
        dcc.RangeSlider(*ranges[key2], step=None, tooltip={"placement": "bottom", "always_visible": True}, marks=None,
                value=ranges[key2],
                id=f'{key2}_slider',
                allowCross=False
        )],style={"width":'40vw'}),], style={"width":'45vw', "margin": 0, 'display': 'inline-block',"position": "relative"})
    ]) 
    for key1, key2 in zip(keys[0::2],keys[1::2])
]


layout = html.Div(children=[
        html.H1(children='Analysis of LHCb data: Task 1'),
        html.Div(children='''
        Use the Sliders to change the cuts on the data!
        '''),] + subplots+[html.Div(children=[dcc.Graph(id="M_graph")]),]
        #[html.Div(children=[html.Button('Calculate Purity', id='purity_button', n_clicks=0),dcc.Graph(id="M_graph")]),]
          ,id="main_div")


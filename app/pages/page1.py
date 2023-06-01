import dash
from dash import dcc
from dash import html
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np
import uproot
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objects as go
import plotly.express as px
dash.register_page(__name__,path='/task1',title='Task 1',
    name='Task 1',top_nav=True,)

MY_DATA = "/data/MasterClassw4momenta10mil.root"
print("Loading data")
df_ = uproot.open(MY_DATA)["DecayTree"].arrays(library="numpy")
print("Done")

collumn_names = {
        "lab0_CHI2NDOF_DTF_Xic": {"x": "DTF CHI2 / NDF", "y": "Counts"},
        "lab3_ProbNNk": {"x": "ProbNNk", "y": "Counts"},
        "lab2_ProbNNp": {"x": "ProbNNp", "y": "Counts"},
        "lab1_IP_OWNPV": {"x": "Impact Parameter", "y": "Counts"},
        "lab1_IPCHI2_OWNPV": {"x": "IP CHI2", "y": "Counts"},
        "lab1_FDCHI2_OWNPV": {"x": "FD CHI2", "y": "Counts"},
        "lab1_M": {"x": "M", "y": "Counts"},
        "lab0_M": {"x": "M", "y": "Counts"}
}

ranges = {
    "lab0_CHI2NDOF_DTF_Xic": [0,50],
    "lab3_ProbNNk": [0,1],
    "lab2_ProbNNp": [0,1],
    "lab1_IP_OWNPV": [0,1],
    "lab1_IPCHI2_OWNPV": [0,150],
    "lab1_FDCHI2_OWNPV": [0,500],
    "lab1_M": [2415,2520],
    "lab0_M": [min(df_["lab0_M"]),max(df_["lab0_M"])]
}

cuts = {
    # "lab0_CHI2NDOF_DTF_Xic": None,
    "lab3_ProbNNk": None,
    "lab2_ProbNNp": None,
    "lab1_IP_OWNPV": None,
    "lab1_IPCHI2_OWNPV": None,
    # "lab1_FDCHI2_OWNPV": None,
}

mass_particles = ()

for cut in cuts:
    cuts[cut] = ranges[cut]

mask = np.ones(len(df_["lab1_IPCHI2_OWNPV"]), dtype=bool)

def get_data(key="lab1_IPCHI2_OWNPV"):
    print("Getting data")
    global mask
    dat = df_[key][mask]
    n, bins = np.histogram(dat, bins=np.linspace(ranges[key][0],ranges[key][1],100))
    bin_centers = 0.5*(bins[1:] + bins[:-1])
    print("Done")
    return bin_centers, n

def change_mask(key, value):
    global mask
    mask = np.ones(len(df_["lab1_IPCHI2_OWNPV"]), dtype=bool)
    cuts[key] = value
    for key, cut in cuts.items():
        lower, upper = cut
        mask = mask & (df_[key] < upper) & (df_[key] > lower)

def get_callback(cut,norange=False):
    def callaback_figure(value):
        e,n = get_data(key=cut)
        df = pd.DataFrame({
        collumn_names[cut]["x"]: e, collumn_names[cut]["y"]: n   
        })
        if not norange:
            fig = px.bar(df, x=collumn_names[cut]["x"], y=collumn_names[cut]["y"],log_y=False, range_x = ranges[cut])
        else:
            fig = px.bar(df, x=collumn_names[cut]["x"], y=collumn_names[cut]["y"],log_y=False)
        return fig
    return callaback_figure

def change_mass(particle, value):
    global mass_particles
    mass_particles = tuple(sorted([p for p in mass_particles if p != particle]))
    if value:
        mass_particles = tuple(sorted(list(mass_particles) + [particle]))
    print(mass_particles)

def calculate_mass():
    global mass_particles
    
    x = sum([df_[f"lab{i}_PX"]for i in mass_particles])
    Y = sum([df_[f"lab{i}_PY"]for i in mass_particles])
    Z = sum([df_[f"lab{i}_PZ"]for i in mass_particles])
    E = sum([df_[f"lab{i}_PE"]for i in mass_particles])
    mass = np.sqrt(E**2 - x**2 - Y**2 - Z**2)

    df_["lab1_M"] = mass
    mn = np.mean(mass)
    std = np.std(mass)
    ranges["lab1_M"] = [mn - 1.5*std, mn + 1.5*std]
    # ranges["lab1_M"] = [min(df_["lab1_M"]),max(df_["lab1_M"])]
    

def get_mass_callback(particle):
    def f(value):
        print(value)
        change_mass(particle, value)
        calculate_mass()
        return []
    return f


def get_dummy_callback(cut):
    def callaback_figure(value):
        change_mask(cut, value)
        return []
    return callaback_figure

for cut1 in cuts:
    callback(
        Output(f'dummy', 'children',allow_duplicate=True),
        Input(f'{cut1}_slider', 'value'),prevent_initial_call='initial_duplicate')(
            get_dummy_callback(cut1)
        )

    callback(
        Output(f'{cut1}_graph', 'figure'),
        Input(f'dummy', 'children'))(
            get_callback(cut1)
        )

callback(
    Output(f'M_graph', 'figure', allow_duplicate=True),
    Input(f'dummy', 'children'),prevent_initial_call='initial_duplicate')(
        get_callback("lab1_M", norange=True)
    )
 

for i, id in [(3,"kaon"), (2,"proton"), (4,"pion"),(5,"kaon2")]:
    callback(
        Output(f'dummy' ,'children', allow_duplicate=True),
        Input(f'{id}_button', 'value'),prevent_initial_call='initial_duplicate')(
            get_mass_callback( i)
        )

keys = list(cuts.keys())

subplots = [
        html.Div(children=[
        html.Div(children=[dcc.Graph(id=f"{key1}_graph"),
        html.Div( children=[dcc.RangeSlider(*ranges[key1], (max(ranges[key1]) - min(ranges[key1])) / 20,
                value=ranges[key1],
                id=f'{key1}_slider'
        )],style={"width":'40vw'}),], style={"width":'45vw', "margin": 0, 'display': 'inline-block',"position": "relative"}),
       html.Div(children=[html.Div( children=[dcc.Graph(id=f"{key2}_graph"),
        dcc.RangeSlider(*ranges[key2], (max(ranges[key2]) - min(ranges[key2])) / 20,
                value=ranges[key2],
                id=f'{key2}_slider'
        )],style={"width":'40vw'}),], style={"width":'45vw', "margin": 0, 'display': 'inline-block',"position": "relative"})
    ]) 
    for key1, key2 in zip(keys[0::2],keys[1::2])
]


layout = html.Div(children=[
        html.H1(children='Analysis of LHCb data: Task 1'),
        html.Div(children='''
        Use the Sliders to change the cuts on the data!
        '''),] + subplots +[html.Div(children=[html.Button('Calculate Purity', id='purity_button', n_clicks=0),dcc.Graph(id="M_graph")]),
        html.Div(id='putity_text',
             children='Enter a value and press submit'),
            html.Div(id="dummy")
        ], id="main_div")


def get_mass():
    return df_["lab1_M"][mask]  

def get_purity(value):
    # vlaue is not used, I just dont dare remove it because I dont know what I am doing
    import pandas as pd
    import numpy as np

    # from jax import numpy as jnp
    from scipy.optimize import curve_fit

    mass = get_mass() 
    centers, n = get_data("lab1_M")
    def gaussian(x, a, x0, sigma):
        return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))
    
    def background(x, a):
        return abs(a) * np.ones_like(x)
    
    def fit_function(x, a, x0, sigma, b):
        return gaussian(x, a, x0, sigma) + background(x, b)
    
    std = np.std(mass)
    mn = np.mean(mass)
    params, cov_mat = curve_fit(fit_function, centers, n, p0=[max(n)/3., mn , 6., 100], bounds=[
        [0, mn - std, 1., 0],
        [np.inf, mn + std, 9., np.inf]
    ])

    df = pd.DataFrame({
        collumn_names["lab1_M"]["x"]: centers, collumn_names["lab1_M"]["y"]: n   
        })

    fig = px.bar(df, x=collumn_names["lab1_M"]["x"], y=collumn_names["lab1_M"]["y"],log_y=False, range_x=ranges["lab1_M"])
    x = np.linspace(*ranges["lab1_M"], 1000)
    y = fit_function(x, *params)
    fig.add_traces(go.Scatter(x= x, y=y, mode = 'lines',showlegend=False))
    purity = gaussian(x, *params[:3]).sum() / y.sum()
    print(purity)
    if value == 0:
        return fig, "Please press the button to calculate the purity"
    return fig, f"The purity is {purity * 100:.1f}%. This leaves {len(mass) * purity:.0f} signal events."




callback(
    Output(f'M_graph', 'figure', allow_duplicate=True),
    Output(f'putity_text', 'children'),
    Input(f'purity_button', 'n_clicks'),prevent_initial_call='initial_duplicate')(
        get_purity
    )
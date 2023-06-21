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

MY_DATA = "/data/MasterClassAllCuts.root"
NBINS = 100
NBINS_MASS = 200
NSTEPS = 20
print("Loading data")
df_ = uproot.open(MY_DATA)["DecayTree"].arrays(library="numpy")
print("Done")
for p in "XYZE":
    df_[f"lab0_P{p}"] = df_[f"lab0_P{p}_DTF_Xic"]
df_[f"lab0_M"] = df_[f"lab0_M_DTF_Xic"]

collumn_names = {
        "lab0_CHI2NDOF_DTF_Xic": {"x": "DTF CHI2 / NDF", "y": "Counts"},
        "lab3_ProbNNk": {"x": "ProbNNk for Kaon from Xi_c", "y": "Counts"},
        "lab5_ProbNNk": {"x": "ProbNNk for Kaon from Omega_c ", "y": "Counts"},
        "lab2_ProbNNp": {"x": "ProbNNp for Proton", "y": "Counts"},
        "lab1_IP_OWNPV": {"x": "Impact Parameter", "y": "Counts"},
        "lab1_IPCHI2_OWNPV": {"x": "IP", "y": "Counts"},
        "lab1_FDCHI2_OWNPV": {"x": "FD CHI2", "y": "Counts"},
        "mass_component": {"x": "M", "y": "Counts"},
        "lab0_PT": {"x": "Transverse Momentum", "y": "Counts"},
        "lab0_M": {"x": "M", "y": "Counts"},
        "lab1_M": {"x": "M", "y": "Counts"}

}  

ranges = {
    "lab0_CHI2NDOF_DTF_Xic": [0,50],
    "lab3_ProbNNk": [0,1],
    "lab2_ProbNNp": [0,1],
    "lab5_ProbNNk": [0,1],
    "lab1_IP_OWNPV": [0,0.09],
    "lab1_IPCHI2_OWNPV": [0,30],
    "lab1_FDCHI2_OWNPV": [0,500],
    "mass_component": [2415,2520],
    "lab0_PT": [min(df_["lab0_PT"]),max(df_["lab0_PT"])],
    "lab0_M": [min(df_["lab0_M"]),max(df_["lab0_M"])],
    "lab1_M": [min(df_["lab1_M"]),max(df_["lab1_M"])]

}

cuts = {
    # "lab0_CHI2NDOF_DTF_Xic": None,
    "lab3_ProbNNk": None,
    "lab2_ProbNNp": None,
    "lab5_ProbNNk": None,
    "lab1_IPCHI2_OWNPV": None,
    "lab1_IP_OWNPV": None,
    "lab0_PT": None

}

ranges_for_mass_combinations = {
    (2,3,4,5): [2960,3200],
}

mass_particles = ()

for cut in cuts:
    cuts[cut] = ranges[cut]

mask = np.ones(len(df_["lab1_IPCHI2_OWNPV"]), dtype=bool)

def get_data(key="lab1_IPCHI2_OWNPV"):
    print("Getting data")
    global mask
    dat = df_[key][mask]
    n, bins = np.histogram(dat, bins=np.linspace(ranges[key][0],ranges[key][1],NBINS if not key == "mass_component" else NBINS_MASS))
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
    if mass_particles == (2,3,4,5):
        change_mask("lab1_M",[2456.,2480.])
    else:
        if "lab1_M" in cuts:
            del cuts["lab1_M"]
            k = list(cuts.keys())[0]
            change_mask(k,cuts[k])
    
 
def calculate_mass():
    global mass_particles
    
    x = sum([df_[f"lab{i}_PX"]for i in mass_particles])
    Y = sum([df_[f"lab{i}_PY"]for i in mass_particles])
    Z = sum([df_[f"lab{i}_PZ"]for i in mass_particles])
    E = sum([df_[f"lab{i}_PE"]for i in mass_particles])
    mass = np.sqrt(E**2 - x**2 - Y**2 - Z**2)
    if mass_particles == (2,3,4,5):
        mass = df_["lab0_M"]
    df_["mass_component"] = mass
    mn = np.mean(mass)
    std = np.std(mass)
    if ranges_for_mass_combinations.get(mass_particles) is None:
        ranges["mass_component"] = [mn - 1.5*std, mn + 1.5*std]
    else:
        ranges["mass_component"] = ranges_for_mass_combinations[mass_particles]
    
    # ranges["mass_component"] = [min(df_["mass_component"]),max(df_["mass_component"])]
    

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
        get_callback("mass_component", norange=True)
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
        html.Div( children=[dcc.RangeSlider(*ranges[key1], round( (max(ranges[key1]) - min(ranges[key1])) / NSTEPS, 3),
                value=ranges[key1],
                id=f'{key1}_slider'
        )],style={"width":'40vw'}),], style={"width":'45vw', "margin": 0, 'display': 'inline-block',"position": "relative"}),
       html.Div(children=[html.Div( children=[dcc.Graph(id=f"{key2}_graph"),
        dcc.RangeSlider(*ranges[key2], round( (max(ranges[key2]) - min(ranges[key2])) / NSTEPS, 2),
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
    return df_["mass_component"][mask]  

def Omega_Spectrum(value):
    import pandas as pd
    import numpy as np

    # from jax import numpy as jnp
    from scipy.optimize import curve_fit
    mass = get_mass() 
    centers, n = get_data("mass_component")
    def gaussian(x, a, x0, sigma):
        return abs(a) * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))
    
    def background(x, a,c, d):
        return abs(a) * (1-np.exp(-(x -d) * c))
    
    def poly(x,*args):
        return np.polynomial.chebyshev.Chebyshev(args,domain=[min(mass),max(mass)])(x)

    x01 = 3000. 
    x02 = 3050.
    x03 = 3066.
    x04 = 3090.
    x05 = 3119.
    def fit_function(x, a1,  sigma1, a2,  sigma2, a3,  sigma3, a4,  sigma4, a5, sigma5,b , c , d,e ,f):
  
        return (
            gaussian(x, a1, x01, sigma1)+
            gaussian(x, a2, x02, sigma2)+
            gaussian(x, a3, x03, sigma3)+
            gaussian(x, a4, x04, sigma4)+
            gaussian(x, a5, x05, sigma5)+
            background(x, b , c , d)+ 
            poly(x, e, f)
        )
    
    p0 = [
        10,  2.,
        10,  2.,
        10,  2.,
        10,  2.,
        10,  2.,
        10, 0.1, 2910.,
        0, 0
        # 0,0,0, 0, 0
    ]
    upper_limit = [
        500,  4.,
        500,  4.,
        500,  4.,
        500,  4.,
        500,  4.,
        10000, 5000., 2990.,
        2000, 2000
        # 2000, 2000, 2000, 2000, 2000
    ]

    lower_limit = [
        3,  0.2,
        3,  0.2,
        3,  0.2,
        3,  0.2,
        3,  0.2,
        0, 0 , 2900.,
        -2000, -2000,
        # -2000, -2000, -2000, -2000, -2000
    ]
    std = np.std(mass)
    mn = np.mean(mass)
    dn = np.sqrt(n)
    dn[n == 0] = 1
    params, cov_mat = curve_fit(fit_function, centers, n, p0=p0 , bounds=(lower_limit, upper_limit), sigma=dn)

    df = pd.DataFrame({
        collumn_names["mass_component"]["x"]: centers, collumn_names["mass_component"]["y"]: n   
        })

    fig = px.bar(df, x=collumn_names["mass_component"]["x"], y=collumn_names["mass_component"]["y"],log_y=False, range_x=ranges["mass_component"])
    x = np.linspace(*ranges["mass_component"], 1000)
    y = fit_function(x, *params)
    fig.add_traces(go.Scatter(x= x, y=y, mode = 'lines',showlegend=False))
    return fig, "Found 5 Peaks: Yield: " + " Yield: ".join([
        "%.0f"%np.sum(gaussian(centers, a, x0, sigma))
        for a, sigma, x0 in zip(params[:10:2],params[1:10:2],[x01,x02,x03,x04,x05])
    ])

def get_purity(value):
    global mass_particles
    if mass_particles == (2,3,4,5):
        return Omega_Spectrum(value)
    # vlaue is not used, I just dont dare remove it because I dont know what I am doing
    import pandas as pd
    import numpy as np

    # from jax import numpy as jnp
    from scipy.optimize import curve_fit

    mass = get_mass() 
    centers, n = get_data("mass_component")
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
        collumn_names["mass_component"]["x"]: centers, collumn_names["mass_component"]["y"]: n   
        })

    fig = px.bar(df, x=collumn_names["mass_component"]["x"], y=collumn_names["mass_component"]["y"],log_y=False, range_x=ranges["mass_component"])
    x = np.linspace(*ranges["mass_component"], 1000)
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
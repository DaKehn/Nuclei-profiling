import sys
sys.path.append('../')
sys.path.append('../../')
sys.path.append('pages/')

import argparse

from pages import home
from pages import surface
from pages import density
from pages import nucleon

from utilities import scene
from utilities import style

from dash import dcc, html, callback, dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objs as go


from nuclear_profile import NuclearProfile
profile = NuclearProfile.empty()

# prevent_initial_callbacks="initial_duplicate"
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],  
                prevent_initial_callbacks="initial_duplicate",
                suppress_callback_exceptions=True)
server = app.server

surface.add_callbacks(app)
density.add_callbacks(app)
nucleon.add_callbacks(app)

scene_camera = scene.initial_camera.copy()


# icons/images for application
local_image_toogle  = "menu-burger.png"
local_image_home    = "home.png"
local_image_object  = "object.png"
local_image_density = "density.png"
local_image_nucleon = "nucleons.png"


# create a button to toggle the sidebar
toggle_button = dbc.Button(
    html.Img(src=app.get_asset_url(local_image_toogle), alt="Toogle", style=style.ICON),
    className="navbar-toggler",
    color="primary",
    id="toggle-button",
)

sidebar = html.Div(
    [
        toggle_button,
        html.Hr(),
        dbc.Nav(
            [
                dbc.Row([
                    dbc.NavLink([
                        dbc.Col([
                            html.Img(src=app.get_asset_url(local_image_home), alt="", style=style.ICON),
                            html.Span("Home", className="ml-2", style={"margin-left": "1rem"}),
                        ]),
                    ], href="/", active="exact"),
                    dbc.NavLink([
                        dbc.Col([
                            html.Img(src=app.get_asset_url(local_image_object), alt="", style=style.ICON),
                            html.Span("Surface", className="ml-2", style={"margin-left": "1rem"}),
                        ]),
                    ], href="/surface", active="exact"),
                    dbc.NavLink([
                        dbc.Col([
                            html.Img(src=app.get_asset_url(local_image_density), alt="", style=style.ICON),
                            html.Span("Density", className="ml-2", style={"margin-left": "1rem"}),
                        ]),
                    ], href="/density", active="exact"),
                    dbc.NavLink([
                        dbc.Col([
                            html.Img(src=app.get_asset_url(local_image_nucleon), alt="", style=style.ICON),
                            html.Span("Nucleon", className="ml-2", style={"margin-left": "1rem"}),
                        ]),
                    ], href="/nucleon", active="exact"),
                ])
            ],
            id="menu-link",
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=style.SIDEBAR_OPENED,
)

content = html.Div(id="page-content", style=style.CONTENT)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])




@app.callback(
    [   Output("sidebar", "style",  allow_duplicate=True),
        Output("menu-link", "style",     allow_duplicate=True),
        Output("page-content", "style")
        ],
    [Input("toggle-button", "n_clicks")],
    prevent_initial_call=True,
)
def toggle_collapse(n):
    if n and n % 2 != 0:
        sidebar_style = style.SIDEBAR_COLLAPSED
        menu_style = style.MENU_COLLAPESED
    else:
        sidebar_style = style.SIDEBAR_OPENED
        menu_style = style.MENU_OPENED

    # Add margin between sidebar and content
    content_style = dict(style.CONTENT)
    content_style["margin-left"] = sidebar_style["width"]

    return sidebar_style, menu_style, content_style



@app.callback(
        Output("page-content", "children"), 
        [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return dbc.Row(
            [
                dbc.Col(home.home_content, width=12),
            ]
        )
    elif pathname == "/surface":
        return dbc.Row(
            [
                dbc.Col(surface.controls, width=4),
                dbc.Col(surface.layout, width=8)
            ]
        )
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    elif pathname == "/density":
        return dbc.Row(
            [
                dbc.Col(density.controls, width=3),
                dbc.Col(density.layout, width=8),
            ]
        )
    elif pathname == "/nucleon":
        return dbc.Row(
            [
                dbc.Col(nucleon.controls, width=3),
                dbc.Col(nucleon.layout, width=8),
            ]
        )
    

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


# Run the app 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Settings")
    parser.add_argument('--debug',  default=False, action="store_true")
    parser.add_argument('--reload', default=False, action="store_true")
    parser.add_argument('--port',   default=8842,  type=int)
    
    args = parser.parse_args()
    print("Application settings \n", args)
    app.run_server(debug=args.debug, use_reloader=args.reload, port=args.port)

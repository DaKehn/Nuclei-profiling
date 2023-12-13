import sys
sys.path.append('../')

# dash components
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# additional libs
import plotly.graph_objs as go
import numpy as np

# application
from utilities import scene
from utilities import style

from nuclear_profile import NuclearProfile
profile = NuclearProfile.empty()

scene_camera = scene.initial_camera.copy()



style_row = html.Div(
            [
                dbc.Row(
                    [
                        html.H5("Figure style"),
                    ], style={"margin-bottom": '-1rem', "margin-top": "10%"}
                ),
                html.Hr(),
                dbc.Row(
                    [
                        html.H6('Scene3D:'),
                        dcc.Checklist(
                            id="scene-checkboxes",
                            options=['Coordinate frame'],
                            value=[],
                            style=style.CHECKLIST,
                            inputStyle=style.CHECKLIST_INPUT,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        html.H6(' Color scale', style={'margin-top': '2rem'}),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                id="surf-scheme",
                                options=['Plasma', 'Viridis', 'Greys', 'Cividis'],
                                value='Plasma',
                                clearable=False
                        ),
                            ], width=9
                        ),
                        dbc.Col(
                            [
                                dcc.Checklist(
                                    id="surf-scheme-invert",
                                    options=[
                                        {'label': 'Invert', 'value': True}
                                    ],
                                    style=style.CHECKLIST,
                                    inputStyle=style.CHECKLIST_INPUT
                                )
                            ], width=3
                        ),
                        
                    ],
                )
            ], 
        )


controls = html.Div(
    [
        html.Div(
            [
                dbc.Label('Radius', style=style.SLIDER_LABEL),
                dbc.Row(
                    [
                        dbc.Col(dcc.Slider(
                                id='radius-slider',
                                min=1,
                                max=10,
                                step=0.1,
                                value=5,
                                marks={i: str(i) for i in range(1, 11)},
                            ), width=8),
                        dbc.Col(dcc.Markdown('$r$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Markdown('=', mathjax=True), width=1),
                        dbc.Col(dcc.Input(id="radius-value", type='number', min=0, max=50, value=5, style=style.CLEAR_INPUT_BOX), width=2),
                    ], style=style.SLIDER
                )
 
            ]
        ),
        html.Div(
            [
                # Slider to change the quadrupole deformation
                dbc.Label("Quadrupole", style=style.SLIDER_LABEL),
                dbc.Row(
                    [
                        dbc.Col(dcc.Slider(
                            id='beta2-slider',
                            min=0,
                            max=0.5,
                            step=0.05,
                            value=0.15,
                            marks={i: str(i) for i in range(1, 5)},
                        ), width=8),
                        dbc.Col(dcc.Markdown('&beta;$_2$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Markdown('=', mathjax=True), width=1),
                        dbc.Col(dcc.Input(id="beta2-value", type='number', min=0, max=0.5, value=0.15, style=style.CLEAR_INPUT_BOX), width=2),
                    ], style=style.SLIDER
                )
            ]
        ),
        html.Div(
            [
                dbc.Label("Axial assymmetry", style=style.SLIDER_LABEL),
                dbc.Row(
                    [
                        dbc.Col(dcc.Slider(
                        id='gamma-slider',
                        min=0,
                        max=60,
                        step=1,
                        value=0.,
                        marks={i: str(i) for i in range(0, 61, 5)},
                        ), width=8),
                        dbc.Col(dcc.Markdown('&gamma;', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Markdown('=', mathjax=True), width=1),
                        dbc.Col(dcc.Input(id="gamma-value", type='number', min=0, max=60, value=0, style=style.CLEAR_INPUT_BOX), width=2),

                    ], style=style.SLIDER
                )
            ]
        ),
        html.Div(
            [
                dbc.Label("Octupole", style=style.SLIDER_LABEL),
                dbc.Row(
                    [
                        dbc.Col(dcc.Slider(
                        id='beta3-slider',
                        min=0,
                        max=0.1,
                        step=0.001,
                        value=0.,
                        marks={i: str(i) for i in np.linspace(0, 0.1, 2)},
                        ), width=8),
                        dbc.Col(dcc.Markdown('&beta;$_3$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Markdown('=', mathjax=True), width=1),
                        dbc.Col(dcc.Input(id="beta3-value", type='number', min=0, max=0.1, value=0, style=style.CLEAR_INPUT_BOX), width=2),

                    ], style=style.SLIDER
                )
            ]
        ),
        html.Div(
            [
                dbc.Label("Hexadecapole", style=style.SLIDER_LABEL),
                dbc.Row(
                    [
                        dbc.Col(dcc.Slider(
                        id='beta4-slider',
                        min=0,
                        max=0.1,
                        step=0.001,
                        value=0.,
                        marks={i: str(i) for i in np.linspace(0, 0.02, 2)},
                        ), width=8),
                        dbc.Col(dcc.Markdown('&beta;$_4$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Markdown('=', mathjax=True), width=1),
                        dbc.Col(dcc.Input(id="beta4-value", type='number', min=0, max=0.1, value=0, style=style.CLEAR_INPUT_BOX), width=2),
                    ], style=style.SLIDER
                )
            ], style={"margin-bottom": "2rem"}
        ),
        dbc.Row(
            [
                html.H6("show:"),
                dbc.Col(
                            [
                                dcc.Checklist(
                                    id="nuclei-checklist-main",
                                    options=['Density', 'Surface'],
                                    value=['Surface'],
                                    style=style.CHECKLIST,
                                    inputStyle=style.CHECKLIST_INPUT,
                                ),
                            ],width=6
                        ),
                        dbc.Col(
                            [
                                dcc.Checklist(
                                    id="nuclei-checklist-lines",
                                    options=['Wireframe', 'Principal axis'],
                                    value=['Wireframe'],
                                    style=style.CHECKLIST,
                                    inputStyle=style.CHECKLIST_INPUT,
                                ),
                            ],width=6
                        ),
            ], style={"padding-left": "0rem"}
        ),
    style_row,
    ], 
    style={"background-color": "#f8f9fa", "padding-left": "1rem", "padding-right": "1rem", "padding-top": "1rem", "padding-bottom": "5%"}
)


layout = dbc.Container(
    [
        dcc.Graph(id='surface-plot', figure = scene.blank_fig()), 
    ],
    fluid=True,
    style={'margin-top': '0px'}
)






def add_callbacks(app):
    # Define callback to update the plot based on slider value
    @app.callback(
        Output('beta2-slider',  'value'),
        Output('beta2-value',   'value'),
        Output('gamma-slider',  'value'),
        Output('gamma-value',   'value'),
        Output('beta3-slider',  'value'),
        Output('beta3-value',   'value'),
        Output('beta4-slider',  'value'),   
        Output('beta4-value',   'value'),
        Output('surface-plot', 'figure', allow_duplicate=True),
    [
        Input('radius-slider',  'value'),
        Input('beta2-slider',   'value'),
        Input('beta2-value',    'value'),
        Input('gamma-slider',   'value'),
        Input('gamma-value',    'value'),
        Input('beta3-slider',   'value'),
        Input('beta3-value',    'value'),
        Input('beta4-slider',   'value'),
        Input('beta4-value',    'value'),
        Input('nuclei-checklist-main', 'value'),
        Input('nuclei-checklist-lines', 'value'),
        Input('scene-checkboxes', 'value'),
        Input('surf-scheme', 'value'),
        Input('surf-scheme-invert', 'value'),
    ]
    )
    def update_plot(radius, beta2_slider, beta2_value, gamma_slider, gamma_value, beta3_slider, beta3_value, beta4_slider, beta4_value, 
                nuclei_checklist_main, nuclei_checklist_lines, scene_cbox, color_scale, invert_scale):

        # ciruclar feedback between 'slider' and 'input' --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        nuclei_checklist    = np.concatenate([nuclei_checklist_main, nuclei_checklist_lines])


        if "beta2" in trigger_id:
            beta2_slider, beta2_value = map_triger(trigger_id, beta2_slider, beta2_value)
        elif "gamma" in trigger_id:
            gamma_slider, gamma_value = map_triger(trigger_id, gamma_slider, gamma_value)
        elif "beta3" in trigger_id:
            beta3_slider, beta3_value = map_triger(trigger_id, beta3_slider, beta3_value)
        elif "beta4" in trigger_id:
            beta4_slider, beta4_value = map_triger(trigger_id, beta4_slider, beta4_value)

        # ciruclar feedback between 'slider' and 'input' --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        global profile 
        profile = NuclearProfile.empty(radius=radius, beta2=beta2_slider, gamma=gamma_slider, beta3=beta3_slider, beta4=beta4_slider)
        Rx, Ry, Rz = profile.GetSurface()
        Wx, Wy, Wz = profile.GetWireFrame()
        px, py, pz = profile.GetPrincipalAxis()

        # Create a 3D surface plot from tamplet
        fig = go.Figure(scene.init_figure)

        if "Surface" in nuclei_checklist:
            fig.add_trace(go.Surface(
                name='Surface',
                x=Rx, 
                y=Ry, 
                z=Rz, 
                surfacecolor=Rx**2 + Ry**2 + Rz**2, 
                showscale=False, 
                showlegend=False,
                colorscale=color_scale,
                reversescale=True if invert_scale else False
                )
            )

        if "Wireframe" in nuclei_checklist:        
            fig.add_trace(go.Scatter3d(
                name='Wireframe',
                x=Wx, 
                y=Wy, 
                z=Wz, 
                mode='lines',
                showlegend=False,
                line_width=1, 
                line_color='rgba(10,10,10, 1)')
            )

        if "Density" in nuclei_checklist:
            Rhox, Rhoy, Rhoz, density = profile.GetDensityGrid() 
            fig.add_trace(go.Volume(
                    x=Rhox.flatten(), 
                    y=Rhoy.flatten(), 
                    z=Rhoz.flatten(), 
                    value=density.flatten(),
                    isomin=0.01, 
                    isomax=0.4, 
                    opacity=0.05, 
                    surface_count=25, 
                    showscale=False,
                    colorscale=color_scale,
                    reversescale=True if invert_scale else False
                )
            )

        show_prin_axis = True if "Principal axis" in nuclei_checklist else False
        fig.add_trace(go.Scatter3d(
                name='Wireframe',
                x=px, 
                y=py, 
                z=pz, 
                mode='lines',
                showlegend=False,
                line_width=5, 
                line_color=f'rgba(10,10,10, {int(show_prin_axis)})'
            )
        )





        show_axis = True if "Coordinate frame" in scene_cbox else False
        if show_axis:
            fig.update_layout(scene=scene.scene_on)
        else:
            fig.update_layout(scene=scene.scene_off)


        global scene_camera

        # Keep perspective to prevent resetting the camera angle
        if scene_camera:
            fig.update_layout(
                scene_camera_eye=scene_camera['eye'],
                scene_camera_center=scene_camera['center'],
                scene_camera_up=scene_camera['up']
            )


        return beta2_slider, beta2_value, gamma_slider, gamma_value, beta3_slider, beta3_value, beta4_slider, beta4_value, fig
    
    
    @app.callback(
        Output('surface-plot', 'figure', allow_duplicate=True),
    [
        Input('surface-plot', 'figure')
    ],
    prevent_initial_call=True
    )
    def store_initial_camera(fig):
        # Store the initial camera parameters
        global scene_camera

        scene_camera['eye'] = fig['layout']['scene']['camera']['eye']
        scene_camera['center'] = fig['layout']['scene']['camera']['center']
        scene_camera['up'] = fig['layout']['scene']['camera']['up']    
        return fig
    
    
    return update_plot, store_initial_camera



def map_triger(trigger, slider, value):
    if 'value' in trigger:
        slider = value
    elif 'slider' in trigger:
        value = slider
    return slider, value


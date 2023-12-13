import sys
sys.path.append('../')

import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import numpy as np

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
                    ], style={"margin-bottom": '-1rem', "margin-top": "20%"},
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H6('Scene3D:'),
                                dcc.Checklist(
                                    id="scene-3d-checkboxes",
                                    options=['Coordinate frame'],
                                    value=[],
                                    style=style.CHECKLIST,
                                    inputStyle=style.CHECKLIST_INPUT,
                                ),
                            ], width=6
                        ),
                        dbc.Col(
                        [
                            html.H6('Projection:'),
                            dcc.Checklist(
                                id="scene-projection-checkboxes",
                                options=['Contour'],
                                value=[],
                                style=style.CHECKLIST,
                                inputStyle=style.CHECKLIST_INPUT,
                            ),
                        ], width=6
                        ),
                    ],className="g-0"
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
                                )
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
                                ),                                
                            ], width=3, style={"margin-bottom": "3rem"}
                        ),
                    ],
                )           
    ]
)


        

controls = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    [
                        html.H5("Atomic properties")
                    ], style={"margin-bottom": '-1rem'}
                ),
                html.Hr(),
                dbc.Row(
                            [
                                
                                dbc.Col(dcc.Markdown('$p$', mathjax=True, style=style.LATEX), width=1),
                                dbc.Col(dcc.Input(id="proton-input", type='number', min=0, max=150, value=15, step=1, style=style.STEP_INPUT_BOX), width=3),
                                dbc.Col(dcc.Markdown('$n$', mathjax=True, style=style.LATEX), width=1),
                                dbc.Col(dcc.Input(id="neutron-input", type='number', min=0, max=150, value=15, step=1, style=style.STEP_INPUT_BOX), width=3),
                            ],
                        ),
            ], style={"margin-bottom": '7.5%'}
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        html.H5("Nucleon properties")
                    ], style={"margin-bottom": '-1rem'}
                ),
                html.Hr(),
                dbc.Row(
                    [
                        
                        dbc.Col(dcc.Markdown('$r$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="nucleon-radius-input", type='number', style=style.DISPLAY_INPUT_BOX, readOnly=True), width=3),
                        dbc.Col(dcc.Markdown('$w$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="nucleon-width-input", type='number', min=0.05, max=1, value=0.25, step=0.05, style=style.STEP_INPUT_BOX), width=3),
                    ],
                ),
            ],style={"margin-bottom": '5%', "margin-top": "0%"}
        ),
        dbc.Row(
                    [

                        html.H6('show:'),
                        dbc.Col(
                        [

                            dcc.Checklist(
                                id="nucleon-checklist-1",
                                options=['Position', 'Density'],
                                value=['Position'],
                                style=style.CHECKLIST,
                                inputStyle=style.CHECKLIST_INPUT,
                            ),
                        ], width=6
                        ),
                        dbc.Col(
                            [
                                dcc.Checklist(
                                    id="nucleon-checklist-2",
                                    options=['Surface', 'Wireframe'],
                                    value=[],
                                    style=style.CHECKLIST,
                                    inputStyle=style.CHECKLIST_INPUT,
                                ),
                            ], width=6
                        ),
                    ],className="g-0", style={"margin-bottom": "3rem"}
                ),

        html.Div(
            [
                dbc.Row(
                    [
                        html.H5("Nucleus properties"),
                    ], style={"margin-bottom": '-1rem'},
                ),
                html.Hr(),
                dbc.Row(
                    [
                        
                        dbc.Col(dcc.Markdown('$r$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="radius-input-nucleon", type='number', style=style.DISPLAY_INPUT_BOX, readOnly=True), width=3),
                        dbc.Col(dcc.Markdown('$a_0$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="diffusion-input-nucleon", type='number', min=0.05, max=1, value=0.65, step=0.05, style=style.STEP_INPUT_BOX), width=3),
                    ],
                )
 
            ]
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown('&beta;$_2$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="beta2-input-nucleon", type='number', min=0, max=0.5, value=0.25, step=0.05, style=style.STEP_INPUT_BOX), width=3),
                        dbc.Col(dcc.Markdown('&beta;$_3$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="beta3-input-nucleon", type='number', min=0, max=0.1, value=0, step=0.05, style=style.STEP_INPUT_BOX), width=3),
                        dbc.Col(dcc.Markdown('&beta;$_4$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="beta4-input-nucleon", type='number', min=0, max=0.1, value=0, style=style.STEP_INPUT_BOX), width=3),

                    ],
                )
            ]
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown('&gamma;', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="gamma-input-nucleon", type='number', min=0, max=60, value=0, style=style.STEP_INPUT_BOX), width=3),

                    ], 
                )
            ]
        ),
        dbc.Row(
                    [
                        html.H6('show:'),
                        dbc.Col(
                            [
                                dcc.Checklist(
                                    id="nuclei-checklist-main",
                                    options=['Density', 'Surface'],
                                    value=[],
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
                                    value=[],
                                    style=style.CHECKLIST,
                                    inputStyle=style.CHECKLIST_INPUT,
                                ),
                            ],width=6
                        ),
                    ], className="pad-row", style={"margin-top": '1rem'}
                ),
    style_row
    ], 
    style={"background-color": "#f8f9fa", "padding-left": "1rem", "padding-right": "1rem", "padding-top": "1rem", "margin-right": "0%"}
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Row([
                    dbc.Col(dbc.Button('  Generate  ', outline=True, color="primary", id='generate-samples',size="sm", className="me-2", n_clicks=0), width=1)
                ]),
                dbc.Col(dcc.Graph(id='nucleon-plot', figure = scene.blank_fig()), width=10),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dcc.Graph(id='nucleon-projection-xy-plot', figure = scene.blank_fig()),
                                dcc.Graph(id='nucleon-projection-xz-plot', figure = scene.blank_fig()),
                                dcc.Graph(id='nucleon-projection-zy-plot', figure = scene.blank_fig()),
                            ]
                        )

                    ],width=2
                )
            ], style={"padding-left": "0rem", "padding-right": "0rem", "margin-top": "0rem", "margin-left": "-2rem"}

        )
    ],
    fluid=True,
    style={'margin-top': '0px'}
)



def add_callbacks(app):

    # Define callback to update the plot based on slider value
    @app.callback(
        Output('nucleon-plot', 'figure', allow_duplicate=True),
        Output('nucleon-projection-xy-plot', 'figure'),
        Output('nucleon-projection-xz-plot', 'figure'),
        Output('nucleon-projection-zy-plot', 'figure'),
        Output('radius-input-nucleon',          'value'),
        Output('nucleon-radius-input',          'value'),
    [
        Input('proton-input',       'value'),
        Input('neutron-input',      'value'),
        Input('generate-samples',   'n_clicks'),
        Input('nucleon-width-input',    'value'),
        Input('diffusion-input-nucleon', 'value'),
        Input('beta2-input-nucleon',    'value'),
        Input('gamma-input-nucleon',    'value'),
        Input('beta3-input-nucleon',    'value'),
        Input('beta4-input-nucleon',    'value'),
        Input('nuclei-checklist-main', 'value'),
        Input('nuclei-checklist-lines', 'value'),
        Input('nucleon-checklist-1',   'value'),
        Input('nucleon-checklist-2',   'value'),
        Input('scene-3d-checkboxes', 'value'),
        Input('scene-projection-checkboxes', 'value'),
        Input('surf-scheme', 'value'),
        Input('surf-scheme-invert', 'value'),
    ]
    )
    def update_nucleon_plot(nproton, nneutron, _, nucleon_width, diffusion, beta2, gamma, beta3, beta4, 
                nuclei_checklist_main, nuclei_checklist_lines, nucleon_checklist_1, nucleon_checklist_2, scene_3d_cbox, scene_projection_cbox, color_scale, invert_scale):

        nuclei_checklist    = np.concatenate([nuclei_checklist_main, nuclei_checklist_lines])
        nucleon_checklist   = np.concatenate([nucleon_checklist_1, nucleon_checklist_2])
        scene_checklist     = np.concatenate([scene_3d_cbox, scene_projection_cbox])


        # only do mc sampling after relevant update of params
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        active_triggers = ['nucleon-width-input', 'diffusion-input-nucleon', 'beta2-input-nucleon'
                           'gamma-input-nucleon', 'beta3-input-nucleon', 'beta4-input-nucleon',
                           'proton-input', 'neutron-input', 'generate-samples']


        global profile 

        if trigger_id in active_triggers or len(trigger_id) == 0:

            profile = NuclearProfile(element=nproton, mass_number=nproton+nneutron)
    
            profile.set_diffusion(diffusion)
            profile.set_beta2(beta2, gamma)
            profile.set_beta3(beta3)
            profile.set_beta4(beta4)

            profile.set_nucleon_width(width=nucleon_width)
            profile.generate_nucleons_by_sampling()


        Rx, Ry, Rz = profile.GetSurface()
        Wx, Wy, Wz = profile.GetWireFrame()
        px, py, pz = profile.GetPrincipalAxis()

        neutron_coordinates = [x.get_center_position() for x in profile.nucleons if x.pdg_code == '2112']
        xn = [coord[0] for coord in neutron_coordinates]
        yn = [coord[1] for coord in neutron_coordinates]
        zn = [coord[2] for coord in neutron_coordinates]

        proton_coordinates  = [x.get_center_position() for x in profile.nucleons if x.pdg_code == '2212']
        xp = [coord[0] for coord in proton_coordinates]
        yp = [coord[1] for coord in proton_coordinates]
        zp = [coord[2] for coord in proton_coordinates]


        fig = go.Figure(scene.init_figure)

        color_differential_surf  = ["Peach", "Blues"]
        color_differential_point = ["red", "blue"]



       

        if "Surface" in nucleon_checklist:
            resolution = 15                
            
            theta       = np.linspace(0, 2 * np.pi, resolution)
            phi         = np.linspace(0, np.pi, resolution)
            theta, phi  = np.meshgrid(theta, phi)
            
            radius=profile.nucleons[0].nucleon_radius

            for i in range(0, len(neutron_coordinates)):                
                xsurf = xn[i] + radius * np.sin(phi) * np.cos(theta)
                ysurf = yn[i] + radius * np.sin(phi) * np.sin(theta)
                zsurf = zn[i] + radius * np.cos(phi)

                # Create a 3D surface plot for the sphere
                fig.add_trace(go.Surface(
                    x=xsurf,
                    y=ysurf,
                    z=zsurf,
                    opacity=1.,
                    showscale=False,
                    showlegend=False,
                    colorscale=color_differential_surf[1]
                    )
                )
            for i in range(0, len(proton_coordinates)):                
                xsurf = xp[i] + radius * np.sin(phi) * np.cos(theta)
                ysurf = yp[i] + radius * np.sin(phi) * np.sin(theta)
                zsurf = zp[i] + radius * np.cos(phi)

                # Create a 3D surface plot for the sphere
                fig.add_trace(go.Surface(
                    x=xsurf,
                    y=ysurf,
                    z=zsurf,
                    opacity=1.,
                    showscale=False,
                    showlegend=False,
                    colorscale=color_differential_surf[0]
                    )
                )




        if "Density" in nucleon_checklist:
            for inucleon in profile.nucleons:
                fig.add_trace(go.Volume(
                    x=inucleon.density_grid["x"].flatten(),
                    y=inucleon.density_grid["y"].flatten(),
                    z=inucleon.density_grid["z"].flatten(),
                    value=inucleon.density_grid["rho"].flatten(),
                    isomin=0.05, 
                    isomax=1.,
                    opacity=0.25,
                    surface_count=10,
                    showscale=False,
                    colorscale=color_differential_surf[0] if inucleon.pdg_code == '2212' else color_differential_surf[1],
                    )
                )


        if "Position" in nucleon_checklist:
            fig.add_trace(go.Scatter3d(
                name='neutrons',
                x=xn,
                y=yn,
                z=zn,
                opacity=0.5,
                mode='markers',
                marker=dict(
                    size=5, 
                    color=color_differential_point[1],
                    sizemode='diameter'
                    ),
                showlegend=False,
                )
            )
            fig.add_trace(go.Scatter3d(
                name='protons',
                x=xp,
                y=yp,
                z=zp,
                opacity=0.5,
                mode='markers',
                marker=dict(
                    size=5, 
                    color=color_differential_point[0],
                    sizemode='diameter'
                    ),
                showlegend=False,
                )
            )
    
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
                    isomax=1., 
                    opacity=0.05, 
                    surface_count=10, 
                    showscale=True,
                    colorscale=color_scale,
                    reversescale=True if invert_scale else False,
                    colorbar=dict(title="", orientation="h", x=0.5, y=-0.15 )
                )
            )


        show_prin_axis = True if "Principal axis" in nuclei_checklist else False
        fig.add_trace(go.Scatter3d(
                name='axix',
                x=px, 
                y=py, 
                z=pz, 
                mode='lines',
                showlegend=False,
                line_width=5, 
                line_color=f'rgba(10,10,10, {int(show_prin_axis)})'
            )
        )

        show_axis = True if "Coordinate frame" in scene_checklist else False
        if show_axis:
            fig.update_layout(scene=scene.scene_on)
        else:
            fig.update_layout(scene=scene.scene_off)

        range_value = np.amax(profile.get_radius_params())
        fig.update_layout(
            scene_aspectmode='cube',
            scene=dict(
                    xaxis = dict(nticks=10, range=[-2*range_value,2*range_value]),
                    yaxis = dict(nticks=10, range=[-2*range_value,2*range_value]),
                    zaxis = dict(nticks=10, range=[-2*range_value,2*range_value]),
                ),
        )
        

        # Keep perspective to prevent resetting the camera angle
        global scene_camera
        if scene_camera:
            fig.update_layout(
                scene_camera_eye=scene_camera['eye'],
                scene_camera_center=scene_camera['center'],
                scene_camera_up=scene_camera['up']
            )


        subfig_xy = go.Figure(scene.init_subaspect)
        subfig_xz = go.Figure(scene.init_subaspect)
        subfig_zy = go.Figure(scene.init_subaspect)

        subfigs = [subfig_xy, subfig_xz, subfig_zy]

        projections = ["XY", "XZ", "YZ"]

        
        for idx, iprojection in enumerate(projections):
            subfigs[idx].add_annotation(
                text=f'{iprojection.lower()}-projection',
                xref="paper", yref="paper",
                x=0.05, y=0.975, showarrow=False,
                font_color='white',
                font_size=14
            )

        # make output variables
        nuclear_radius = round(profile.nuclear_radius, 2)
        nucleon_radius = round(profile.nucleons[0].nucleon_radius, 2)
        return fig, subfig_xy, subfig_xz, subfig_zy,  nuclear_radius, nucleon_radius

    
    
    @app.callback(
        Output('nucleon-plot', 'figure', allow_duplicate=True),
    [
        Input('nucleon-plot', 'figure')
    ],
        prevent_initial_call=True
    )
    def store_nucleon_camera(fig):
        # Store the initial camera parameters
        global scene_camera
        if 'scene' in fig['layout'] and 'camera' in fig['layout']['scene']:
            scene_camera['eye'] = fig['layout']['scene']['camera']['eye']
            scene_camera['center'] = fig['layout']['scene']['camera']['center']
            scene_camera['up'] = fig['layout']['scene']['camera']['up']    
        return fig
    
    
    return update_nucleon_plot, store_nucleon_camera

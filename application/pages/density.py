import sys
sys.path.append('../')

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
from utilities import method


from nuclear_profile import NuclearProfile
profile = NuclearProfile.empty()

scene_camera = scene.initial_camera.copy()


style_row = html.Div(
    [

                dbc.Row(
                    [
                        html.H5("Figure style"),
                    ], style={"margin-bottom": '-1rem', "margin-top": "10%"},
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
                        html.H5("Nucleus properties"),
                    ], style={"margin-bottom": '-1rem'},
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown('$r$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="radius-input", type='number', min=0, max=50, value=5, step=0.1, style=style.STEP_INPUT_BOX), width=3),
                        dbc.Col(dcc.Markdown('$a_0$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="diffusion-input", type='number', min=0.05, max=1, value=0.25, step=0.05, style=style.STEP_INPUT_BOX), width=3),
                    ],
                ),
            ]
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown('&beta;$_2$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="beta2-input", type='number', min=0, max=0.5, value=0.15, step=0.05, style=style.STEP_INPUT_BOX), width=3),
                        dbc.Col(dcc.Markdown('&beta;$_3$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="beta3-input", type='number', min=0, max=0.1, value=0, style=style.STEP_INPUT_BOX), width=3),
                        dbc.Col(dcc.Markdown('&beta;$_4$', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="beta4-input", type='number', min=0, max=0.1, value=0, style=style.STEP_INPUT_BOX), width=3),

                    ],
                )
            ]
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dcc.Markdown('&gamma;', mathjax=True, style=style.LATEX), width=1),
                        dbc.Col(dcc.Input(id="gamma-input", type='number', min=0, max=60, value=0, style=style.STEP_INPUT_BOX), width=3),

                    ], 
                )
            ]
        ),
        dcc.Markdown('Diffusion $a_0$', mathjax=True, style=style.LATEX),
                dbc.Row(
                    [
                        dbc.Col(dcc.Slider(
                                id='diffusion-slider',
                                min=0.05,
                                max=1,
                                step=0.05,
                                value=0.25,
                                marks={i: str(i) for i in range(1, 11)},
                            ), width=12),
                    ], style={'margin-left': '-2.5rem', 'margin-right': '-2rem', 'margin-bottom': '5%'}
                ),
        dbc.Row(
                    [
                        html.H6('show:'),
                        dbc.Col(
                            [
                                dcc.Checklist(
                                    id="nuclei-checklist-main",
                                    options=['Density', 'Surface'],
                                    value=['Density'],
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
    style={"background-color": "#f8f9fa", "padding-left": "1rem", "padding-right": "1rem", "padding-top": "1rem"}
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='density-plot', figure = scene.blank_fig()), width=10),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dcc.Graph(id='density-projection-xy-plot', figure = scene.blank_fig()),
                                dcc.Graph(id='density-projection-xz-plot', figure = scene.blank_fig()),
                                dcc.Graph(id='density-projection-zy-plot', figure = scene.blank_fig()),
                            ]
                        )

                    ],width=2
                )
            ]
        )
    ],
    fluid=True,
    style={'margin-top': '0px'}
)





def add_callbacks(app):

    # Define callback to update the plot based on slider value
    @app.callback(
        Output('density-plot', 'figure', allow_duplicate=True),
        Output('density-projection-xy-plot', 'figure'),
        Output('density-projection-xz-plot', 'figure'),
        Output('density-projection-zy-plot', 'figure'),
        Output('diffusion-input', 'value'),
        Output('diffusion-slider', 'value'),
    [
        Input('diffusion-input', 'value'),
        Input('diffusion-slider', 'value'),
        Input('radius-input',   'value'),
        Input('beta2-input',    'value'),
        Input('gamma-input',    'value'),
        Input('beta3-input',    'value'),
        Input('beta4-input',    'value'),
        Input('nuclei-checklist-main', 'value'),
        Input('nuclei-checklist-lines', 'value'),
        Input('scene-3d-checkboxes', 'value'),
        Input('scene-projection-checkboxes', 'value'),
        Input('surf-scheme', 'value'),
        Input('surf-scheme-invert', 'value'),
    ]
    )
    def update_density_plot(diffusion, diffusion_slider, radius, beta2, gamma, beta3, beta4, 
                nuclei_checklist_main, nuclei_checklist_lines, scene_3d_cbox, scene_projection_cbox, color_scale, invert_scale):

        # ciruclar feedback between 'slider' and 'input' --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if "diffusion" in trigger_id:
            diffusion_slider, diffusion = method.map_triger(trigger_id, diffusion_slider, diffusion)
        
        
        nuclei_checklist = np.concatenate([nuclei_checklist_main, nuclei_checklist_lines])
        scene_checklist = np.concatenate([scene_3d_cbox, scene_projection_cbox])

        global profile 
        profile = NuclearProfile.empty(radius=radius, diffusion = diffusion, beta2=beta2, gamma=gamma, beta3=beta3, beta4=beta4)
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
                #surfacecolor=Rx**2 + Ry**2 + Rz**2, 
                showscale=False, 
                showlegend=False,
                colorscale=['#f0f921','#f0f921'],
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
                    surface_count=25, 
                    showscale=True,
                    colorscale=color_scale,
                    reversescale=True if invert_scale else False,
                    colorbar=dict(title="", orientation="h", x=0.5, y=-0.15 )
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





        show_axis = True if "Coordinate frame" in scene_checklist else False
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


        #fig.update_layout(showlegend=False,
        #                  coloraxis=dict(colorbar=dict(orientation='h', y=-0.15)))     

        #fig.for_each_coloraxis(lambda x: x['colorbar'].update({'orientation':'h', 'thickness':20, 'y': -1.0}))   
        #if refresh_fig:
        #    scene_camera = scene.initial_camera.copy()
        #    fig.update_layout(
        #            scene_camera_eye=scene_camera['eye'],
        #            scene_camera_center=scene_camera['center'],
        #            scene_camera_up=scene_camera['up'],
        #            uirevision='constant'
        #        )



        subfig_xy = go.Figure(scene.init_subaspect)
        subfig_xz = go.Figure(scene.init_subaspect)
        subfig_zy = go.Figure(scene.init_subaspect)

        subfigs = [subfig_xy, subfig_xz, subfig_zy]

        projections = ["XY", "XZ", "YZ"]

        max_projection = 1
        for idx, iprojection in enumerate(projections):
            _, _, values = profile.GetProjection(iprojection) 
            if max_projection < np.amax(values):
                max_projection = np.amax(values)

        for idx, iprojection in enumerate(projections):
            xaxis, yaxis, values = profile.GetProjection(iprojection) 
            subfigs[idx].add_trace(go.Heatmap(x=xaxis, y=yaxis, z=values, 
                                            showscale=False, 
                                            connectgaps=True, 
                                            zsmooth='best',
                                            colorscale=color_scale,
                                            reversescale=True if invert_scale else False,
                                            zmin = 0,
                                            zmax = max_projection,
                        )
            )
            subfigs[idx].add_trace(go.Contour(x=xaxis, y=yaxis, z=values,
                                                contours_coloring='heatmap', 
                                                contours=dict(
                                                    coloring ='heatmap', 
                                                    showlabels=False), 
                                                showscale=False,
                                                zmin = 0,
                                                zmax = max_projection,
                                    )
            )

            subfigs[idx].add_annotation(
                text=f'{iprojection.lower()}-projection',
                xref="paper", yref="paper",
                x=0.05, y=0.975, showarrow=False,
                font_color='white',
                font_size=14
            )
        

        return fig, subfig_xy, subfig_xz, subfig_zy, diffusion, diffusion_slider
    
    
    @app.callback(
        Output('density-plot', 'figure', allow_duplicate=True),
    [
        Input('density-plot', 'figure')
    ],
    prevent_initial_call=True
    )
    def scenestore_density_camera(fig):
        # Store the initial camera parameters
        global scene_camera

        scene_camera['eye'] = fig['layout']['scene']['camera']['eye']
        scene_camera['center'] = fig['layout']['scene']['camera']['center']
        scene_camera['up'] = fig['layout']['scene']['camera']['up']    
        return fig
    
    
    return update_density_plot, scenestore_density_camera

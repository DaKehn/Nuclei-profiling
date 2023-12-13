import plotly.graph_objs as go


scene_off = dict(
    aspectmode='data',
    xaxis=dict(
        title='',
        showbackground=False,
        showticklabels=False
    ),
    yaxis=dict(
        title='',
        showbackground=False,
        showticklabels=False
    ),
    zaxis=dict(
        title='',
        showbackground=False,
        showticklabels=False
    )
)

scene_on = dict(
    aspectmode='data',
    xaxis=dict(
        title='X',
        showbackground=True,
        showticklabels=True
    ),
    yaxis=dict(
        title='Y',
        showbackground=True,
        showticklabels=True
    ),
    zaxis=dict(
        title='Z',
        showbackground=True,
        showticklabels=True
    )
)

initial_camera = dict(
    up=dict(x=0, y=0, z=1),
    center=dict(x=0, y=0, z=0),
    eye=dict(x=.95, y=.95, z=.85)
)


# Set layout
init_figure = go.Figure()
init_figure.update_layout(
    height=800,
    uirevision='constant',
    scene=scene_off,
    margin=dict(l=20, r=20, t=20, b=20),
)


# Set layout
init_subaspect = go.Figure()
init_subaspect.update_layout(
    height=300,
    width=300,
    uirevision='constant',
    margin=dict(l=20, r=20, t=20, b=20),
)


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig


def map_triger(trigger, slider, value):
    if 'input' in trigger:
        slider = value
    elif 'slider' in trigger:
        value = slider
    return slider, value


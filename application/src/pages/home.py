import sys
sys.path.append('../')

from dash import dcc, html, callback, dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from utilities import style


home_content = dbc.Container(
    [
        dbc.Row(
            [
            dbc.Col(
                [
                dbc.Row(
                [  
                    dcc.Markdown('''
                                ## Atomic structure
                                  
                                <p>  </p>

       
                                ### Shape engineering the atomic nuclei
                                
                                Most atomic nuclei exhibit some sort of intrinsic deformation due to the multipole moments of the nucleon distribution function. 
                                Consequently, the nuclear structure can be of very complex forms which are not easily modeled.
                                Though, experts in the field have come up with clever ways of modeling these structures in terms of the spherical harmonics, which often are known for their relation to the electron orbitals. 
                                These shape variations can be modeled by an equation for the radius $R(\\theta, \\varphi)$ that utilizes these spherical harmonics, where each corresponds to the magnitude of the multipole moment 
                                
                                $$
                                R'(\\theta, \\varphi)= R_0 (1 + \\beta_2 (\\cos(\\gamma) Y_2^0(\\theta) + \\frac{1}{\\sqrt{2}}\\sin(\\gamma) Y_2^2(\\theta, \\varphi)) + \\beta_3Y_3^0(\\theta, \\varphi) + \\beta_4Y_4^0(\\theta, \\varphi)) 
                                $$
                                
                                Here $R_0$ denotes the rms radius of the nuclei, $\\beta_n$ the n´th multipole moment of the nucleon distribution, $\\gamma$ the angular asymmetry, and $Y_{\\ell}^m(\\theta, \\varphi)$ denotes the spherical harmonics. 
                                For a perfect sphere $\\beta_2=\\beta_3=\\beta_4=0$, the resulting surface radius would be constant $R'(\\theta, \\varphi)= R_0$
                                
                                ### Moddeling the nucleon distribution 

                                The Wood-Saxon profile is a function commonly used to describe the nuclear density distribution of nucleons. 
                                It provides an approximate representation of how nucleons (protons and neutrons) are distributed within the nucleus. 
                                The Wood-Saxon profile can account for the effects of nuclear shape deformation on the nucleon density by using the equation for the deformed surface, as outlined above.

                                $$
                                \\rho (r, \\theta, \\varphi)=   \\rho_0 \\left[ 1 + \\exp\\left(\\frac{r-R'(\\theta, \\varphi)}{a_0}\\right) \\right]^{-1} 
                                $$
                        ''', 
                        mathjax=True, style=style.LATEX, dangerously_allow_html=True
                    )
                ], style={"margin-right": "1rem"}
            ),
                ], width=7,
            ),
            dbc.Col(
                [
                dbc.Row(
                    [
                        dbc.Card(dbc.CardBody(
                            [
                                dcc.Markdown(''' 
                                    ####  Disclaimer!
                                    If you decide to use or incorporate this framework into your projects, educational content or to produce figures,
                                    please provide appropriate attribution and citation to acknowledge the original author and source. https://github.com/DaKehn/Nuclei-profiling, Frederik S. K. Roemer.
                                ''',
                                mathjax=True,
                                )
                            ], 
                        ),style={"margin-bottom": "1rem"}),
                        html.Br(),
                        dbc.Card(
                        [
                            dbc.CardBody(
                            [
                                dcc.Markdown('''
                                        ### Usage
                                        This application are constructed with two core components, namely an _exploration_ and _simulation_ module.
                                        Each module consist of severeall  is constructed with severel induvidual modules, all optimized to focus on óne specific thing. 
                                        The application for each module are further divided into an  module that focus on educational understanding 
                                '''
                                ,),
                                dcc.Markdown('''
                                        #####  Exploration
                                        The exploration consist of a series of interactive 3D figures where parameters such as the deformation strengh and nuclear diffusion can be adjusted.
                                        Aditionnally the ordering of protons and neutrons can be genereted according the 3D Wood-Saxon density function. 
                                        *_The rendering time of figures in this module might cause some seconds delay when parameters are adjusted_
                                    ''',
                                    mathjax=True
                                ),
                                dbc.CardLink(html.H6("Surface"), href="surface"),
                                dcc.Markdown(''' 
                                        Explore how the surface of deformed nuclei are affected through different indivuidual multipole strenghs $\\beta_n$, and also in combination with each other
                                    ''',
                                    mathjax=True
                                ),
                                dbc.CardLink(html.H6("Density"), href="density"),
                                dcc.Markdown(''' 
                                        Explore the the density distrubtion of the nucleons and how the deformation can add new dimensions to high energy collisions
                                    ''',
                                    mathjax=True
                                ),
                                dbc.CardLink(html.H6("Nucleon"), href="nucleon"),
                                dcc.Markdown(''' 
                                        Explore the distribution of nucleons inside the nucleus, andontrole the nucleon _structure_ to see how it effects the nuclei. 
                                    ''',
                                    mathjax=True
                                ),
                                dcc.Markdown(''' 
                                        #####  Simulation
                                        *to be released*
                                    ''',
                                    mathjax=True
                                )
                            ],
                            )
                        ], style=style.CARD_USAGE, color="primary", outline=True),
                    ], className="pad-row"
                ), ],width=5
            )
            ], 
        )
    ],
    fluid=True
)


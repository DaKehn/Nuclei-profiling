# Nuclei-profiling
This framework provides a representation for atomic nuclei and facilitates the study of their physics. The project has _two_ main ideas which is to...

* Provide a convenient and intuitive graphical representation of the nuclear structure.
* Simplistic experiments of the initial interaction between nuclei in high energy collision (in the works). 


## Interactive dashboard application

One of the key functionalities is the ability to generate graphical representations of nucleon density distributions thorugh an interactive dashboard. This allows users to gain insights into the spatial distribution of nucleons within the nucleus witout having to poses any programming skills. The dashboard consist of numerus 'live' plotting pages, where different attributes and physics are highlighted. Each page can be used indenpendely to explore concepts, create figures or even as part of educational content.

Run online: [https://nuclei-profiling.onrender.com](https://nuclei-profiling.onrender.com)
Run local: launch application/src/app.py   

### Features

* Create and illustrate atomic nuclei with intrinsic deformation through a live dashboard
* Create density renderings of the nuclei based on the deformed Wood-Saxon profile
* Rotate the nuclei in three dimensions
* Create projection of the nuclei in the transverse plane

Additional features and capabilities might be added in the future, enhancing its functionality and providing users with even more tools for nuclear structure analysis.


### Requirements

* Python (version 3.11.3), only version tested 
* Required dependencies: Plotly, numpy

*note:* dashboard application requires the additional dependecies: plotly, dash, dash_bootstrap_components

## Disclaimer

If you decide to use or incorporate this framework into your projects, please provide appropriate attribution and citation to acknowledge the original author and source. https://github.com/DaKehn/Nuclei-profiling, Frederik K. Roemer.

The code provided is intended for informational and educational purposes only. It is distributed "as is," without any warranties or guarantees of any kind, express or implied. The author and distributor of this code shall not be held liable for any damages or losses arising from its use.

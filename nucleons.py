import numpy as np

class Nucleon:

    def __init__(self, x, y, z, width=0.5, pdg = None):
        self.pdg_code = pdg

        self.nucleon_width  = width
        self.nucleon_radius     = 3**(1./2.) * width
        self.nucleon_free_path  = 2*self.nucleon_radius

        self.space_resolution   = 25
        self.center_position = {
            "x": x,
            "y": y,
            "z": z
        }
        
        xgrid, ygrid, zgrid, val = self.pdf_gaussian()
        self.density_grid = {
            "x": xgrid,
            "y": ygrid,
            "z": zgrid,
            "rho": val
        }

    def pdf_gaussian(self):
        """
        Generate 3D grid for the 'volume' grid and return 3D arrays.

        Returns:
            x (ndarray): 3D array representing the x-coordinates of the grid.
            y (ndarray): 3D array representing the y-coordinates of the grid.
            z (ndarray): 3D array representing the z-coordinates of the grid.
            gaussian (ndarray): 3D array representing the Gaussian values of the grid.
        """
        x = np.linspace(self.center_position["x"] - 2*self.nucleon_radius, self.center_position["x"] + 2*self.nucleon_radius, self.space_resolution)
        y = np.linspace(self.center_position["y"] - 2*self.nucleon_radius, self.center_position["y"] + 2*self.nucleon_radius, self.space_resolution)
        z = np.linspace(self.center_position["z"] - 2*self.nucleon_radius, self.center_position["z"] + 2*self.nucleon_radius, self.space_resolution)
        x, y, z = np.meshgrid(x, y, z)

        distance = np.sqrt((x - self.center_position["x"])**2 + (y - self.center_position["y"])**2 + (z - self.center_position["z"])**2)
        gaussian = np.exp(-0.5 * (distance / self.nucleon_width)**2)

        return x, y, z, gaussian

    def set_width(self, width):
        self.nucleon_width = width
    
    def set_radius(self, radius):
        self.nucleon_radius = radius
    
    def get_center_position(self):
        return [
            self.center_position["x"],
            self.center_position["y"],
            self.center_position["z"]
        ]

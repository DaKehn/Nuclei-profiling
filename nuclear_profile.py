import SpHarmonics as y_lm
import Coordinates as coord_space
import numpy as np

    
class ReferenceGrid:
    rho        = None
    Xx, Yy, Zz = None, None, None
    Rx, Ry, Rz = None, None, None
    Wx, Wy, Wz = [], [], []
    Xpa, Ypa, Zpa = None, None, None

    
    def __init__(self, resulution, low, high):
        self.grid_resolution    = 50j
        self.low                = low
        self.high               = high

    def SetPrincipalAxis(self, lenght):
        """ Principal axis for 3D object, denoted along z-axis"""
        self.Xpa = np.linspace(0,0,100) 
        self.Ypa = np.linspace(0,0,100)
        self.Zpa = np.linspace(-lenght, lenght, 100)

    def SetDensityGrid(self, Func):
        """ Main grid space for 3D object"""
        self.Xx, self.Yy, self.Zz = np.mgrid[self.low:self.high:self.grid_resolution,
                                self.low:self.high:self.grid_resolution,
                                self.low:self.high:self.grid_resolution]
        self.rho = Func(self.Xx, self.Yy, self.Zz)
        return

    def SetWireFrame(self, SphFunc, nmeridlines=12, nparlines=12):
        """ Helper function to set meridian and parrallel lines of spherical object """
        theta = np.linspace(0, np.pi, 120)
        phi = np.linspace(0, 2*np.pi, 120)
        self.Wx, self.Wy, self.Wz = np.empty( shape=(1, 0) ), np.empty( shape=(1, 0) ), np.empty( shape=(1, 0) )
        for dtheta in [theta[10*k] for k in range(nmeridlines)]:              
            self.Wx = np.append( self.Wx, SphFunc(dtheta,phi)*np.sin(dtheta)*np.cos(phi))      
            self.Wy = np.append( self.Wy, SphFunc(dtheta,phi)*np.sin(dtheta)*np.sin(phi))
            self.Wz = np.append( self.Wz, SphFunc(dtheta,phi)*np.cos(dtheta))
        for dphi in [phi[10*k] for k in range(nparlines)]:             
            self.Wx = np.append( self.Wx, SphFunc(theta,dphi)*np.sin(theta)*np.cos(dphi))      
            self.Wy = np.append( self.Wy, SphFunc(theta,dphi)*np.sin(theta)*np.sin(dphi))
            self.Wz = np.append( self.Wz, SphFunc(theta,dphi)*np.cos(theta))
        return
    
    def SetSurface(self, SphFunc):
        """ Helper function to set surface of spherical object"""
        theta, phi = np.mgrid[0:np.pi:self.grid_resolution*4, 0:2*np.pi:self.grid_resolution*4]
        xyz = np.array([np.sin(theta) * np.cos(phi),
                        np.sin(theta) * np.sin(phi),
                        np.cos(theta)])
        self.Rx, self.Ry, self.Rz = SphFunc(theta,phi)*xyz
        return

    def GetDensityGrid(self):
        """ Return density grid for object """
        return self.Xx, self.Yy, self.Zz, self.rho
    
    def GetSurface(self):
        """ Return surface grid for object """
        return self.Rx, self.Ry, self.Rz
        
    def GetWireFrame(self):
        """ Return wireframe for object """
        return self.Wx, self.Wy, self.Wz

    def GetPrincipalAxis(self):
        """ Return principal axis for object """
        return self.Xpa, self.Ypa, self.Zpa
    
class NuclearProfile(ReferenceGrid):
    rho = None

    def __init__(self, R0, a0, beta2=0, gamma=0, beta3=0, beta4=0):
        ReferenceGrid.__init__(self, 40j, -2, 2)
        self.R0 = R0
        self.a0 = a0
        self.beta2 = beta2
        self.gamma = gamma*(1./180*np.pi)
        self.beta3 = beta3
        self.beta4 = beta4
        self.reset_nuclei()

    def reset_nuclei(self):
        """ Reinitialize all objects (wireframe, surface etc..)"""
        self.SetPrincipalAxis(self.R0*1.5)
        self.SetSurface(self.Rp)
        self.SetWireFrame(self.Rp)
        self.SetDensityGrid(self.WSDeformDensity)
    
    def set_beta2(self, beta, gamma = 0):
        """ Set quadrupole deformation beta2 """
        self.beta2 = beta
        self.gamma = gamma*(1./180*np.pi)
        self.reset_nuclei()
    
    def set_beta3(self, beta):
        """ Set octupole deformation beta3 """
        self.beta3 = beta
        self.reset_nuclei()
    
    def set_beta4(self, beta):
        """ Set hexadecapole deformation beta4 """
        self.beta4 = beta
        self.reset_nuclei()

    def set_beta(self, beta2,  beta3, beta4):
        """ Set hexadecapole deformation beta4 """
        self.beta2, self.beta3, self.beta4 = beta2, beta3, beta4
        self.reset_nuclei()

    def Rp(self, theta, phi):
        """Calculate the radius based on the Wood-Saxon profile for deformed nuclei"""
        RPrime = self.R0 * (1.
                           + self.beta2 * (np.cos(self.gamma) * y_lm.Y20(theta)
                                           + 1. / np.sqrt(2) * np.sin(self.gamma) * y_lm.Y22(theta, phi))
                           + self.beta3 * y_lm.Y30(theta)
                           + self.beta4 * y_lm.Y40(theta))
        return RPrime

    def WSDeformDensity(self, x, y, z):
        """ Calculate the density based on the Wood-Saxon profile for deformed nuclei """
        r, phi, theta = coord_space.cart2sph(x, y, z)
        density = 1 + np.exp((r - self.Rp(theta, phi)) / self.a0)
        return 1. / density


    def GetProjection(self, plane="XY"):
        """ Rotates the nucleus in x -> y -> z by Euler angles """ 
        if "X" in plane and "Y" in plane: return self.Xx[:, 0, 0], self.Yy[0, :, 0], np.sum(self.rho, axis=2)
        if "X" in plane and "Z" in plane: return self.Xx[:, 0, 0], self.Zz[0, 0, :], np.sum(self.rho, axis=1)
        if "Y" in plane and "Z" in plane: return self.Yy[0, :, 0], self.Zz[0, 0, :], np.sum(self.rho, axis=0)

    def Rotate(self, alpha=0, beta=0, gamma=0):
        """ Rotates the nucleus in x -> y -> z by Euler angles (note density grid does not rotate properly for more then one rotation)""" 
        x_rot, y_rot, z_rot = coord_space.EulerXYZ([self.Xx, self.Yy, self.Zz], alpha, beta, gamma)
        self.rho = self.WSDeformDensity(x_rot, y_rot, z_rot)
        
        self.Xpa, self.Ypa, self.Zpa = coord_space.EulerXYZ([self.Xpa, self.Ypa, self.Zpa], alpha, beta, gamma)
        self.Rx, self.Ry, self.Rz = coord_space.EulerXYZ([self.Rx, self.Ry, self.Rz], alpha, beta, gamma)
        self.Wx, self.Wy, self.Wz = coord_space.EulerXYZ([self.Wx, self.Wy, self.Wz], alpha, beta, gamma)
        return


  

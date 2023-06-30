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
        self.grid_resolution    = resulution
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
    NUCLEAR_RADIUS_PARAMETER = 1.2*1e-15

    nuclear_radius      = None      # R0 
    nuclear_diffusion   = None      # a0
    nuclear_density     = None      # rho
    rho = None

    beta2 = 0
    gamma = 0
    beta3 = 0
    beta4 = 0

    mass_number = None
    atomic_number = None
    neutrons = None
    protons = None

    #, R0, a0, beta2=0, gamma=0, beta3=0, beta4=0
    def __init__(self, element=0, mass_number=0):
        ReferenceGrid.__init__(self, 30j, -2, 2)

        if isinstance(element, str):
            if self.get_z_from_name(element) is None:
                print(f'Elements not found in table')
                return
            self.atomic_number = self.get_z_from_name(element)
        elif isinstance(element, int):
            self.atomic_number = element

        self.mass_number        = mass_number
        self.nuclear_radius     = self.get_radius_from_mass_number(mass_number)
        self.nuclear_diffusion  = 0.5    # no particular motivation for default value
        self.reset_nuclei()

    @classmethod
    def empty(cls, radius = 1, nucleon_density=1., diffusion=0.15, beta2=0, gamma=0, beta3=0, beta4=0):
        """ create empty nucleus object"""
        new_instance = cls()
        new_instance.nuclear_radius     = radius
        new_instance.nuclear_density    = nucleon_density
        new_instance.nuclear_diffusion  = diffusion
        new_instance.set_beta2(beta2, gamma)
        new_instance.set_beta3(beta3)
        new_instance.set_beta4(beta4)
        new_instance.reset_nuclei()
        return new_instance

    def reset_nuclei(self):
        """ Reinitialize all objects (wireframe, surface etc..)"""
        self.SetPrincipalAxis(self.nuclear_radius)
        self.SetSurface(self.prime_radius)
        self.SetWireFrame(self.prime_radius)
        self.SetDensityGrid(self.density_wood_saxon)
    
    def set_diffusion(self, diffusion):
        self.nuclear_diffusion = diffusion
        self.reset_nuclei()

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

    def set_mulitpole_strenght(self, n, strenght):
        """ Set deformation strenght for multipole moment of n'th order"""
        if   n == 2: self.set_beta2(self, strenght)
        elif n == 3: self.set_beta3(self, strenght)
        elif n == 4: self.set_beta4(self, strenght)
        else: print("Multipole moment {n} not defined")
        self.reset_nuclei()

    def prime_radius(self, theta, phi):
        """Calculate the surface radius of the nucleus"""
        prime = 1
        if self.beta2 is not None: 
            prime += self.beta2 * (np.cos(self.gamma) * y_lm.Y20(theta) + 1. / np.sqrt(2) * np.sin(self.gamma) * y_lm.Y22(theta, phi))
        if self.beta3 is not None: 
            prime += self.beta3 * y_lm.Y30(theta)
        if self.beta4 is not None: 
            prime += self.beta4 * y_lm.Y40(theta)
        return prime*self.nuclear_radius

    def density_wood_saxon(self, x, y, z):
        """ Calculate the density based on the Wood-Saxon profile for deformed nuclei """
        r, phi, theta = coord_space.cart2sph(x, y, z)
        density = 1 + np.exp((r - self.prime_radius(theta, phi)) / self.nuclear_diffusion)
        return 1. / density

    def density_solid_sphere(self, x, y, z):
        r, phi, theta = coord_space.cart2sph(x, y, z)
        density = 1 * (r<self.prime_radius(theta, phi))
        return density

    def GetProjection(self, plane="ij"):
        """ Return projection in specified ij-plane """ 
        if "X" in plane and "Y" in plane: return self.Xx[:, 0, 0], self.Yy[0, :, 0], np.sum(self.rho, axis=2)
        if "X" in plane and "Z" in plane: return self.Xx[:, 0, 0], self.Zz[0, 0, :], np.sum(self.rho, axis=1)
        if "Y" in plane and "Z" in plane: return self.Yy[0, :, 0], self.Zz[0, 0, :], np.sum(self.rho, axis=0)

    def Rotate(self, alpha=0, beta=0, gamma=0):
        """ Rotates the nucleus in x -> y -> z by Euler angles (note density grid does not rotate properly for more then one rotation)""" 
        x_rot, y_rot, z_rot = coord_space.EulerXYZ([self.Xx, self.Yy, self.Zz], alpha, beta, gamma)
        self.rho = self.density_wood_saxon(x_rot, y_rot, z_rot)
        
        self.Xpa, self.Ypa, self.Zpa = coord_space.EulerXYZ([self.Xpa, self.Ypa, self.Zpa], alpha, beta, gamma)
        self.Rx, self.Ry, self.Rz = coord_space.EulerXYZ([self.Rx, self.Ry, self.Rz], alpha, beta, gamma)
        self.Wx, self.Wy, self.Wz = coord_space.EulerXYZ([self.Wx, self.Wy, self.Wz], alpha, beta, gamma)
        return

    def info(self):
        print(f'Mass number   \t {self.mass_number}     ')
        print(f'Atomic number \t {self.atomic_number}   ')

    @classmethod
    def get_radius_from_mass_number(cls, mass_number):
        return NuclearProfile.NUCLEAR_RADIUS_PARAMETER * pow(mass_number, 1/3.)

    @classmethod
    def get_z_from_name(cls, element):
        """Find atomic number from element name"""
        match element.lower():
            case 'h'    | 'hydrogen':       return 1
            case 'he'   | 'helium':         return 2
            case 'li'   | 'lithium':        return 3
            case 'be'   | 'beryllium':      return 4
            case 'b'    | 'boron':          return 5
            case 'c'    | 'carbon':         return 6
            case 'n'    | 'nitrogen':       return 7
            case 'o'    | 'oxygen':         return 8
            case 'f'    | 'fluorine':       return 9
            case 'ne'   | 'neon':           return 10
            case 'na'   | 'sodium':         return 11
            case 'mg'   | 'magnesium':      return 12
            case 'al'   | 'aluminum':       return 13
            case 'si'   | 'silicon':        return 14
            case 'p'    | 'phosphorus':     return 15
            case 's'    | 'sulfur':         return 16
            case 'cl'   | 'chlorine':       return 17
            case 'ar'   | 'argon':          return 18
            case 'k'    | 'potassium':      return 19
            case 'ca'   | 'calcium':        return 20
            case 'sc'   | 'scandium':       return 21
            case 'ti'   | 'titanium':       return 22
            case 'v'    | 'vanadium':       return 23
            case 'cr'   | 'chromium':       return 24
            case 'mn'   | 'manganese':      return 25
            case 'fe'   | 'iron':           return 26
            case 'ni'   | 'nickel':         return 27
            case 'co'   | 'cobalt':         return 28
            case 'cu'   | 'copper':         return 29
            case 'zn'   | 'zinc':           return 30
            case 'ga'   | 'gallium':        return 31
            case 'ge'   | 'germanium':      return 32
            case 'as'   | 'arsenic':        return 33
            case 'se'   | 'selenium':       return 34
            case 'br'   | 'bromine':        return 35
            case 'kr'   | 'krypton':        return 36
            case 'rb'   | 'rubidium':       return 37
            case 'sr'   | 'strontium':      return 38
            case 'y'    | 'yttrium':        return 39
            case 'zr'   | 'zirconium':      return 40
            case 'nb'   | 'niobium':        return 41
            case 'mo'   | 'molybdenum':     return 42
            case 'tc'   | 'technetium':     return 43
            case 'ru'   | 'ruthenium':      return 44
            case 'rh'   | 'rhodium':        return 45
            case 'pd'   | 'palladium':      return 46
            case 'ag'   | 'silver':         return 47
            case 'cd'   | 'cadmium':        return 48
            case 'in'   | 'indium':         return 49
            case 'sn'   | 'tin':            return 50
            case 'sb'   | 'antimony':       return 51
            case 'i'    | 'iodine':         return 53
            case 'te'   | 'tellurium':      return 52
            case 'xe'   | 'xenon':          return 54
            case 'cs'   | 'cesium':         return 55
            case 'ba'   | 'barium':         return 56
            case 'la'   | 'lanthanum':      return 57
            case 'ce'   | 'cerium':         return 58
            case 'pr'   | 'praseodymium':   return 59
            case 'nd'   | 'neodymium':      return 60
            case 'pm'   | 'promethium':     return 61
            case 'sm'   | 'samarium':       return 62
            case 'eu'   | 'europium':       return 63
            case 'gd'   | 'gadolinium':     return 64
            case 'tb'   | 'terbium':        return 65
            case 'dy'   | 'dysprosium':     return 66
            case 'ho'   | 'holmium':        return 67
            case 'er'   | 'erbium':         return 68
            case 'tm'   | 'thulium':        return 69
            case 'yb'   | 'ytterbium':      return 70
            case 'lu'   | 'lutetium':       return 71
            case 'hf'   | 'hafnium':        return 72
            case 'ta'   | 'tantalum':       return 73
            case 'w'    | 'tungsten':       return 74
            case 're'   | 'rhenium':        return 75
            case 'os'   | 'osmium':         return 76
            case 'ir'   | 'iridium':        return 77
            case 'pt'   | 'platinum':       return 78
            case 'au'   | 'gold':           return 79
            case 'hg'   | 'mercury':        return 80
            case 'tl'   | 'thallium':       return 81
            case 'pb'   | 'lead':           return 82
            case 'bi'   | 'bismuth':        return 83
            case 'po'   | 'polonium':       return 84
            case 'at'   | 'astatine':       return 85
            case 'rn'   | 'radon':          return 86
            case 'fr'   | 'francium':       return 87
            case 'ra'   | 'radium':         return 88
            case 'ac'   | 'actinium':       return 89
            case 'th'   | 'thorium':        return 90
            case 'pa'   | 'protactinium':   return 91
            case 'u'    | 'uranium':        return 92
            case 'np'   | 'neptunium':      return 93
            case 'pu'   | 'plutonium':      return 94
            case 'am'   | 'americium':      return 95
            case 'cm'   | 'curium':         return 96
            case 'bk'   | 'berkelium':      return 97
            case 'cf'   | 'californium':    return 98
            case 'es'   | 'einsteinium':    return 99
            case 'fm'   | 'fermium':        return 100
            case 'md'   | 'mendelevium':    return 101
            case 'no'   | 'nobelium':       return 102
            case 'lr'   | 'lawrencium':     return 103
            case 'rf'   | 'rutherfordium':  return 104
            case 'db'   | 'dubnium':        return 105
            case 'sg'   | 'seaborgium':     return 106
            case 'bh'   | 'bohrium':        return 107
            case 'hs'   | 'hassium':        return 108
            case 'mt'   | 'meitnerium':     return 109
            case 'ds'   | 'darmstadtium':   return 110
            case 'rg'   | 'roentgenium':    return 111
            case 'cn'   | 'copernicium':    return 112
            case 'nh'   | 'nihonium':       return 113
            case 'fl'   | 'flerovium':      return 114
            case 'mc'   | 'moscovium':      return 115
            case 'lv'   | 'livermorium':    return 116
            case 'ts'   | 'tennessine':     return 117
            case 'og'   | 'oganesson':      return 118
            case _: 
                print(f'could not find element {element} in table')
                return None
            

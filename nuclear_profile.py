import SpHarmonics as y_lm
import Coordinates as coord_space
import numpy as np

from nucleons import Nucleon
    
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

    def SetGridRange(self, low, high):
        self.low = low
        self.high = high

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
    """
    A class representing a nuclear profile.

    This class inherits from the `ReferenceGrid` class and provides methods to generate and manipulate the 'profile' of atomic nuclei.

    Attributes:
        NUCLEAR_PREFIX (float): A constant representing prefix (for scale).
        NUCLEAR_RADIUS_PARAMETER (float): A constant representing the nuclear radius parameter.
        nuclear_radius (float): The radius of the nucleus.
        nuclear_diffusion (float): The diffusion parameter for the nuclear profile.
        nuclear_density (float): The density of the nucleus.
        rho (float): The density grid for the nucleus.
        beta2 (float): The quadrupole deformation beta2.
        gamma (float): The gamma angle for the quadrupole deformation.
        beta3 (float): The octupole deformation beta3.
        beta4 (float): The hexadecapole deformation beta4.
        nucleon_width (float): The width of the nucleons.
        nucleons (list): A list of `Nucleon` objects representing the nucleons in the nucleus.
        atomic_number (int): The atomic number of the element.
        mass_number (int): The mass number of the nucleus.
    """
    NUCLEAR_PREFIX           = 1e-15
    NUCLEAR_RADIUS_PARAMETER = 1.2

    nuclear_radius      = None      # R0 
    nuclear_diffusion   = None      # a0
    nuclear_density     = None      # rho
    rho = None

    beta2 = 0
    gamma = 0
    beta3 = 0
    beta4 = 0

    nucleon_width = 0.5

    nucleons = []

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

        self.mass_number    = mass_number
        self.atomic_number  = element
        
        self.nuclear_radius     = self.get_radius_from_mass_number(mass_number)
        self.nuclear_diffusion  = 0.65    # no particular motivation for default value
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
        self.SetSurface(self.prime_radius)
        self.SetWireFrame(self.prime_radius)
        
        # calculate the maximum radius
        max_radius = np.amax(self.get_radius_params())
        if not max_radius:
            max_radius = 1.
        
        # calculate mgrid scale
        grid_scale = max_radius * (1 + self.nuclear_diffusion)

        # set the grid range
        self.SetGridRange(-grid_scale, grid_scale)

        # set the density grid
        self.SetDensityGrid(self.density_wood_saxon)

        # set the principal axis
        self.SetPrincipalAxis(max_radius * 1.25)
    
    def set_diffusion(self, diffusion):
        """
        Set the diffusion parameter for the nuclear profile.

        Args:
            diffusion (float): The diffusion parameter for the nuclear profile.

        Returns:
            None
        """
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
        """
        Set the deformation strength for the multipole moment of the n-th order.

        Args:
            n (int): The order of the multipole moment.
            strenght (float): The deformation strength.

        Returns:
            None
        """
        if   n == 2: self.set_beta2(self, strenght)
        elif n == 3: self.set_beta3(self, strenght)
        elif n == 4: self.set_beta4(self, strenght)
        else: print("Multipole moment {n} not defined")
        self.reset_nuclei()

    def set_nucleon_width(self, width):
        """ Set the width of the nucleons."""
        self.nucleon_width = width

    def prime_radius(self, theta, phi):
        """Calculate the surface radius of the nucleus
        Args:
            theta (float): The polar angle in spherical coordinates.
            phi (float): The azimuthal angle in spherical coordinates.

        Returns:
            float: The surface radius of the nucleus.
        """
        prime = 1
        if self.beta2 is not None: 
            prime += self.beta2 * (np.cos(self.gamma) * y_lm.Y20(theta) + 1. / np.sqrt(2) * np.sin(self.gamma) * y_lm.Y22(theta, phi))
        if self.beta3 is not None: 
            prime += self.beta3 * y_lm.Y30(theta)
        if self.beta4 is not None: 
            prime += self.beta4 * y_lm.Y40(theta)
        return prime*self.nuclear_radius

    def density_wood_saxon(self, x, y, z):
        """
        Calculate the density based on the Wood-Saxon profile for deformed nuclei.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            z (float): The z-coordinate.

        Returns:
            float: The calculated density.
        """
        r, phi, theta = coord_space.cart2sph(x, y, z)
        density = 1 + np.exp((r - self.prime_radius(theta, phi)) / self.nuclear_diffusion)
        return 1. / density


    def inverse_cdf_deformed_woods_saxon(self, u, theta, phi):
        """
        Calculate the value of the inverse cumulative distribution function (CDF) for the deformed Woods-Saxon distribution.

        Args:
            u (float): The input value for the CDF.
            theta (float): The polar angle in spherical coordinates.
            phi (float): The azimuthal angle in spherical coordinates.

        Returns:
            float: The inverse CDF value.
        """
        inverse_cdf_values = self.nuclear_radius * np.log((1/u) - 1) * self.nuclear_diffusion / self.prime_radius(theta, phi)
        return inverse_cdf_values

    def generate_nucleons_by_sampling(self):
        """
        Generate nucleons based on the Inverse Transform Method.

        Returns:
            None
        """
        if self.nucleons: self.nucleons.clear()

        # generate number of protons and neutrons
        nucleon_list = np.concatenate([
            np.full(self.get_proton_number(), '2212'),
            np.full(self.get_neutron_number(),'2112')
        ])
        np.random.shuffle(nucleon_list)


        itry = 0
        while len(self.nucleons) < self.mass_number:
            # start from first nucelon in list
            next_pdg_code = nucleon_list[len(self.nucleons)]

            theta   = np.random.uniform(0, np.pi, 1)
            phi     = np.random.uniform(0, 2 * np.pi, 1)
            u       = np.random.uniform(0, 1, 1)
            r       = self.inverse_cdf_deformed_woods_saxon(u, theta, phi)

            ix, iy, iz = coord_space.sph2cart(r, theta, phi)
            if not self.nucleons:
                self.nucleons.append(
                    Nucleon( ix[0], iy[0], iz[0], width=self.nucleon_width, pdg=next_pdg_code)
                )
                continue

            # Assume no overlap -> if overlap break and try again
            overlap = False
            for inucleon in self.nucleons:
                dist = np.sqrt((inucleon.center_position["x"] - ix)**2 + (inucleon.center_position["y"] - iy)**2 + (inucleon.center_position["z"] - iz)**2)
                if dist < inucleon.nucleon_free_path:
                    overlap = True
                    break

            if not overlap:
                self.nucleons.append(
                    Nucleon(ix[0], iy[0], iz[0], width=self.nucleon_width, pdg=next_pdg_code)
                )
            itry += 1
            if itry > 1e6:
                raise Exception("Maximum number of iterations reached without generating the desired number of nucleons.")
        
        if len(self.nucleons) != self.mass_number:
            raise Exception("Number of generated nucleons does not match the desired mass number.")
        
        return
    
    def generate_nucleons_by_list(self, x, y, z):
        """
        Generate nucleons based on input coordinates ([x1,x2...] ,[y1,y2...], [z1,z2...]).

        Args:
            x (list): A list of x-coordinates.
            y (list): A list of y-coordinates.
            z (list): A list of z-coordinates.

        Returns:
            None
        """
        if not all( len(lst) != self.mass_number for lst in [x, y, z]):
            raise Exception(f'Mass number and lenght of arrays does not match. Expected {self.mass_number}, but got size: x({len(x)}), x({len(y)}), x({len(z)})')

        if self.nucleons: self.nucleons.clear()
        for i in range(len(x)):
            self.nucleons.append(
                Nucleon( x[i], y[i], z[i])
            )
        return

    
    def get_nucleon_coordinates(self):
        """
        Retrieves the coordinates of each nucleon stored in the nucleons list.

        Returns:
            list: A list of tuples representing the coordinates of nucleons in the form (x, y, z).
        """
        coordinates = []
        for nucleon in self.nucleons:
            coordinates.append(
                nucleon.get_center_position()
            )
        return coordinates


    def density_solid_sphere(self, x, y, z):
        """
        Calculate the density based on a solid sphere profile.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            z (float): The z-coordinate.

        Returns:
            float: The density at the given coordinates.
        """
        r, phi, theta = coord_space.cart2sph(x, y, z)
        density = 1 * (r<self.prime_radius(theta, phi))
        return density

    def GetProjection(self, plane="xy"):
        """
        Return projection in the specified ij-plane.

        Args:
            plane (str): The plane in which the projection is desired. 
                        It should be a combination of 'x', 'y', and 'z' characters.

        Returns:
            tuple: A tuple containing the ij-coordinates, and the summed density along the plane.
        """
        plane = plane.lower()
        if "x" in plane and "y" in plane: 
            return self.Xx[:, 0, 0], self.Yy[0, :, 0], np.sum(self.rho, axis=2)
        elif "x" in plane and "z" in plane: 
            return self.Xx[:, 0, 0], self.Zz[0, 0, :], np.sum(self.rho, axis=1)
        elif "y" in plane and "z" in plane: 
            return self.Yy[0, :, 0], self.Zz[0, 0, :], np.sum(self.rho, axis=0)
        else:
            raise Exception(f'Uknown projection {plane}!')


    def rotate(self, alpha=0, beta=0, gamma=0):
        """
        Rotates the nucleus in x(alpha) -> y(beta) -> z(gamma) by Euler angles.

        Args:
            alpha (float): The rotation angle around the x-axis in radians.
            beta (float): The rotation angle around the y-axis in radians.
            gamma (float): The rotation angle around the z-axis in radians.

        Returns:
            None
        """ 
        x_rot, y_rot, z_rot = coord_space.EulerXYZ([self.Xx, self.Yy, self.Zz], alpha, beta, gamma)
        self.rho = self.density_wood_saxon(x_rot, y_rot, z_rot)
        
        self.Xpa, self.Ypa, self.Zpa = coord_space.EulerXYZ([self.Xpa, self.Ypa, self.Zpa], alpha, beta, gamma)
        self.Rx, self.Ry, self.Rz = coord_space.EulerXYZ([self.Rx, self.Ry, self.Rz], alpha, beta, gamma)
        self.Wx, self.Wy, self.Wz = coord_space.EulerXYZ([self.Wx, self.Wy, self.Wz], alpha, beta, gamma)
        return

    def get_radius_params(self):
        """
        Calculate the limits of the radius if nucleus is deformed.

        Returns:
            list: A list containing the maximum and minimum radius.
        """
        limits = [
            np.amax(np.sqrt(self.Rx**2 + self.Ry**2 + self.Rz**2)),
            np.amin(np.sqrt(self.Rx**2 + self.Ry**2 + self.Rz**2))
        ] 
        return limits

    def get_neutrons(self):
        """
        Retrieves the neutrons from the list of nucleons.

        Returns:
            list: A list of `Nucleon` objects representing the neutron.
        """
        return [x for x in self.nucleons if x.pdg_code == '2112']

    def get_protons(self):
        """
        Retrieves the protons from the list of nucleons.

        Returns:
            list: A list of `Nucleon` objects representing the proton.
        """
        return [x for x in self.nucleons if x.pdg_code == '2212']



    def get_neutron_number(self):
        """Returns the number of neutrons in the nucleus."""
        return self.mass_number - self.atomic_number

    def get_proton_number(self):
        """Returns the number of protons in the nucleus."""
        return self.atomic_number

    def info(self):
        """Print the mass number and atomic number of the nuclear profile."""
        print(f'Mass number   \t {self.mass_number}     ')
        print(f'Atomic number \t {self.atomic_number}   ')
        return

    @classmethod
    def get_radius_from_mass_number(cls, mass_number):
        '''Calculate the nuclear radius based on the mass number'''
        return NuclearProfile.NUCLEAR_RADIUS_PARAMETER * pow(mass_number, 1/3.)

    @classmethod
    def get_z_from_name(cls, element):
        """Find atomic number from element name.

        Args:
            element (str): The name of the element.

        Returns:
            int: The atomic number of the element.
        """
        if not isinstance(element, str):
            raise ValueError("Element name be a string")
        
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
            

import numpy as np

def Y20(theta):
    Y = 3*np.cos(theta)**2 - 1
    Y *= (1/4) * np.sqrt(5/np.pi)
    return Y

def Y22(theta, phi):
    Y = 2*np.cos(2*phi)*np.sin(theta)**2
    Y *= (1./4.) * np.sqrt((15.0/2.0)/np.pi)
    return Y

def Y30(theta):
    Y = 5.0*(np.cos(theta))**3 - 3.0*np.cos(theta)
    Y *= 1.0/4.0*np.sqrt(7.0/np.pi)*Y
    return Y

def Y40(theta):
    Y = 35.0*(np.cos(theta))**4 - 30.0*(np.cos(theta))**2 +3.0
    Y *= 3.0 /16.0 /np.sqrt(np.pi)
    return Y

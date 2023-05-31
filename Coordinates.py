import numpy as np
import math

def sph2cart(r, theta, phi):
    """ return [x, y, z]"""
    return [
        r * np.sin(theta) * np.cos(phi),
        r * np.sin(theta) * np.sin(phi),
        r * np.cos(theta)
    ]

def cart2sph(x,y,z):
    """ return [r, theta, phi]"""
    return [
        np.sqrt(x**2 + y**2 + z**2),
        np.arctan2(y,x),
        np.arctan(np.sqrt(x**2+y**2)/z)
    ]


def EulerXYZ(matrix, alpha, beta, gamma): 
    X3 = np.copy(matrix[0])
    Y3 = np.copy(matrix[1])
    Z3 = np.copy(matrix[2])
    if(len(X3.shape)<3):
        X2, Y2, Z2 = RotateX(X3, Y3, Z3, alpha)
        X1, Y1, Z1 = RotateY(X2, Y2, Z2, beta)
        X,  Y,  Z  = RotateZ(X1, Y1, Z1, gamma)
    else:
        X2, Y2, Z2 = RotateX(X3, Y3, Z3, alpha)
        X1, Y1, Z1 = RotateY(X2, Y2, Z2, beta)
        X,  Y,  Z  = RotateZ(X1, Y1, Z1, gamma)
    return [X, Y, Z]

def RotateX(x1,y1,z1, gamma):
    if(gamma==0): return [x1,y1,z1]
    x = x1
    y = y1*np.cos(gamma) - z1*np.sin(gamma)
    z = y1*np.sin(gamma) + z1*np.cos(gamma)
    return [x,y,z]

def RotateY(x1,y1,z1, beta):
    if(beta==0): return [x1,y1,z1]
    x = x1*np.cos(beta) + z1*np.sin(beta)
    y = y1
    z = -x1*np.sin(beta) + z1*np.cos(beta)
    return [x,y,z]

def RotateZ(x1,y1,z1, alpha):
    if(alpha==0): return [x1,y1,z1]
    x = x1*np.cos(alpha) - y1*np.sin(alpha)
    y = x1*np.sin(alpha) + y1*np.cos(alpha)
    z = z1
    return [x,y,z]
import math
from PyNite import FEModel3D

def read_beam_file(filename:str)->str:
    """
    Returns a string representing the text data in the file
    at 'filename'.
    """
    with open(filename) as file:
        file_data=file.read()
    return file_data


def str_to_int(s: str) -> int:
    """
    Returns an integer if the string 's' represents an integer
    """
    return int(s)

def str_to_float(s: str) -> float:
    """
    Returns an float if the string 's' represents an float
    """
    return float(s)

def calc_shear_modulus (nu:float, E:float) -> float:
    """
    Return the shear moduls calculated from 'nu' and 'E'
    """
    G=E/(2*(1+nu))
    return G

def euler_buckling_load(
    l: float,
    E: float,
    I: float,
    k: float,
) -> float:
    """
    Returns the Euler critical load for the column section described by 'l', 'E', 'I' and 'k'.
    'l': braced length of the column
    'E': Elastic moduls
    'I': Second moment of area
    'k': Effective length factor
    """
    P_cr=math.pi**2*E*I/(k*l)**2
    return P_cr

def beam_reactions_ss_cant(
    w:float,
    b:float,
    a:float,
) -> tuple[float,float]:
    """
    Returms the reactions "R1" and "R2" for a simply supported beam
    with a continuous cantilever on one end. R2 is the backspan support and R1 is the hammer support.
    """
    length=b+a
    centroid_of_udl=length/2
    equiv_point_load=w*length
    r1=equiv_point_load*centroid_of_udl/b
    r2=equiv_point_load-r1
    return -r1,-r2

def fe_model_ss_cant(
    w: float,
    b: float,
    a: float,
    E: float, 
    I: float, 
    A: float, 
    J: float, 
    nu: float, 
    rho: float=1.,
)->FEModel3D:
    """
    Return a Pynite.FEModel3D model of a simply supported beam
    with a cantilever on one end. The beam is loaded with a UDL

    "w": The magnitude of the UDL
    "b": The length of the backspan
    "a": The length of the cantilever
    "E": The elastic modulus
    "I": The second moment of inertia
    "A": The cross-sectional area
    "J": The polar moment of inertia
    "nu": Poisson's ratio of material
    "rho": Density of the material
    """
    model=FEModel3D()
    G=calc_shear_modulus(nu,E)
    model.add_material('default',E,G,nu,rho)
    model.add_node("N0",0,0,0)
    model.add_node("N1",b,0,0)
    model.add_node("N2",b+a,0,0)
    model.def_support("N0",True,True,True,True,True,False)
    model.def_support("N1",False,True,False,False,False,False)
    model.add_member("M0","N0","N2",'default',Iy=1.0,Iz=I,J=J,A=A)
    model.add_member_dist_load("M0","Fy",w1=w,w2=w)
    return model
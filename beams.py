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

def read_beam_file(filename:str)->str:
    """
    Returns a string representing the text data in the file
    at 'filename'.
    """
    with open(filename) as file:
        file_data=file.read()
    return file_data

def separate_lines(file_data):
   """
   Separates lines in a string containing new line characters into a list.

   Args:
       file_data: A string containing text with new line characters.

   Returns:
       A list of strings, where each element represents a line in the original data.
   """
   lines = file_data.splitlines()
   return lines

def extract_data(data_list, index):
    """
    Extracts the data list item corresponding to the index and returns it as a separate list.
    """
    data_item = data_list[index]
    data_item.split()
    return data_item.split(",")

def get_spans(beam_length:float,cant_support_loc:float):
    """
    This functions takes the total length of the beam and the
    location of the cantilever support and returns the length 
    of the backspan.
    """
    b=beam_length-cant_support_loc
    a=beam_length-b
    return a,b

from PyNite import FEModel3D

def build_beam(beam_data: list[str]) -> FEModel3D:
    """
    Returns a beam finite element model for the data in 'beam_data' which is assumed to represent
    a simply supported beam with a cantilever at one end with a uniform distributed load applied
    in the direction of gravity.
    """
    LEI = extract_data(beam_data, 0)
    L = str_to_float(LEI[0])
    E = str_to_float(LEI[1])
    I = str_to_float(LEI[2])
    supports_1_and_2 = extract_data(beam_data, 1)
    loc_sup_1=str_to_float(supports_1_and_2[0])
    loc_sup_2=str_to_float(supports_1_and_2[1])
    loads=extract_data(beam_data,2)
    udl=str_to_float(loads[0])
    l_cant=L-loc_sup_2
    l_backspan=L-l_cant
    beam_data=udl,l_backspan,l_cant,E,I,1,1,1,
    beam_model=fe_model_ss_cant(beam_data[0],beam_data[1],beam_data[2],beam_data[3],beam_data[4],beam_data[5],beam_data[6],beam_data[7])
    return beam_model  

def load_beam_model(filename:str) -> FEModel3D:
    """
    This function converts a beam data into a beam model.
    It assumes model the beam is a simply supported beam
    with a cantilever on one end and the beam is loaded with a UDL
    """
    beam_data=read_beam_file(filename)
    beam_lines=separate_lines(beam_data)
    beam_model=build_beam(beam_lines)
    return beam_model
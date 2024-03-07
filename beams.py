import math
import csv

def get_spans(beam_length:float,cant_support_loc:float):
    """
    This functions takes the total length of the beam and the
    location of the cantilever support and returns the length 
    of the backspan.
    """
    b=beam_length-cant_support_loc
    a=beam_length-b
    return a,b
def str_to_int(s: str) -> int:
    """
    Returns an integer if the string 's' represents an integer
    """
    return int(s)
def str_to_float(s: str)-> float|str:
    """
    Returns the string 's' converted into a float if possible.
    Returns the original string, 's', otherwise.
    """
    try:
        return float(s)
    except ValueError:
        return s
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
    print(equiv_point_load)
    r1=equiv_point_load*centroid_of_udl/b
    r2=equiv_point_load-r1
    print(r1,r2,r1+r2)
    return -r1,-r2

def read_beam_file(filename:str)->list[list[str]]:
    """
    Returns a string representing the text data in the file
    at 'filename'.
    """
    csvfile_data=[]
    with open(filename,"r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            csvfile_data.append(line)
    return csvfile_data

def separate_data(filename:list[str])->list[list[str]]:
    """
    The function returns a list containing the strings of a list split in new list
    """
    split_data=[]
    for line in filename:
        split=line.split(", ")
        split_data.append(split)
    return split_data


def convert_to_numeric(raw_data: list[list[str]]) -> list[list[float]]:
    """
    Returns a nested list of floats representing all of the numeric string data in
    'raw_data' being converted into a floats. 

    If the data cannot be converted, a ValueError will be raised.
    """
    outer_acc = []
    for line in raw_data:
        inner_acc = []
        for element in line:
            inner_acc.append(str_to_float(element))
        outer_acc.append(inner_acc)
    return outer_acc

def get_structured_beam_data(filename:list[list[str]])->dict:
    """
    This function returns a dictionary with the input beam data parcelled out.
    """
    beam_dict = {}
    beam_dict['Name']=filename[0][0]
    beam_dict.update(parse_beam_attributes(convert_to_numeric(filename)[1]))
    beam_dict['Supports']=parse_supports(convert_to_numeric(filename)[2])
    beam_dict['Loads']=parse_loads(convert_to_numeric(filename)[3:])
    return beam_dict 
  
def get_node_locations(support_locations: list[float], beam_length: float) -> dict[str, float]:
    """
    Returns a dict representing the node names and node coordinates required for
    a beam with support locations at 'support_locations' and a beam of length of 
    'beam_length'.

    Each node name and node location is unique. Nodes are numbered sequentially from
    left to right starting at "N0".
    """
    nodes_to_create = support_locations[:] # make a copy
    if 0.0 not in support_locations:
        nodes_to_create.append(0.0)
    if beam_length not in support_locations:
        nodes_to_create.append(beam_length)
        
    node_locations = {}
    for idx, sup_loc in enumerate(sorted(nodes_to_create)):
        node_locations.update({f"N{idx}": sup_loc})
    return node_locations

def calc_shear_modulus (nu:float, E:float) -> float:
    """
    Return the shear moduls calculated from 'nu' and 'E'
    """
    G=E/(2*(1+nu))
    return G

from PyNite import FEModel3D
def build_beam(beam_data: dict) -> FEModel3D:
    """
    Returns a FEModel3D of a beam that has the attributes described in 'beam_data' and 'A', 'J', 'nu', and 'rho'.
    """
    beam_data['Nodes'] = get_node_locations(list(beam_data['Supports'].keys()),beam_data['L'])
    beam_model = FEModel3D()
    for node_name, x_coord in beam_data['Nodes'].items():
        beam_model.add_node(node_name, x_coord, 0, 0)
        support_type = beam_data['Supports'].get(x_coord, None)
        if support_type == "P":
            beam_model.def_support(node_name, True, True, True, True, False, False)
        elif support_type == "R":
            beam_model.def_support(node_name, False, True, True, False, False, False)
        elif support_type == "F":
            beam_model.def_support(node_name, True, True, True, True, True, True)

    shear_modulus = calc_shear_modulus(beam_data['E'], beam_data['nu'])
    beam_model.add_material("Beam Material", beam_data['E'], shear_modulus, beam_data['nu'], beam_data['rho'])
    
    # The variable 'node_name' retains the last value from the for loop
    # Which gives us the j-node
    beam_model.add_member(
        beam_data['Name'], 
        "N0", 
        node_name, 
        material="Beam Material", 
        Iy=beam_data['Iy'], 
        Iz=beam_data['Iz'],
        J=beam_data['J'],
        A=beam_data['A'],
    )
    for load in beam_data['Loads']:
        if load['Type'] == "Point":
            beam_model.add_member_pt_load(
                beam_data['Name'],
                load['Direction'],
                load['Magnitude'],
                load['Location']
            )
        elif load['Type'] == "Dist":
            beam_model.add_member_dist_load(
                beam_data['Name'],
                load['Direction'],
                load['Start Magnitude'],
                load['End Magnitude'],
                load['Start Location'],
                load['End Location']
            )
    return beam_model
def load_beam_model(filename:str) -> FEModel3D:
    """
    This function converts a beam data into a beam model.
    It assumes model the beam is a simply supported beam
    with variable number of supports and the beam is loaded with a UDL
    """
    beam_model=build_beam(get_structured_beam_data(read_beam_file(filename)))
    return beam_model

def parse_supports(filename:list[str])->dict[float, str]:
    """
        Returns a dictionary representing the data in 'supports' separated
    out into a dictionary with support locations as keys and support types
    as values. 

    Assumes 'supports' is in a format that looks like this:
    ['support_loc:support_type', 'support_loc:support_type', etc...]
    e.g. ['1000:P', '3800:R', '6000:R']
    Where the valid support types are one of: P (pinned), F (fixed), or R (roller)
    """
    parsed={}
    for support in filename:
        sup_loc,sup_type=support.split(":")
        parsed.update({str_to_float(sup_loc):sup_type})
    return parsed

def parse_loads(filename)->list[dict]:
    """
    Returns a the loads in 'loads_data' structured into a list of dicts.
    """
    parsed=[]
    for load in filename:
        load_type,load_dir=load[0].split(":")
        load_case=load[-1].split(":")[-1]
        if load_type=="POINT":
            magnitude=load[1]
            location=load[2]
            parsed.append({"Type":load_type.title(),
                           "Direction":load_dir.title(),
                           "Magnitude":magnitude,
                           "Location":location,
                           "Case":load_case})

        elif load_type=="DIST":
            start_magnitude=load[1]
            end_magnitude=load[2]
            start_location=load[3]
            end_location=load[4]
            parsed.append({"Type": load_type.title(),
                    "Direction": load_dir.title(),
                    "Start Magnitude": start_magnitude,
                    "End Magnitude": end_magnitude,
                    "Start Location": start_location,
                    "End Location": end_location,
                    "Case": load_case})
    return parsed

def parse_beam_attributes(filename:list[float]) -> dict[str, float]:
    """
    Returns a dictionary of beam attributes according to which attributes are present
    in 'beam_attributes' in the order according to the beam file format BEAM_FORMAT.md,
    Workbook_04 edition. The order of attributes are as follows: Length,E,Iz,[Iy,A,J,nu,rho]
    """
    ATTR_ORDER = ["L", "E", "Iz", "Iy", "A", "J", "nu", "rho"]
    parsed = {}
    for idx, attr in enumerate(ATTR_ORDER):
        try:
            attr_present = filename[idx]
            parsed.update({attr: attr_present})
        except IndexError:
            parsed.update({attr: 1.0})
    return parsed
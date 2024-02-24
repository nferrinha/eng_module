def read_beam_file(filename:str):
    """
    Returns a string representing the text data in the file
    at 'filename'.
    """
    file_data=[]
    with open(filename) as file:
        for line in file.readlines():
            no_newline=line.strip()
            file_data.append(no_newline)
    return file_data

def separate_data(filename:list[str])->list[list[str]]:
    """
    The function returns a list containing the strings of a list split in new list
    """
    split_data=[]
    for line in filename:
        split=line.split(", ")
        split_data.append(split)
    return split_data

def str_to_float(s: str) -> float:
    """
    Returns an float if the string 's' represents an float
    """
    return float(s)

def convert_to_numeric(filename:list[list[str]])->list[list[float]]:
    """
    This function converts strings inside a list into floats
    """
    converted_data=[]
    for line in filename[:]:
        numeric_data=[]
        for sub_lines in line:
            a=str_to_float(sub_lines.replace(",",""))
            numeric_data.append(a)
        converted_data.append(numeric_data)
    return converted_data
def get_structured_data(filename:list[list[str]])->dict:
    """
    This function returns a dictionary with the input beam data parcelled out.
    """
    beam_dict = {}
    for line in filename:
        beam_dict['Name']=filename[0][0]
        beam_dict['L']=convert_to_numeric(filename[1:])[0][0]
        beam_dict['E']=convert_to_numeric(filename[1:])[0][1]
        beam_dict['Iz']=convert_to_numeric(filename[1:])[0][2]
        beam_dict['Supports']=convert_to_numeric(filename[1:])[1]
        beam_dict['Loads']=convert_to_numeric(filename[1:])[2:]
    return beam_dict
  
def get_node_locations(filename:list)->dict[str,float]:
    """
    This function takes the list of support locations and returns a dictionary with the node names and their locations
    """
    node_locations={}
    for i,support in enumerate(filename):
        node_name=f"N{i}"
        node_locations[node_name] = support
    return node_locations

def calc_shear_modulus (nu:float, E:float) -> float:
    """
    Return the shear moduls calculated from 'nu' and 'E'
    """
    G=E/(2*(1+nu))
    return G


from PyNite import FEModel3D
def build_beam(beam_data:dict,A:float=1,J:float=1,nu:float=1,rho:float=1) -> FEModel3D:
    """
    Returns a beam finite element model for the data in 'beam_data' which is assumed to represent
    a simply supported beam with multiple nodes with a uniform distributed load applied
    in the direction of gravity.
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
    node_dict=get_node_locations(beam_data['Supports'])
    E=beam_data['E']
    L=beam_data['L']
    Iz=beam_data['Iz']
    
    model=FEModel3D()
    G=calc_shear_modulus(nu,E)
    model.add_material('default',E,G,nu,rho)
    for node_number,node_coord in node_dict.items():
        model.add_node(node_number,node_coord,0,0)
        model.def_support(node_number,False,True,False,False,False,False)
    model.def_support(node_number,True,True,True,True,True,False)
    model.add_member("M0",(list((node_dict.keys()))[0]),node_number,'default',Iy=1.0,Iz=Iz,J=J,A=A)
    
    for idx,loads in enumerate(beam_data['Loads']):
        model.add_member_dist_load("M0","Fy",loads[0],loads[0],loads[1],loads[2])
    return model
def load_beam_model(filename:str) -> FEModel3D:
    """
    This function converts a beam data into a beam model.
    It assumes model the beam is a simply supported beam
    with variable number of supports and the beam is loaded with a UDL
    """
    beam_model=build_beam(get_structured_data(separate_data(read_beam_file(filename))))
    return beam_model
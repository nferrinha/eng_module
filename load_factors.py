EC_0_COMBS={
    "LC1":{"D":1.35},
    "LC2":{"D":1.35,"L":1.5}
    "LC3":{"D":1.35,"L":1.05,"W":1.5},
    "LC4":{"D":1.35,"L":1.5,"W":0.9}
    "LC5":{"D":1.0,,"W":1.5}
}

def factor_load(
    D_load: float = 0., 
    D: float = 0., 
    L_load: float = 0., 
    L: float = 0., 
    W_load: float = 0., 
    W: float = 0.,
    E_load: float = 0., 
    E: float = 0.,
    S_load: float = 0., 
    S: float = 0.,)->float:
    """
    Returns the factored load for the given load components and factors provided"""
    factored=D_load*D+L_load*L+W_load*W+E_load*E+S_load*S
    return factored
    
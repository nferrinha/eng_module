import pandas as pd
from typing import Optional
from sectionproperties.pre.library import steel_sections as steel
import sectionproperties.pre.geometry as geom
from sectionproperties.analysis.section import Section
from sectionproperties.pre.pre import Material
import numpy as np

df=pd.read_excel("Sections and Merchant Bars-ArcelorMittal_V2023-4.xlsx",sheet_name="EN sections",
                    header=3,
                    usecols="B,D,F:M,AC:AN,AO:AR",
                   )

tidy=df.loc[~(df['Unnamed: 1'].isna()|df['h'].isna())]
pf_sections=tidy.rename(columns=
    {
        "Unnamed: 1":"Section name",
        "Pure bending yy": "Class flexural S355",
        "Unnamed: 41": "Class flexural S460",
        "Pure compression": "Class axial S355",
        "Unnamed: 43": "Class axial S460",
        " iz": "iz"
    }
                       )
for column in pf_sections.columns:
    if column !="Section name":
        pd.to_numeric(pf_sections[column],errors='coerce')

pf_sections.to_csv("eu_pf_sections.csv",index=False)

def load_eu_pf_sections(filename:str="eu_pf_sections.csv"):
    """
    Returns a DataFrame representing the European parallel flange sections
    in the ArcelorMittal catalogue v2023. All units in table have been converted
    to mm scale.
    """
    cm = 1e1 # cm to mm conversion
    df = pd.read_csv(filename)
    
    # Apply dimensional scaling for consistent units of mm across all fields
    df.A = df.A * cm**2
    df.Iy = df.Iy * cm**4
    df['Wel.y'] = df['Wel.y'] * cm**3
    df['Wpl.y'] = df['Wpl.y'] * cm**3
    df.iy = df.iy * cm
    df.Avz =  df.Avz * cm**2
    df.Iz = df.Iz * cm**4
    df['Wel.z'] =  df['Wel.z'] * cm**3
    df['Wpl.z'] = df['Wpl.z'] * cm**3
    df.iz = df.iz * cm
    df.Ss = df.Ss * cm
    df.It = df.It * cm**4
    df.Iw = df.Iw * cm**6 * 1e3
    return df

def sections_filter(df: pd.DataFrame, operator: str, **kwargs) -> pd.DataFrame:
    """
    Returns filtered df a
    """
    sub_df = df.copy()
    if operator not in ["ge", "le"]:
        raise ValueError(f"Invalid operator: {operator}. Please use 'ge' or 'le'.")

    for key, value in kwargs.items():
        if operator == "ge":
            sub_df = sub_df.loc[sub_df[key] >= value]  # Greater than or equal to
        elif operator == "le":
            sub_df = sub_df.loc[sub_df[key] <= value]  # Less than or equal to
       
        if sub_df.empty:
            print(f"No records match the filter criteria: {kwargs}")

    return sub_df

def sort_by_weight(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns sorted df
    """
    df = df.sort_values("kg/m")
    return df

def create_section(
    steel_section: pd.Series, 
    mesh_size: float = 100,
) -> float: 
    """
    Returns a section from section_record
    """
    d = steel_section.d
    b = steel_section.b
    t_f = steel_section.tf
    t_w = steel_section.tw
    k = steel_section.r
    r = k - t_f
    steel_350 = Material("Steel 350 MPa", 200e3, 0.3, 350, 1, color='lightgrey')
    geom = steel.i_section(d=d, b=b, t_f=t_f, t_w=t_w, r=r, n_r = 12, material=steel_350)
    geom.create_mesh(mesh_size)
    section = Section(geom)
    return section
def max_vonmises_stress(
    section: Section,
    N: float = 0,
    Mx: float = 0,
    My: float = 0,
    Vx: float = 0,
    Vy: float = 0,
    Mz: float = 0,
) -> float:
    """
    Returns the maximum von Mises stress that occurs within 'section' when subjected to the combined
    actions of 'N', 'Mx', 'My', 'Mz', 'Vx', 'Vy'.
    """
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    stress_result = section.calculate_stress(N, Vx, Vy, Mx, My, Mzz=Mz)
    stress_dict = stress_result.get_stress()[0]
    vm = stress_dict['sig_vm']
    return np.max(np.abs(vm))


def calculate_section_stresses(
    sections_df: pd.DataFrame,
    fy: float,
    N: float = 0,
    Mx: float = 0,
    My: float = 0,
    Vx: float = 0,
    Vy: float = 0,
    Mz: float = 0
) -> pd.DataFrame:
    """
    Returns 'sections_df' with nine additional columns added:
        - Steel yield strength 
        - N
        - Mx
        - My
        - Vx
        - Vy
        - Mz
        - sig_vm Max (Maximum von Mises stress)
        - DCR stress
        
    Calculated off of the section data in each row and the provided
    force actions.
    """
    for df_idx, row in sections_df.iterrows():
        print(f"Calculating section: {row['Section name']}")
        section = create_section(row, mesh_size=100)
        max_vm_stress = max_vonmises_stress(section, N, Mx, My, Vx, Vy, Mz)
        row['fy'] = fy
        row['sig_vm Max'] = max_vm_stress
        row['DCR stress'] = row['fy'] / row['sig_vm Max']
    return sections_df
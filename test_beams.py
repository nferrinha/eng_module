import eng_module.beams as beams
import math
import csv

def test_get_spans():
    beam1_span=4000,2500
    calculated_beam_span=beams.get_spans(beam1_span[0],beam1_span[1])
    assert calculated_beam_span==(2500, 1500)

def test_str_to_int():
    string_1 = "43"
    string_2 = "2000"
      
    assert beams.str_to_int(string_1)==43
    assert beams.str_to_int(string_2)==2000

def test_str_to_float():
    string_1 = "43"
    string_2 = "2000"
    string_3 = "324.625"
    assert beams.str_to_float(string_1)==43.0
    assert beams.str_to_float(string_2)==2000.0
    assert beams.str_to_float(string_3)==324.625
def test_euler_buckling_load():
    # Column 1 - Value will be in Newtons
    l1 = 5300 # mm
    E1 = 200000 # MPa
    I1 = 632e6 # mm**4
    k1 = 1.0

    # Column 2 - Value will be in kips ("kips" == "kilopound" == 1000 lbs)
    l2 = 212 # inch
    E2 = 3645 # ksi ("ksi" == "kips per square inch")
    I2 = 5125.4 # inch**4
    k2 = 2.0

    assert beams.euler_buckling_load(l1,E1,I1,k1)==44411463.02234584
    assert beams.euler_buckling_load(l2,E2,I2,k2)==1025.6361727834453
    
def test_beam_reactions_ss_cant():
    w1 = 50 # kN/m (which is the same as N/mm)
    a1 = 2350 # mm
    b1 = 4500 # mm

    w2 = 19 # lbs/inch == 228 lbs/ft
    a2 = 96 # inch
    b2 = 96 # inch

    r1_1,r2_1=beams.beam_reactions_ss_cant(w1,b1,a1)
    r1_2,r2_2=beams.beam_reactions_ss_cant(w2,b2,a2)
   
    assert (round(r1_1,2),round(r2_1,2))==(-260680.56,-81819.44)
    assert (round(r1_2,2),round(r2_2,2))==(-3648.0, -0.0)

def test_read_beam_file():
    beam1_data = beams.read_beam_file('test_data/beam_1-wk4.txt')
    assert beam1_data == [['Balcony transfer'],
 ['4800', '24500', '1200000000', '1', '1'],
 ['1000:P', '3800:R'],
 ['POINT:Fy', '-10000', '4800', 'case:Live'],
 ['DIST:Fy', '30', '30', '0', '4800', 'case:Dead']]

def test_separate_data():
    beam_1_result=[
 '4800, 200000, 437000000',
 '0, 3000',
 '-10']
    lines_data=beams.separate_data(beam_1_result)
    assert lines_data==[['4800', '200000', '437000000'],['0', '3000'],['-10']]

def test_str_to_float():
    string_1 = "43"
    string_2 = "2000"
    string_3 = "324.625"
    assert beams.str_to_float(string_1)==43.0
    assert beams.str_to_float(string_2)==2000.0
    assert beams.str_to_float(string_3)==324.625

def test_convert_to_numeric():
    beam1_strings=[
 ['4800', '19200', '1000000000'],
 ['0', '3000'],
 ['-100', '500', '4800'],
 ['-200', '3600', '4800']
]
    assert beams.convert_to_numeric(beam1_strings) ==[[4800.0, 19200.0, 1000000000.0],
 [0.0, 3000.0],
 [-100.0, 500.0, 4800.0],
 [-200.0, 3600.0, 4800.0]]
    
def test_get_structured_beam_data():
    separated_data=beams.read_beam_file("test_data/beam_1-wk4.txt")
    assert beams.get_structured_beam_data(separated_data)=={'Name': 'Balcony transfer',
 'L': 4800.0,
 'E': 24500.0,
 'Iz': 1200000000.0,
 'Iy': 1.0,
 'A': 1.0,
 'J': 1.0,
 'nu': 1.0,
 'rho': 1.0,
 'Supports': {1000.0: 'P', 3800.0: 'R'},
 'Loads': [{'Type': 'Point',
   'Direction': 'Fy',
   'Magnitude': -10000.0,
   'Location': 4800.0,
   'Case': 'Live'},
  {'Type': 'Dist',
   'Direction': 'Fy',
   'Start Magnitude': 30.0,
   'End Magnitude': 30.0,
   'Start Location': 0.0,
   'End Location': 4800.0,
   'Case': 'Dead'}]}
    
def test_get_node_locations():
    beam_length = 10000.0
    supports = [1000.0, 4000.0, 8000.0]
    assert beams.get_node_locations(supports,beam_length)=={'N0': 0.0, 'N1': 1000.0, 'N2': 4000.0, 'N3': 8000.0, 'N4': 10000.0}

def test_calc_shear_modulus():
    E1 = 200000
    nu1 = 0.3
    E2 = 3645
    nu2 = 0.2
    assert math.isclose(beams.calc_shear_modulus(nu1, E1), 76923.077, rel_tol=1e-6)
    assert math.isclose(beams.calc_shear_modulus(nu2, E2), 1518.75, rel_tol=1e-6)

def test_build_beam():
    beam_dict=beams.get_structured_beam_data(beams.read_beam_file("test_data/beam_1-wk4.txt"))
    beam_model = beams.build_beam(beam_dict)
    beam_model.analyze()
    assert math.isclose(beam_model.Members["Balcony transfer"].min_deflection("dy"), -0.5223356009070277, rel_tol=1e-6)

def test_load_beam_model():
    beam_model = beams.load_beam_model('test_data/beam_1-wk4.txt')
    beam_model.analyze()
    assert math.isclose(beam_model.Members["Balcony transfer"].min_deflection("dy"),  -0.5223356009070277, rel_tol=1e-4)

def test_parse_supports():
    input_supports=['1000:P', '3800:R', '4800:F', '8000:R']
    beam_supports=beams.parse_supports(input_supports)
    assert beams.parse_supports(input_supports)=={1000: 'P', 3800: 'R', 4800: 'F', 8000: 'R'}

def test_parse_loads():
    input_loads=[
    ['POINT:Fy', -10000.0, 4800.0, 'case:Live'],
    ['DIST:Fy', 30.0, 30.0, 0.0, 4800.0, 'case:Dead']
]
    beam_loads=beams.parse_loads(input_loads)
    assert beams.parse_loads(input_loads)==[{'Type': 'Point',
  'Direction': 'Fy',
  'Magnitude': -10000.0,
  'Location': 4800.0,
  'Case': 'Live'},
 {'Type': 'Dist',
  'Direction': 'Fy',
  'Start Magnitude': 30.0,
  'End Magnitude': 30.0,
  'Start Location': 0.0,
  'End Location': 4800.0,
  'Case': 'Dead'}]
    
def test_parse_beam_attributes():
    input_attributes=[20e3, 200e3, 6480e6, 390e6, 43900, 11900e3, 0.3]
    beam_attributes=beams.parse_beam_attributes(input_attributes)
    assert beams.parse_beam_attributes(input_attributes)=={'L': 20000.0,
 'E': 200000.0,
 'Iz': 6480000000.0,
 'Iy': 390000000.0,
 'A': 43900,
 'J': 11900000.0,
 'nu': 0.3,
 'rho': 1.0}
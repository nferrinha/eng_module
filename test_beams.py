import eng_module.beams as beams
import math

def test_read_beam_file():
    beam1_data = beams.read_beam_file('test_data/beam_1.txt')
    assert beam1_data == [
 '4800, 200000, 437000000',
 '0, 3000',
 '-10']

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
    separated_data=[['Roof beam'],
 ['4800', '19200', '1000000000'],
 ['0', '3000', '4800'],
 ['-100', '500', '4800'],
 ['-200', '3600', '4800']]
    assert beams.get_structured_beam_data(separated_data)=={'Name': 'Roof beam',
 'L': 4800.0,
 'E': 19200.0,
 'Iz': 1000000000.0,
 'Supports': [0.0, 3000.0, 4800.0],
 'Loads': [[-100.0, 500.0, 4800.0], [-200.0, 3600.0, 4800.0]]}
    
def test_get_node_locations():
    supports=[0.0, 3000.0, 4800.0]
    assert beams.get_node_locations(supports)=={'N0': 0.0, 'N1': 3000.0, 'N2': 4800.0}

def test_calc_shear_modulus():
    E1 = 200000
    nu1 = 0.3
    E2 = 3645
    nu2 = 0.2
    assert math.isclose(beams.calc_shear_modulus(nu1, E1), 76923.077, rel_tol=1e-6)
    assert math.isclose(beams.calc_shear_modulus(nu2, E2), 1518.75, rel_tol=1e-6)

def test_build_beam():
    beam_dict = {
        "Name": "Test Beam",
        "L": 5000,
        "E": 200000,
        "Iz": 400e6,
        "Supports": [0.0, 5000.0],
        "Loads": [[-100, 0.0, 5000.0]],
        "Nodes": {"N0": 0.0, "N1": 5000.0}
    }
    beam_model = beams.build_beam(beam_dict)
    beam_model.analyze()
    assert math.isclose(beam_model.Members['M0'].min_deflection("dy"), -10.172, rel_tol=1e-4)

def test_load_beam_model():
    beam_model = beams.load_beam_model('test_data/beam_4-wk3.txt')
    beam_model.analyze()
    assert math.isclose(beam_model.Members['M0'].min_deflection("dy"),  -68.12, rel_tol=1e-4)
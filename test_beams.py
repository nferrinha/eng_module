import eng_module.beams as beams
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

def test_calc_shear_modulus():
    # Material 1
    E1 = 200000 # MPa
    nu1 = 0.3

    # Material 2
    E2 = 3645 # ksi ("ksi" == "kips per square inch"; "kips" == "kilopound" == 1000 lbs)
    nu2 = 0.2   

    assert beams.calc_shear_modulus(nu1,E1) == 76923.07692307692
    assert beams.calc_shear_modulus(nu2,E2) == 1518.75

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

def test_fe_model_ss_cant():
    w1 = 50 # kN/m (which is the same as N/mm)
    a1 = 2350 # mm
    b1 = 4500 # mm

    w2 = 19 # lbs/inch == 228 lbs/ft
    a2 = 96 # inch
    b2 = 96 # inch

    E=1.
    I=1.
    A=1.
    J=1.
    nu=1.
    model1=beams.fe_model_ss_cant(w1,b1,a1,E,I,A,J,nu)
    model1.analyze()   

    r2_1=model1.Nodes['N0'].RxnFY['Combo 1']
    r1_1=model1.Nodes['N1'].RxnFY['Combo 1']
    ar1_1,ar2_1=beams.beam_reactions_ss_cant(w1,b1,a1)
    assert round(ar2_1,2)==round(r2_1,2)
    assert round(ar1_1,2)==round(r1_1,2)
 
    w2 = 19 # lbs/inch == 228 lbs/ft
    a2 = 96 # inch
    b2 = 96 # inch

    E=1.
    I=1.
    A=1.
    J=1.
    nu=1.
    model2=beams.fe_model_ss_cant(w2,b2,a2,E,I,A,J,nu)
    model2.analyze()   

    r2_2=model2.Nodes['N0'].RxnFY['Combo 1']
    r1_2=model2.Nodes['N1'].RxnFY['Combo 1']
    ar1_2,ar2_2=beams.beam_reactions_ss_cant(w2,b2,a2)
    assert round(ar2_2,2)==round(r2_2,2)
    assert round(ar1_2,2)==round(r1_2,2)

def test_read_beam_file():
    beam1_data = beams.read_beam_file('test_data/beam_1.txt')
    assert beam1_data == '4800, 200000, 437000000\n0, 3000\n-10'

def test_separate_lines():
    beam_1_result='4800, 200000, 437000000\n0, 3000\n-10'
    lines_data=beams.separate_lines(beam_1_result)
    assert lines_data==['4800, 200000, 437000000', '0, 3000', '-10']

def test_extract_data():
    beam_1_data=['4800, 200000, 437000000', '0,3000', '-10']
    extracted_data=beams.extract_data(beam_1_data,0)
    assert extracted_data==['4800', ' 200000', ' 437000000'] 

def test_get_spans():
    beam1_span=4000,2500
    calculated_beam_span=beams.get_spans(beam1_span[0],beam1_span[1])
    assert calculated_beam_span==(2500, 1500)

def test_load_beam_model():
    beam_2_model=beams.load_beam_model('test_data/beam_2.txt')
    beam_2_model.analyze()
    support_n0=beam_2_model.Nodes['N0'].RxnFY
    support_n1=beam_2_model.Nodes['N1'].RxnFY
    assert round(support_n0['Combo 1'],0)==0
    assert round(support_n1['Combo 1'],0)==3420
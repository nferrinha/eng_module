import concrete_transport_calculator as ctc  # Import script


# Test Function for calculate_loading_time
def test_calculate_loading_time():
    assert ctc.calculate_loading_time(200, 10) == 3

# Test Function for calculate_adjusted_loading_time
def test_calculate_adjusted_loading_time():
    assert ctc.calculate_adjusted_loading_time(3, 20) == 4  # Typical

# Test Function for calculate_transit_time
def test_calculate_transit_time():
    # Test valid input
    assert ctc.calculate_transit_time(5, 20) == 15
    assert ctc.calculate_transit_time(10, 15) == 40

# Test Function for calculate_pumping_time
def test_calculate_pumping_time():
    assert ctc.calculate_pumping_time(20, 10) == 30  # Typical

# Test Function for calculate_mixers_needed
def test_calculate_mixers_needed():
    assert ctc.calculate_mixers_needed(200, 150) == 2

# Test Function for calculate_batching_plants_needed
def test_calculate_batching_plants_needed():
    assert ctc.calculate_batching_plants_needed(200, 100) == 2

# Test Function for calculate_mixers_loaded_per_hour
def test_calculate_mixers_loaded_per_hour():
    assert ctc.calculate_mixers_loaded_per_hour(4, 200, 100) == 30 
    
# Test Function for calculate_effective_hourly_rate
def test_calculate_effective_hourly_rate():
    assert ctc.calculate_effective_hourly_rate(20, 10) == 200
    
# Test Function for calculate_gross_one_way_time
def test_calculate_gross_one_way_time():
    assert ctc.calculate_gross_one_way_time(3, 15, 30) == 48

# Test Function for calculate_total_adjusted_one_way_time
def test_calculate_total_adjusted_one_way_time():
    assert ctc.calculate_total_adjusted_one_way_time(48, 75) == 64

# Test Function for calculate_adjusted_return_time
def test_calculate_adjusted_return_time():
    assert ctc.calculate_adjusted_return_time(64, 15, 75) == 79

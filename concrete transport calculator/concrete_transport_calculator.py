import numpy as np
import plotly.subplots as sp 
import plotly.graph_objects as go

mixer_capacities = {  # Add your mixer data here
    "Putzmeister P 8 HR": 8,
    "Putzmeister P 9 HR": 9,
    "Putzmeister P 10 HR": 10,
    "Putzmeister P 12 HR": 12,
    "Everdigm ETM 12": 12
}

# User Inputs 
mixer_type = "Putzmeister P 10 HR" 
distance = 5.08 
speed = 15  
batch_plant_rate = 200
theoretical_rate = 200
maneuver_allowance = 20
pumping_rate = 20
fleet_allowance = 25
num_mixers = 8  # Or the number of mixers you want to simulate

def calculate_loading_time(batch_plant_rate, mixer_volume):
  if batch_plant_rate <= 0:
    raise ValueError("Batch plant rate cannot be zero or negative")
  return mixer_volume / batch_plant_rate

def calculate_adjusted_loading_time(loading_time, maneuver_allowance):
  if maneuver_allowance < 0:
    raise ValueError("Maneuver allowance cannot be negative")
  return loading_time * (1 + maneuver_allowance/100)

def calculate_transit_time(distance, speed):
  if distance <= 0:
    raise ValueError("Distance cannot be zero or negative")
  if speed <= 0:
    raise ValueError("Speed cannot be zero or negative")
  return (distance * 1000) / (speed * 60) 

def calculate_pumping_time(pumping_rate, mixer_volume):
  if pumping_rate <= 0:
    raise ValueError("ConcretePumping rate cannot be zero or negative")
  return mixer_volume / pumping_rate

def calculate_mixers_needed(theoretical_rate, effective_rate):
  if theoretical_rate <= 0:
    raise ValueError("Theoretical rate cannot be zero or negative")
  return np.ceil(theoretical_rate / effective_rate).astype(int)

def calculate_batching_plants_needed(theoretical_rate, batch_plant_rate):
  return np.ceil(theoretical_rate / batch_plant_rate).astype(int) 

def calculate_mixers_loaded_per_hour(adjusted_loading_time, theoretical_rate, batch_plant_rate):
  num_batching_plants = calculate_batching_plants_needed(theoretical_rate, batch_plant_rate)
  effective_rate_per_plant = 60 / adjusted_loading_time
  return np.floor(effective_rate_per_plant * num_batching_plants).astype(int)

def calculate_effective_hourly_rate(mixers_loaded_per_hour, mixer_volume):
  return mixers_loaded_per_hour * mixer_volume

def calculate_gross_one_way_time(loading_time, transit_time, pumping_time):
  return loading_time + transit_time + pumping_time

def calculate_total_adjusted_one_way_time(gross_one_way_time, fleet_allowance):
  if fleet_allowance < 0:
    raise ValueError("Fleet allowance cannot be negative")
  return gross_one_way_time * (1 + fleet_allowance/100)

def calculate_adjusted_return_time(total_adjusted_one_way_time, transit_time, fleet_allowance):
  return total_adjusted_one_way_time + transit_time * (1 + fleet_allowance/100)
    
    
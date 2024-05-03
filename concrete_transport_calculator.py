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

class ConcreteMixerProject:
    def __init__(self, mixer_type):
        self.mixer_type = mixer_type
        self.mixer_volume = mixer_capacities[mixer_type]

    def calculate_loading_time(self, batch_plant_rate):
     if batch_plant_rate <= 0:
         raise ValueError("Batch plant rate cannot be zero or negative")

     loading_time = self.mixer_volume / batch_plant_rate
     return loading_time 

    def calculate_adjusted_loading_time(self, loading_time, maneuver_allowance):
        if maneuver_allowance < 0:
            raise ValueError("Maneuver allowance cannot be negative")
        adjusted_loading_time = loading_time * (1 + maneuver_allowance/100)
        return adjusted_loading_time

    def calculate_transit_time(self, distance, speed):
        if distance <= 0:
            raise ValueError("Distance cannot be zero or negative")
        if speed <= 0:
            raise ValueError("Speed cannot be zero or negative")
        transit_time = (distance * 1000) / (speed * 60)  # Convert to minutes
        return transit_time

    def calculate_pumping_time(self, pumping_rate):
        if pumping_rate <= 0:
            raise ValueError("ConcretePumping rate cannot be zero or negative")

        pumping_time = self.mixer_volume / pumping_rate
        return pumping_time

    def calculate_mixers_needed(self, theoretical_rate, effective_rate):
        if theoretical_rate <= 0: 
            raise ValueError("Theoretical rate cannot be zero or negative")
        mixers_needed = np.ceil(theoretical_rate / effective_rate).astype(int)  
        return mixers_needed  # Round up and convert to integer
    
    def calculate_batching_plants_needed(self, theoretical_rate, batch_plant_rate):
        plants_needed = np.ceil(theoretical_rate / batch_plant_rate).astype(int)
        return plants_needed  # Round up and convert to integer
    
    def calculate_mixers_loaded_per_hour(self, adjusted_loading_time):
        num_batching_plants = self.calculate_batching_plants_needed(self.theoretical_rate, self.batch_plant_rate)

        # Now calculate the effective rate as before
        effective_rate_per_plant = 60 / adjusted_loading_time 
        mixers_loaded_hour = np.floor(effective_rate_per_plant * num_batching_plants).astype(int)
        return mixers_loaded_hour  # Round down and convert to integer

    def calculate_effective_hourly_rate(self, mixers_loaded_per_hour):
        return mixers_loaded_per_hour * self.mixer_volume

    def calculate_gross_one_way_time(self, loading_time, transit_time, pumping_time):
        gross_one_way_time = loading_time + transit_time + pumping_time
        return gross_one_way_time 
    
    def calculate_total_adjusted_one_way_time(self, gross_one_way_time, fleet_allowance):
        if fleet_allowance < 0:
            raise ValueError("Fleet allowance cannot be negative")

        total_adjusted_one_way_time = gross_one_way_time * (1 + fleet_allowance/100)
        return total_adjusted_one_way_time

    def calculate_adjusted_return_time(self, total_adjusted_one_way_time, transit_time, fleet_allowance):
        adjusted_return_time = total_adjusted_one_way_time + transit_time * (1 + fleet_allowance/100)
        return adjusted_return_time
    
    def generate_timeline(self):
        timeline = [(0, 0)]  # Mixer starts at 0
        timestamps = []
        queue_sizes = []
        current_timestamp = 0
        self.mixers_in_queue = 0  # Initialize the queue

        # Initial Loading 
        start_loading = current_timestamp 
        end_loading = current_timestamp + self.calculate_adjusted_loading_time(self.loading_time, self.maneuver_allowance)
        timeline.extend([(start_loading, 0), (end_loading, 0)]) 
        timestamps.extend([start_loading, end_loading])
        queue_sizes.extend([self.mixers_in_queue, self.mixers_in_queue]) 
        self.mixers_in_queue += 1 

        # ... Transit to Site, Pumping at Site, Return Transit ...

        # Mixer returning, update queue
        start_return = current_timestamp
        end_return = current_timestamp + self.calculate_adjusted_return_time(self.total_adjusted_one_way_time, self.transit_time, self.fleet_allowance)
        timeline.extend([(start_return, 0), (end_return, 0)])
        current_timestamp = end_return
        timestamps.extend([start_return, end_return])
        queue_sizes.extend([self.mixers_in_queue, self.mixers_in_queue])

        # Potential Wait in Queue
        while self.mixers_in_queue >= self.num_batching_plants: 
            wait_time = self.calculate_adjusted_loading_time(self.loading_time, self.maneuver_allowance)
            timeline.extend([(current_timestamp, 0), (current_timestamp + wait_time, 0)])
            current_timestamp += wait_time  
            timestamps.extend([current_timestamp, current_timestamp])
            queue_sizes.extend([self.mixers_in_queue, self.mixers_in_queue]) 

        # Next Mixer Begins Loading
        self.mixers_in_queue -= 1  

        return timeline, timestamps, queue_sizes

def generate_visualization(self, mixer_data):
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    # Main Timeline (With waiting visualization)
    for mixer in mixer_data:
        x = []
        y = []
        is_waiting = False

        for timestamp, location in mixer["timeline"]:
            if location == 0 and is_waiting:
                y.append(f"Mixer {mixer['id']} (Waiting)") 
            else:
                y.append(f"Mixer {mixer['id']}")

            x.append(timestamp)
            is_waiting = location == 0 and self.mixers_in_queue >= self.num_batching_plants 

        trace = go.Scatter(
            x=x, 
            y=y, 
            mode='markers+lines', 
            line=dict(color='red' if is_waiting else 'blue')
        )
 
        fig.add_trace(trace, row=1, col=1)

    fig.update_layout(title="Mixer Positions Timeline (with Queue)")
    fig.show()

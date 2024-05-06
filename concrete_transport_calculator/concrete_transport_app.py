import streamlit as st
from concrete_transport_calculator import mixer_capacities, calculate_loading_time, calculate_adjusted_loading_time,  calculate_transit_time, calculate_pumping_time, calculate_mixers_needed, calculate_batching_plants_needed, calculate_mixers_loaded_per_hour, calculate_effective_hourly_rate, calculate_gross_one_way_time, calculate_total_adjusted_one_way_time, calculate_adjusted_return_time
import plotly.graph_objects as go

def dashboard_page():
    st.title("Concrete Mixer Dashboard") 
    #User Inputs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        distance = st.number_input("Distance to Casting Site (km)", value=5.08, min_value=0.01)
        speed = st.number_input("Mixer Average Speed (km/h)", value=15.0, min_value=0.01)
        theoretical_rate = st.number_input("Theoretical Concrete Rate Required (m3/hr)", value=200.0, min_value=0.01)
    
    with col2:
        batch_plant_rate = st.number_input("Batching Plant Rate (m3/hr)", value=200.0, min_value=0.01)
        pumping_rate = st.number_input("Concrete Pumping Rate (m3/hr)", value=20.0, min_value=0.01)
    
    with col3:
        maneuver_allowance = st.number_input("Maneuver Allowance (%)", value=20)
        fleet_allowance = st.number_input("Fleet Allowance (%)", value=25)
    
    def calculate_and_update_chart(distance, speed, batch_plant_rate, theoretical_rate, maneuver_allowance, pumping_rate, fleet_allowance):
        mixer_results = {}
        for name, capacity in mixer_capacities.items():
            loading_time = calculate_loading_time(batch_plant_rate, capacity)
            adjusted_loading_time = calculate_adjusted_loading_time(loading_time, maneuver_allowance)
            transit_time = calculate_transit_time(distance, speed)
            pumping_time = calculate_pumping_time(pumping_rate, capacity)
            gross_one_way_time = calculate_gross_one_way_time(adjusted_loading_time, transit_time, pumping_time)
            adjusted_one_way_time = calculate_total_adjusted_one_way_time(gross_one_way_time, fleet_allowance)
            mixer_results[name] = adjusted_one_way_time
    
        fig = go.Figure(data=[go.Bar(
            x=list(mixer_results.keys()),
            y=list(mixer_results.values())
        )])
    
        fig.update_layout(title="One-Way Time per Mixer",
                          xaxis_title="Mixer Type",
                          yaxis_title="Time (minutes)")  
        return fig 
    fig = calculate_and_update_chart(distance, speed, batch_plant_rate, theoretical_rate, maneuver_allowance, pumping_rate, fleet_allowance)
    st.plotly_chart(fig)

def mixer_details_page():
    st.title("Detailed Concrete Mixer Transport Calculations")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mixer_type = st.selectbox("Select Mixer Type", list(mixer_capacities.keys()))
        distance = st.number_input("Distance to Casting Site (km)", value=5.08, min_value=0.01)
        speed = st.number_input("Mixer Average Speed (km/h)", value=15.0, min_value=0.01)
    
    with col2:
        theoretical_rate = st.number_input("Theoretical Concrete Rate Required (m3/hr)", value=200.0, min_value=0.01)
        batch_plant_rate = st.number_input("Batching Plant Rate (m3/hr)", value=200.0, min_value=0.01)
        pumping_rate = st.number_input("Concrete Pumping Rate (m3/hr)", value=20.0, min_value=0.01)

    with col3:
        maneuver_allowance = st.number_input("Maneuver Allowance (%)", value=20)
        fleet_allowance = st.number_input("Fleet Availability (%)", value=75)

    mixer_volume = mixer_capacities[mixer_type]
    
    # Initialize variables        
    loading_time = 0
    adjusted_loading_time = 0
    transit_time = 0
    pumping_time = 0
    plants_needed = 0
    mixers_loaded_per_hour=0
    hourly_rate = 0
    gross_one_way_time = 0
    total_adjusted_one_way_time = 0
    adjusted_return_time = 0

    if st.button("Show Detailed Results"):
        mixer_volume = mixer_capacities[mixer_type]
        loading_time = calculate_loading_time(batch_plant_rate, mixer_volume)
        adjusted_loading_time = calculate_adjusted_loading_time(loading_time, maneuver_allowance)
        transit_time = calculate_transit_time(distance, speed)
        pumping_time = calculate_pumping_time(pumping_rate, mixer_volume)
        plants_needed = calculate_batching_plants_needed(theoretical_rate, batch_plant_rate)
        mixers_loaded_per_hour=calculate_mixers_loaded_per_hour(adjusted_loading_time, theoretical_rate, batch_plant_rate)
        hourly_rate = calculate_effective_hourly_rate(mixers_loaded_per_hour, mixer_volume)
        gross_one_way_time = calculate_gross_one_way_time(adjusted_loading_time, transit_time, pumping_time)
        total_adjusted_one_way_time = calculate_total_adjusted_one_way_time(gross_one_way_time, fleet_allowance)
        adjusted_return_time = calculate_adjusted_return_time(total_adjusted_one_way_time, transit_time, fleet_allowance)

    st.subheader("Results")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Mixer Type", mixer_type)
        st.metric("Mixer Drum Capacity (m3)", mixer_capacities[mixer_type])
        st.metric("Number of Batching Plants Required", plants_needed)     
        st.metric("Gross Concrete Loading Time (min)", loading_time)
        st.metric("Concrete Loading Time including Truck Manouvering (min)", adjusted_loading_time)
        st.metric("N° Mixers Loaded/Hour", mixers_loaded_per_hour)
        st.metric("Effective Hourly Concrete Rate (m3/h)", hourly_rate)
        
    with col2:        
        st.metric("Transit Time (mins)", transit_time)
        st.metric("Pumping/Unloading Time (mins)", pumping_time)
        st.metric("Total Gross Time (mins)", gross_one_way_time)
        st.metric("Total Adjusted One-Way Time (mins)", total_adjusted_one_way_time)
        st.metric("Total Adjusted Return Time (mins)", adjusted_return_time)
    
def main():
    page = st.sidebar.selectbox("Choose a page", ["Dashboard", "Mixer Details"])

    if page == "Dashboard":
        dashboard_page()
    elif page == "Mixer Details":
        mixer_details_page()

if __name__ == "__main__":
    main()
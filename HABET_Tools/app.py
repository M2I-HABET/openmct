import streamlit as st
from streamlit_folium import st_folium
import serial
import serial.tools.list_ports
import folium
from datetime import datetime
import plotly.graph_objects as go
import pandas as pd
import time


# Configuration and setup
# Initialize Streamlit app
st.title('Telemetry Data Broker')
#st.sidebar.title('Configuration')

# Initialize the map
initial_latitude = 42.035
initial_longitude = -93.613
map_obj = folium.Map(location=[initial_latitude, initial_longitude], zoom_start=7)

# Data prefix to look for in the serial data
data_prefix = '$$HAR'

# List to store the breadcrumb trail (latitude and longitude) and telemetry data
breadcrumb_trail = []
altitude_data = []
temperature_data = []
pressure_data = []
humidity_data = []

# Create empty containers for map and plots
map_container = st.empty()
plot_container = st.empty()

'''
# Function to scan and list available serial ports
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Function to let the user select a serial port
def select_serial_port():
    ports = list_serial_ports()
    if not ports:
        st.error("No serial ports found.")
        return None
    
    selected_port = st.selectbox("Select a serial port", ports)
    return selected_port
'''

# Select the serial port
#selected_port = select_serial_port()
selected_port = '/dev/tty.usbserial-10'
if selected_port is None:
    st.stop()

# Configure the serial connection
ser = serial.Serial(
    port=selected_port,
    baudrate=115200,  # Baud rate
    timeout=1       # Timeout in seconds
)

# Functions

# Function to add a point to the map and update the breadcrumb trail
def update_map(lat, lon, alt):
    global map_obj, breadcrumb_trail
    point = (lat, lon)
    breadcrumb_trail.append(point)

    # Create a new map for Streamlit
    map_obj = folium.Map(location=[lat, lon], zoom_start=7)
    folium.Marker(location=[lat, lon], popup=f"Altitude: {alt} meters").add_to(map_obj)
    if len(breadcrumb_trail) > 1:
        folium.PolyLine(breadcrumb_trail, color="blue").add_to(map_obj)

    # Update the map display in Streamlit
    with map_container:
        st_folium(map_obj, width=700, height=500)

# Function to update the graphs
def update_plots():
    fig = go.Figure()
    if altitude_data:
        fig.add_trace(go.Scatter(y=altitude_data, mode='lines+markers', name='Altitude'))
    if temperature_data:
        fig.add_trace(go.Scatter(y=temperature_data, mode='lines+markers', name='Temperature'))
    if pressure_data:
        fig.add_trace(go.Scatter(y=pressure_data, mode='lines+markers', name='Pressure'))
    if humidity_data:
        fig.add_trace(go.Scatter(y=humidity_data, mode='lines+markers', name='Humidity'))
    
    fig.update_layout(title='Telemetry Data Over Time', xaxis_title='Data Points', yaxis_title='Values')
    
    # Update the plot display in Streamlit
    with plot_container:
        st.plotly_chart(fig, use_container_width=True)


# Main Loop

# Continuously read data from the serial port and update the Streamlit app
try:
    while True:
        data = ser.readline().decode('utf-8').strip()
        if data:
            print(data)
            if data.startswith(data_prefix):
                # Parse the HAR data
                parsed_data = data.split(',')
                latitude = float(parsed_data[1])/10000000
                longitude = float(parsed_data[2])/10000000
                altitude = float(parsed_data[3])/1000
                temperature = float(parsed_data[8])/100
                pressure = float(parsed_data[7])/100
                humidity = float(parsed_data[9])/1000

                # Update the map and plots
                update_map(latitude, longitude, altitude)

                altitude_data.append(altitude)
                temperature_data.append(temperature)
                pressure_data.append(pressure)
                humidity_data.append(humidity)

                update_plots()
                time.sleep(.5)  # Adjust this to control the update rate

except KeyboardInterrupt:
    # Close the serial port on exit
    ser.close()
    st.write("Keyboard interrupt detected. Closing Serial. Exiting...")
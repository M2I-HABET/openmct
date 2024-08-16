import streamlit as st
import folium
from streamlit_folium import st_folium
import serial
import serial.tools.list_ports
import threading
import time

# Initialize the map
initial_latitude = 42.035
initial_longitude = -93.613
map_obj = folium.Map(location=[initial_latitude, initial_longitude], zoom_start=7)


# Telemetry data storage
breadcrumb_trail = []
altitude_data = []
temperature_data = []
pressure_data = []
humidity_data = []

# Function to scan and list available serial ports
def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Function to let the user select a serial port
def select_serial_port():
    ports = list_serial_ports()
    if not ports:
        print("No serial ports found.")
        return None
    
    print("Available serial ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port}")
    
    selected_port = None
    while selected_port is None:
        try:
            choice = int(input("Select a serial port by number: "))
            if 0 <= choice < len(ports):
                selected_port = ports[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    return selected_port

# Select the serial port
selected_port = select_serial_port()
if selected_port is None:
    exit("No serial port selected. Exiting...")

# Configure the serial connection
ser = serial.Serial(
    port=selected_port,
    baudrate=115200,  # Baud rate
    timeout=1       # Timeout in seconds
)


# Function to update the map with new data
def update_map(lat, lon, alt):
    global map_obj, breadcrumb_trail

    point = (lat, lon)
    breadcrumb_trail.append(point)

    # Add marker for the new point
    folium.Marker(location=[lat, lon], popup=f"Altitude: {alt} meters").add_to(map_obj)

    # Update the polyline to show the breadcrumb trail
    if len(breadcrumb_trail) > 1:
        folium.PolyLine(breadcrumb_trail, color="blue").add_to(map_obj)

# Function to read serial data
def serial_reader():
    try:
        while True:
            data = ser.readline().decode('utf-8').strip()
            if data:
                latitude = float(parsed_data[1])/10000000
                longitude = float(parsed_data[2])/10000000
                altitude = float(parsed_data[3])/1000
                temperature = float(parsed_data[8])/100
                pressure = float(parsed_data[7])/100
                humidity = float(parsed_data[9])/1000
                battery = float(parsed_data[11])
                speed = float(parsed_data[5])/10
                pdop = float(parsed_data[6])/10
                heading = float(parsed_data[4])/100000

                # Update map and telemetry data
                update_map(latitude, longitude, altitude)
                altitude_data.append(altitude)
                temperature_data.append(temperature)
                pressure_data.append(pressure)
                humidity_data.append(humidity)

                # Log the data
                print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude} meters")
                print(f"Temperature: {temperature} °C, Pressure: {pressure} hPa, Humidity: {humidity} %")
            
            time.sleep(1)  # Adjust sleep time for your data rate

    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

# Run the serial reader in a separate thread
threading.Thread(target=serial_reader, daemon=True).start()

# Streamlit app setup
st.title("Real-Time Breadcrumb Trail Map")

# Display the updated map in Streamlit
map_display = st_folium(map_obj, width=700, height=500)

# Display the telemetry data
st.subheader("Telemetry Data")
st.write(f"Latest Altitude: {altitude_data[-1] if altitude_data else 'N/A'} meters")
st.write(f"Latest Temperature: {temperature_data[-1] if temperature_data else 'N/A'} °C")
st.write(f"Latest Pressure: {pressure_data[-1] if pressure_data else 'N/A'} hPa")
st.write(f"Latest Humidity: {humidity_data[-1] if humidity_data else 'N/A'} %")

# Real-time plot with Streamlit (altitude, temperature, pressure, humidity)
st.subheader("Real-Time Telemetry Plots")
st.line_chart(altitude_data, width=0, height=0, use_container_width=True)
st.line_chart(temperature_data, width=0, height=0, use_container_width=True)
st.line_chart(pressure_data, width=0, height=0, use_container_width=True)
st.line_chart(humidity_data, width=0, height=0, use_container_width=True)
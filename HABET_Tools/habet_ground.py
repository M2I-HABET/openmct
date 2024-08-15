import serial
import serial.tools.list_ports
import folium
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import plotly.graph_objects as go

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

# Function to add a point to the map and update the breadcrumb trail
def add_point_to_map(lat, lon, alt):
    global map_obj, breadcrumb_trail
    point = (lat, lon)
    breadcrumb_trail.append(point)
    #altitude_data.append(alt)

    # Add marker for the new point
    folium.Marker(location=[lat, lon], popup=f"Altitude: {alt} meters").add_to(map_obj)
    
    # Update the polyline to show the breadcrumb trail
    if len(breadcrumb_trail) > 1:
        folium.PolyLine(breadcrumb_trail, color="blue").add_to(map_obj)

    # Update the map center
    map_obj.location = point

# Function to save the map to an HTML file
def save_map(filename="map.html"):
    map_obj.save(filename)

# Plotting altitude data
#def update_altitude_plot(frame):
#    plt.cla()  # Clear the previous plot
#    plt.plot(altitude_data, marker='o')
#    plt.title('Altitude over Time')
#    plt.xlabel('Data Points')
#    plt.ylabel('Altitude (meters)')
#    plt.grid(True)

# Plotting telemetry data
def update_plots(frame):
    plt.clf()  # Clear the previous plots
    
    plt.subplot(2, 2, 1)
    plt.plot(altitude_data, marker='o', color='blue')
    plt.title('Altitude over Time')
    plt.xlabel('Data Points')
    plt.ylabel('Altitude (meters)')
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(temperature_data, marker='o', color='red')
    plt.title('Temperature over Time')
    plt.xlabel('Data Points')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(pressure_data, marker='o', color='green')
    plt.title('Pressure over Time')
    plt.xlabel('Data Points')
    plt.ylabel('Pressure (hPa)')
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(humidity_data, marker='o', color='purple')
    plt.title('Humidity over Time')
    plt.xlabel('Data Points')
    plt.ylabel('Humidity (%)')
    plt.grid(True)

    plt.tight_layout()

# Select the serial port
selected_port = select_serial_port()
if selected_port is None:
    exit("No serial port selected. Exiting...")

# Initialize the map
initial_latitude = 42.035
initial_longitude = -93.613
map_obj = folium.Map(location=[initial_latitude, initial_longitude], zoom_start=7)

# List to store the breadcrumb trail (latitude and longitude) and altitude data
breadcrumb_trail = []
altitude_data = []
temperature_data = []
pressure_data = []
humidity_data = []

# Configure the serial connection
ser = serial.Serial(
    port=selected_port,
    baudrate=115200,  # Baud rate
    timeout=1       # Timeout in seconds
)

# Set up the plots with FuncAnimation for live updating
plt.figure(figsize=(12, 8))
ani = FuncAnimation(plt.gcf(), update_plots, interval=1000)
plt.show(block=False)
# Continuously read data from the serial port
try:
    while True:
        data = ser.readline().decode('utf-8').strip()
        if data:
            print(data)
            if data.startswith('$$HAR'):
                # Parse the HAR data
                parsed_data = data.split(',')
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

                
                # Add the point to the map and keep the breadcrumb trail
                add_point_to_map(latitude, longitude, altitude)

                altitude_data.append(altitude)
                temperature_data.append(temperature)
                pressure_data.append(pressure)
                humidity_data.append(humidity)
                
                # Print the data
                print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude} meters")
                print(f"Temperature: {temperature} °C, Pressure: {pressure} hPa, Humidity: {humidity} %")
            
                
                # Save the map periodically
                save_map("breadcrumb_trail_map.html")
                # To keep the plot responsive
                plt.pause(0.01)

except KeyboardInterrupt:
    # Close the serial port on exit
    ser.close()

    # Final save of the map
    save_map("final_breadcrumb_trail_map.html")
    

    print("Map and 3D plot generated and serial connection closed.")

import tkinter as tk
from tkinter import Frame
from tkinterhtml import HtmlFrame
import folium
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import io
import serial

# Initialize the map
initial_latitude = 42.035
initial_longitude = -93.613
map_obj = folium.Map(location=[initial_latitude, initial_longitude], zoom_start=7)

# Data prefix to look for in the serial data
data_prefix = '$$HAR'

# List to store the breadcrumb trail (latitude and longitude) and altitude data
breadcrumb_trail = []
altitude_data = []
temperature_data = []
pressure_data = []
humidity_data = []

# Dummy data for demonstration purposes
data = {
    'temperature': [],
    'humidity': [],
    'pressure': [],
    'latitude': [],
    'longitude': []
}

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

def read_serial_data():
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
            battery = float(parsed_data[11])
            speed = float(parsed_data[5])/10
            pdop = float(parsed_data[6])/10
            heading = float(parsed_data[4])/100000

            # Add the point to the map and keep the breadcrumb trail
            #add_point_to_map(latitude, longitude, altitude)

            altitude_data.append(altitude)
            temperature_data.append(temperature)
            pressure_data.append(pressure)
            humidity_data.append(humidity)
            
            # Print the data
            print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude} meters")
            print(f"Temperature: {temperature} °C, Pressure: {pressure} hPa, Humidity: {humidity} %")
            # Save the map periodically
            #save_map("breadcrumb_trail_map.html")
            # To keep the plot responsive
            #plt.pause(0.01)
    return {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'latitude': latitude,
        'longitude': longitude
    }

def update_data():
    new_data = read_serial_data()
    for key in data:
        data[key].append(new_data[key])
        # Limit data length for demonstration purposes
        if len(data[key]) > 50:
            data[key].pop(0)

def create_map(latitude, longitude):
    m = folium.Map(location=[latitude, longitude], zoom_start=13)
    folium.Marker([latitude, longitude], popup='GPS Location').add_to(m)
    m.save('map.html')

def update_map(lat, lon):
    create_map(lat, lon)
    map_html.load_url('map.html')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Display GUI")
        
        # Create Frames
        self.map_frame = Frame(self.root)
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.graph_frame = Frame(self.root)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Embed the map
        self.map_html = HtmlFrame(self.map_frame, horizontal_scrollbar="auto")
        self.map_html.pack(fill=tk.BOTH, expand=True)
        self.update_map(0, 0)  # Default coordinates
        
        # Create graphs
        self.figure, self.ax = plt.subplots(3, 1, figsize=(5, 10))
        self.figure.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.update_graphs()
        
        # Start data update
        self.update_interval = 1000  # Update every second
        self.update_data_loop()
    
    def update_map(self):
        if data['latitude'] and data['longitude']:
            lat = data['latitude'][-1]
            lon = data['longitude'][-1]
            create_map(lat, lon)
            self.map_html.load_url('map.html')

    def update_graphs(self):
        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()
        
        # Plot Temperature
        self.ax[0].plot(data['temperature'], label='Temperature')
        self.ax[0].set_title('Temperature')
        self.ax[0].set_xlabel('Time')
        self.ax[0].set_ylabel('°C')
        self.ax[0].legend()
        
        # Plot Humidity
        self.ax[1].plot(data['humidity'], label='Humidity', color='orange')
        self.ax[1].set_title('Humidity')
        self.ax[1].set_xlabel('Time')
        self.ax[1].set_ylabel('%')
        self.ax[1].legend()
        
        # Plot Pressure
        self.ax[2].plot(data['pressure'], label='Pressure', color='green')
        self.ax[2].set_title('Pressure')
        self.ax[2].set_xlabel('Time')
        self.ax[2].set_ylabel('hPa')
        self.ax[2].legend()
        
        self.canvas.draw()
    
    def update_data_loop(self):
        update_data()
        self.update_map()
        self.update_graphs()
        self.root.after(self.update_interval, self.update_data_loop)

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
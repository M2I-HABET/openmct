from flask import Flask, render_template, jsonify
import random
import time
import serial
import serial.tools.list_ports

app = Flask(__name__)

# Initialize the map
initial_latitude = 42.035
initial_longitude = -93.613

# Data prefix to look for in the serial data
data_prefix = '$$HAR'

data = {
    'temperature': [],
    'humidity': [],
    'pressure': [],
    'latitude': [],
    'longitude': [],
    'altitude': []
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

def sim_data():
    """ Simulate reading data from a serial port. """
    return {
        'temperature': round(random.uniform(20, 30), 2),
        'humidity': round(random.uniform(30, 60), 2),
        'pressure': round(random.uniform(980, 1050), 2),
        'latitude': round(random.uniform(-90, 90), 6),
        'longitude': round(random.uniform(-180, 180), 6),
        'altitude': round(random.uniform(900, 5000), 2)  # Added altitude
    }

def read_serial_data():
    """ Read serial data from the connected device """
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
    return {
        'temperature': temperature,
        'altitude': altitude,
        'humidity': humidity,
        'pressure': pressure,
        'latitude': latitude,
        'longitude': longitude
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    #new_data = read_serial_data()
    new_data = sim_data()
    for key in data:
        data[key].append(new_data[key])
        # Limit data length for demonstration purposes
        if len(data[key]) > 50:
            data[key].pop(0)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False)
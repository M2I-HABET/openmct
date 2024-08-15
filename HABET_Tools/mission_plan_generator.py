import json
from datetime import datetime

def get_unix_timestamp(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        unix_timestamp = int(dt.timestamp() * 1000)  # Convert to Unix timestamp in milliseconds
        return unix_timestamp
    except ValueError:
        print("Error: Incorrect date/time format. Please use the format 'YYYY-MM-DD HH:MM:SS'.")
        return None

def get_time_input(activity_name, phase_name):
    while True:
        print(f"\nEnter details for activity '{activity_name}' in phase '{phase_name}':")
        
        start_time_str = input("Enter the start time (YYYY-MM-DD HH:MM:SS): ")
        start = get_unix_timestamp(start_time_str)
        if start is None:
            continue
        
        end_time_str = input("Enter the end time (YYYY-MM-DD HH:MM:SS): ")
        end = get_unix_timestamp(end_time_str)
        if end is None:
            continue
        
        if end <= start:
            print("Error: End time must be after start time.")
            continue
        
        return start, end

def create_plan():
    # Predefined structure based on the provided example
    phases = {
        "Flight Planning Phase": [
            {"name": "FRR", "type": "Flight Planning", "color": "green", "textColor": "white"},
            {"name": "PIR", "type": "Flight Planning", "color": "green", "textColor": "white"},
            {"name": "ERR", "type": "Flight Planning", "color": "green", "textColor": "white"},
            {"name": "LRR", "type": "Flight Planning", "color": "green", "textColor": "white"}
        ],
        "Launch Phase": [
            {"name": "Launch Debrief", "type": "Launch", "color": "orange", "textColor": "white"},
            {"name": "Launch Site Prep", "type": "Launch", "color": "orange", "textColor": "white"},
            {"name": "Spacecraft Power On", "type": "Launch", "color": "orange", "textColor": "white"},
            {"name": "Roll Call for Fill", "type": "Launch", "color": "orange", "textColor": "white"},
            {"name": "Balloon Fill", "type": "Launch", "color": "orange", "textColor": "white"},
            {"name": "Spacecraft Tests and Checks", "type": "Launch", "color": "orange", "textColor": "white"},
            {"name": "Roll Call for Launch", "type": "Launch", "color": "orange", "textColor": "white"},
            {"name": "Launch!", "type": "Launch", "color": "orange", "textColor": "white"}
        ],
        "Flight Phase": [
            {"name": "Ascent", "type": "Flight", "color": "blue", "textColor": "white"},
            {"name": "Burst", "type": "Flight", "color": "blue", "textColor": "white"},
            {"name": "Descent", "type": "Flight", "color": "blue", "textColor": "white"},
            {"name": "Landing", "type": "Flight", "color": "blue", "textColor": "white"},
            {"name": "Recovery", "type": "Flight", "color": "blue", "textColor": "white"}
        ]
    }

    plan = {}

    for phase_name, activities in phases.items():
        plan[phase_name] = []
        for activity in activities:
            start, end = get_time_input(activity['name'], phase_name)
            activity_entry = {
                "name": activity['name'],
                "start": start,
                "end": end,
                "type": activity['type'],
                "color": activity['color'],
                "textColor": activity['textColor']
            }
            plan[phase_name].append(activity_entry)

    return plan

def save_plan_to_json(plan):
    file_name = input("Enter the name of the output JSON file (without extension): ") + ".json"
    with open(file_name, 'w') as json_file:
        json.dump(plan, json_file, indent=4)
    print(f"\nPlan saved to {file_name}")

def main():
    print("OpenMCT Mission Plan Generator")
    print("=============================\n")
    
    plan = create_plan()
    save_plan_to_json(plan)

if __name__ == "__main__":
    main()

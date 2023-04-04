from dronekit import connect, Command
from pymavlink import mavutil
import time

def execute_mission(custom_latitude, custom_longitude):
    # Connect to the vehicle
    connection_string = "tcp:23.105.171.72:14550"
    print(f"Connecting to vehicle on: {connection_string}")
    vehicle = connect(connection_string, wait_ready=True, timeout=90)
    print('gets here')

    # Clear the current mission
    vehicle.commands.clear()
    vehicle.flush()

    # Home waypoint
    home = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    vehicle.commands.add(home)

    # Waypoint 1
    waypoint1_lat = custom_latitude
    waypoint1_lon = custom_longitude
    waypoint1_alt = 3
    waypoint1 = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, waypoint1_lat, waypoint1_lon, waypoint1_alt)
    vehicle.commands.add(waypoint1)

    # Loiter at an altitude of 3 for 20 seconds
    loiter_alt = 3
    loiter_time = 20
    loiter = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME, 0, 0, loiter_time, 0, 0, 0, waypoint1_lat, waypoint1_lon, loiter_alt)
    vehicle.commands.add(loiter)

    # Waypoint 1 with original altitude
    waypoint1_original_alt = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, waypoint1_lat, waypoint1_lon, waypoint1_alt)
    vehicle.commands.add(waypoint1_original_alt)

    # Return to Launch (RTL)
    rtl = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    vehicle.commands.add(rtl)

    # Upload the mission
    vehicle.commands.upload()

    print(f"Uploaded mission with {vehicle.commands.count} waypoint(s)")

    # Wait for the mission to be uploaded
    timeout = 30  # Timeout in seconds
    start_time = time.time()
    expected_command_count = 4  # Update this to the expected number of waypoints
    while vehicle.commands.count != expected_command_count and (time.time() - start_time) < timeout:
        print("Uploading mission...")
        time.sleep(1)

    if vehicle.commands.count == expected_command_count:
        print("Mission uploaded successfully!")
    else:
        print("Mission upload timed out!")

    # Close the vehicle object
    vehicle.close()

def lambda_handler(event, context):
    custom_latitude = event['latitude']
    custom_longitude = event['longitude']
    execute_mission(custom_latitude, custom_longitude)
    return {
        'statusCode': 200,
        'body': 'Mission executed successfully!',
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Origin': 'origin',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'POST',
            'Content-Type': 'application/json'
        }
    }

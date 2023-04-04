from dronekit import connect, Command
from pymavlink import mavutil
import time

def execute_mission():
    # Connect to the vehicle
    connection_string = "tcp:23.105.171.72:14550"
    print(f"Connecting to vehicle on: {connection_string}")
    vehicle = connect(connection_string, wait_ready=True, timeout=90)

    # Define the waypoint coordinates
    waypoint_lat = 40.499348
    waypoint_lon = -74.448927
    waypoint_alt = 10

    # Clear the current mission
    vehicle.commands.clear()
    vehicle.flush()

    # Add home location as the first waypoint (the autopilot will set the actual home location)
    home = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    vehicle.commands.add(home)

    # Add the desired waypoint
    waypoint = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, waypoint_lat, waypoint_lon, waypoint_alt)
    vehicle.commands.add(waypoint)
    waypoint = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, 40.504807, -74.460163, waypoint_alt)
    vehicle.commands.add(waypoint)

    # Upload the mission
    vehicle.commands.upload()

    print(f"Uploaded mission with {vehicle.commands.count} waypoint(s)")

    # Wait for the mission to be uploaded
    timeout = 30  # Timeout in seconds
    start_time = time.time()
    while vehicle.commands.count != 2 and (time.time() - start_time) < timeout:
        print("Uploading mission...")
        time.sleep(1)

    if vehicle.commands.count == 2:
        print("Mission uploaded successfully!")
    else:
        print("Mission upload timed out!")

    # Close the vehicle object
    vehicle.close()

def lambda_handler(event, context):
    execute_mission()
    return {
        'statusCode': 200,
        'body': 'Mission executed successfully!'
    }

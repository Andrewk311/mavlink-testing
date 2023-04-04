from dronekit import connect, Command, LocationGlobalRelative
from pymavlink import mavutil
import time

# Connect to the drone
print("Connecting to drone...")
vehicle = connect('tcp:23.105.171.72:14550', wait_ready=True, source_system=200, timeout=60)
print("Connected to drone (system %u component %u)" % (vehicle.system, vehicle.components))

# Set a waypoint with desired coordinates
latitude = 40.499348
longitude = -74.448927
altitude = 10

# Create a new waypoint
waypoint = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0, latitude, longitude, altitude)

# Clear any existing missions and upload the new mission
vehicle.commands.clear()
vehicle.commands.add(waypoint)
vehicle.commands.upload()

print("Mission uploaded")

# Disconnect from the drone
vehicle.close()

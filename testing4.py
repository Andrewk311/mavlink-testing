from pymavlink import mavutil

# Establish a MAVLink connection
the_connection = mavutil.mavlink_connection('tcp:23.105.171.72:14550')

# Wait for the first heartbeat 
the_connection.wait_heartbeat()

# Create a MAVLink instance
mav = mavutil.mavlink.MAVLink(the_connection)

# Send a command to the drone to switch to guided mode
mav.command_long_send(
    1,                          # autopilot system id
    1,                          # autopilot component id
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,  # command
    0,                          # confirmation
    4,                          # custom mode (GUIDED)
    0, 0, 0, 0, 0, 0, 0)       # parameters

# Wait for the mode switch to complete
the_connection.wait_heartbeat()

# Send a waypoint to the drone
mav.mission_item_send(
    1,                      # autopilot system id
    1,                      # autopilot component id
    0,                      # waypoint sequence
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,   # coordinate frame
    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,   # waypoint command
    0,                      # current (not used)
    0,                      # autocontinue (not used)
    0,                      # unused parameter (param1)
    0,                      # unused parameter (param2)
    0,                      # unused parameter (param3)
    0,                      # unused parameter (param4)
    20.279588,              # latitude of the waypoint
    -75.473507,             # longitude of the waypoint
    10)                     # altitude of the waypoint (meters)
from pymavlink import mavutil

# Establish a MAVLink connection
the_connection = mavutil.mavlink_connection('tcp:23.105.171.72:14550')

# Wait for the first heartbeat 
the_connection.wait_heartbeat()

# Create a MAVLink instance
mav = mavutil.mavlink.MAVLink(the_connection)

# Create a MAVLink mission message
msg = the_connection.mav.command_long_encode(
    0,              # target system
    0,              # target component
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,  # command
    0,              # confirmation
    4,              # custom mode (GUIDED)
    0,              # param2
    0,              # param3
    0,              # param4
    0,              # param5
    0,              # param6
    0)              # param7

# Pack the message using the MAVLink instance
packed_msg = msg.pack(mav)

# Send the packed message to the drone
the_connection.write(packed_msg)
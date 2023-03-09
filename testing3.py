from pymavlink import mavutil

# Establish a MAVLink connection
the_connection = mavutil.mavlink_connection('tcp:23.105.171.72:14550')

# Wait for the first heartbeat
the_connection.wait_heartbeat()

# Listen for MAVLink messages
while True:
    try:
        # Wait for a message from the drone
        msg = the_connection.recv_msg()

        # Print the message to the console
        if msg is not None:
            print(msg)

    except KeyboardInterrupt:
        # Exit the loop if the user presses Ctrl-C
        break
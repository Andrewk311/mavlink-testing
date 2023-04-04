from pymavlink import mavutil
import time

def send_mission_count(mavcon, count):
    mavcon.mav.mission_count_send(mavcon.target_system, mavcon.target_component, count)

def clear_mission(mavcon):
    mavcon.mav.mission_clear_all_send(mavcon.target_system, mavcon.target_component)

def request_mission_item(mavcon, seq):
    mavcon.mav.mission_request_send(mavcon.target_system, mavcon.target_component, seq)

def send_mission_item(mavcon, lat, lon, alt, seq=0):
    frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT
    command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
    current = 0
    autocontinue = 1
    param1 = 0
    param2 = 0
    param3 = 0
    param4 = 0

    lat_int = int(lat * 1e7)
    lon_int = int(lon * 1e7)

    mavcon.mav.mission_item_send(mavcon.target_system, mavcon.target_component, seq, frame, command, current, autocontinue, param1, param2, param3, param4, lat_int, lon_int, alt)

the_connection = mavutil.mavlink_connection('tcp:23.105.171.72:14550', source_system=200)
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
# Request all parameters
the_connection.mav.param_request_list_send(the_connection.target_system, the_connection.target_component)

# Clear any existing waypoints
clear_mission(the_connection)


# Print received parameters
while True:
    param = the_connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=1)
    if param is not None:
        print("Received param: %s = %f" % (param.param_id, param.param_value))
    else:
        break


# Set a waypoint with desired coordinates
latitude = 40.499348
longitude = -74.448927
altitude = 10

# Send mission count (1 waypoint)
send_mission_count(the_connection, 1)

# Wait for MISSION_REQUEST from the autopilot
timeout = time.time() + 10  # Set a 10-second timeout
while True:
    if time.time() > timeout:
        print("Timeout waiting for MISSION_REQUEST")
        break

    msg = the_connection.recv_match(type=['MISSION_REQUEST'], blocking=True, timeout=1)
    if msg is not None:
        seq = msg.seq
        print("Received MISSION_REQUEST for item %u" % seq)

        # Send the waypoint
        send_mission_item(the_connection, latitude, longitude, altitude, seq)
        time.sleep(1)
        # Wait for MISSION_ACK
        while True:
            ack = the_connection.recv_match(type=['MISSION_ACK'], blocking=True, timeout=1)
            if ack is not None:
                if ack.type == mavutil.mavlink.MAV_MISSION_ACCEPTED:
                    print("Mission upload complete")

                    print("Requesting uploaded mission item...")
                    request_mission_item(the_connection, seq)

                    # Wait for MISSION_ITEM message
                    timeout = time.time() + 10  # Set a 10-second timeout
                    while True:
                        if time.time() > timeout:
                            print("Timeout waiting for MISSION_ITEM")
                            break

                        msg = the_connection.recv_match(type=['MISSION_ITEM'], blocking=True, timeout=1)
                        if msg is not None:
                            print("Received MISSION_ITEM:")
                            print("  seq: %u" % msg.seq)
                            print("  lat: %f" % (msg.x / 1e7))
                            print("  lon: %f" % (msg.y / 1e7))
                            print("  alt: %f" % msg.z)
                            break


                    break
                else:
                    print("Mission upload failed")
                    break
            else:
                break
        break

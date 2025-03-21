import time
import rtde_control
import rtde_receive
import numpy as np
import argparse

# Import our custom modules
import robot_control
import stl_reader

def main():
    print("Code initiation")
    time.sleep(0.3)
    print("Connecting to arm")
    
    # Simple variables for controlling and receiving information from arm
    rtde_c = rtde_control.RTDEControlInterface("192.168.56.101")
    rtde_r = rtde_receive.RTDEReceiveInterface("192.168.56.101")
    
    # Define acceleration and velocity variables used for control
    acc = 0.2  # m/s2
    vel = 0.2  # m/s
    
    # Define dimensions of object being printed
    length = 0.300  # units are in METERS!!!
    width = length
    time.sleep(0.3)

    print("Connected to Arm")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Control UR16 robot to trace shapes')
    parser.add_argument('--stl', type=str, help='Path to STL file (optional)')
    parser.add_argument('--mode', type=str, default='house', 
                        choices=['house', 'stl_full', 'stl_contour'],
                        help='Operating mode: house, stl_full, or stl_contour')
    parser.add_argument('--scale', type=float, default=0.001,
                        help='Scale factor for STL vertices (default 0.001 for mm to m)')
    parser.add_argument('--z_offset', type=float, default=0.01,
                        help='Z-offset to add to all movements (default: 0.01m)')
    args = parser.parse_args()
    
    # Move to home position
    print("Sending Home")
    robot_control.home(rtde_c, 0.5, 0.5)
    
    # Move to origin
    print("Moving to part origin")
    robot_control.origin(rtde_c, rtde_r, acc, vel)
    
    # Execute the selected mode
    if args.mode == 'house':
        robot_control.house(rtde_r, rtde_c, acc, vel, width, length)
    elif args.mode == 'stl_full' and args.stl:
        # Pass the scale factor to the execute_stl_path function
        robot_control.execute_stl_path(rtde_r, rtde_c, args.stl, acc, vel, 
                                      z_offset=args.z_offset, scale_factor=args.scale)
    elif args.mode == 'stl_contour' and args.stl:
        # Pass the scale factor to the trace_stl_contour function
        robot_control.trace_stl_contour(rtde_r, rtde_c, args.stl, acc, vel, 
                                       z_offset=args.z_offset, scale_factor=args.scale)
    else:
        if args.mode != 'house' and not args.stl:
            print("Error: STL file path required for stl_full or stl_contour modes")
        else:
            print(f"Unknown mode: {args.mode}")
    
    # Disconnect from the robot
    rtde_c.disconnect()
    if not rtde_c.isConnected():
        print("Disconnected")

    print("Goodbye")
            
if __name__ == "__main__":
    main()

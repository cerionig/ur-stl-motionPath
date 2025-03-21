# this code will connect to the UR16 (IP: 172.16.3.115), home the arm to a designated position, move slightly off home, and return to home
# used to test connection and motion

import time
import ur
import numpy as np

def deg2rad(deg):
    return deg*np.pi/180

def home(robot, acc, vel):
    home = (deg2rad(180), deg2rad(-90), deg2rad(-90), deg2rad(-180), deg2rad(-90), deg2rad(0))
    robot.moveJ(home,acc,vel)


def generate_circle_points(center, radius, num_points, z_height):
    """
    Generate points along a circular path in the XY plane.
    
    Args:
        center (list): [x, y] coordinates of circle center
        radius (float): radius of the circle in meters
        num_points (int): number of points to generate along the circle
        z_height (float): constant Z height for the circle
        
    Returns:
        list: List of [x, y, z] points along the circle
    """
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append([x, y, z_height])
    return points    

def main():
    connected = False
    tries = 0
    maxTries = 5

    print("hello")

    while not connected and tries < maxTries:
        try:
            time.sleep(0.3)
            #robot = urx.Robot("172.16.3.115")
            rtde_c = rtde_control.RTDEControlInterface("yyy.yyy.yyy.yyy")

            time.sleep(0.3)
            connected = True
        except:
            tries += 1
            print(f"Connection attempt {tries} failed.")
            time.sleep(1) # Wait for a second before next attempt
        if connected:
            print("connected to Arm")
            print("sending Home")
            home(rtde_c,0.5,0.5)
            print("Home")
            print('moving arm')
            rtde_r = rtde_receive.RTDEReceiveInterface("yyy.yyy.yyy.yyy")
            linearPosition = rtde_r.getActualTCPPose()
            print(linearPosition)
            linearPosition[1] += 0.100
            rtde_c.moveL(linearPosition, 0.01, 0.01)
            home(rtde_c,0.5,0.5)
            rtde_c.moveC()
            rtde_c.disconnect()
            if( not rtde_c.isConnected()):
                print("disconnected")

            print("Goodbye")
        else:
            print("Connection failed, check robot status.")

if __name__ == "__main__":
    main()

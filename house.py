import time
import rtde_control
import rtde_receive
import numpy as np
import matplotlib.pyplot as plt

def deg2rad(deg):
    return deg*np.pi/180

def cosd(a):
    return np.cos(deg2rad(a))

def sind(a):
    return np.sin(deg2rad(a)) 

def home(robot, acc, vel):
    home = (deg2rad(180), deg2rad(-90), deg2rad(-90), deg2rad(-180), deg2rad(-90), deg2rad(0))
    robot.moveJ(home,acc,vel)


def house(rtde_r, rtde_c, acc, vel, width, length):

    # main hoiuse outline
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX = [] 
    savedPoseY = []
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[2] += 0.200 # units are in meters 
    linearPosition[0] -= 0.5*width
    linearPosition[1] -= 0.25*length
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[0] += 0.33333333*width
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[1] += 0.25*length
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[0] += 0.3333*width
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[1] -= 0.25*length
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[0] += 0.3333*width
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[1] += 0.5*length
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[0] -= 0.5*width
    linearPosition[1] += 0.5*length
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[0] += 0.5*width
    linearPosition[1] -= 0.5*length
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[1] -= 0.5*length

    # circle window
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[2] -= 0.200 # units are in meters
    linearPosition[0] += 0.5*width
    linearPosition[1] += 0.75*length
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[1] += 0.333*width
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    linearPosition[2] += 0.200 # units are in meters
    rtde_c.moveL(linearPosition, acc, vel)
    linearPosition = rtde_r.getActualTCPPose()
    savedPoseX.append(linearPosition[0])
    savedPoseY.append(linearPosition[1])
    #variables for circle
    r = 0.33333*width 
    dtheta = 10
    theta = 0
    poses = []
    x0 = linearPosition[0]
    y0 = linearPosition[1]
    z0 = linearPosition[2]
    rx = linearPosition[3]
    ry = linearPosition[4]
    rz = linearPosition[5]
    while theta <= 360:
        x = x0 + r * cosd(theta)
        y = y0 + r * sind(theta)
        z = z0
        poses.append([x,y,z,rx,ry,rz])
        theta += dtheta
    for x in poses:
        rtde_c.moveL(x,acc,vel)
        print(x)
    linearPosition = rtde_r.getActualTCPPose()
    linearPosition[2] -= 0.200 # units are in meters
    rtde_c.moveL(linearPosition, acc, vel)

def main():

    print("hello")
    
        
    time.sleep(0.3)
    rtde_c = rtde_control.RTDEControlInterface("192.168.56.101")

    time.sleep(0.3)

    print("connected to Arm")
    print("sending Home")
    home(rtde_c,0.5,0.5)
    print("Home")
    print('moving arm')
    rtde_r = rtde_receive.RTDEReceiveInterface("192.168.56.101")
    
    acc = 0.2 # m/s2
    vel = 0.2 # m/s
    length = 0.300 #units are in METERS!!! 
    width = length / 2

    #house(rtde_r, rtde_c, acc, vel, width, length)
    rtde_c.disconnect()
    if( not rtde_c.isConnected()):
        print("disconnected")

    print("Goodbye")
       
            
if __name__ == "__main__":
    main()

import time
import numpy as np
import stl_reader

def deg2rad(deg):
    """Convert degrees to radians"""
    return deg * np.pi / 180

def cosd(a):
    """Cosine of angle in degrees"""
    return np.cos(deg2rad(a))

def sind(a):
    """Sine of angle in degrees"""
    return np.sin(deg2rad(a)) 

def move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=0.05):
    """
    Move the robot to a safe height above its current position.
    
    Args:
        rtde_c: RTDE Control interface
        rtde_r: RTDE Receive interface
        acc (float): Acceleration for the movement
        vel (float): Velocity for the movement
        height_offset (float): How much to lift in meters
    """
    # Get current position
    current_pose = rtde_r.getActualTCPPose()
    
    # Create a safe position (same XY, higher Z)
    safe_pose = current_pose.copy()
    safe_pose[2] += height_offset
    
    # Move to safe height
    print(f"Moving to safe height: {safe_pose[2]:.4f}m (+{height_offset:.2f}m)")
    rtde_c.moveL(safe_pose, acc, vel)
    time.sleep(0.5)  # Small delay for stability
    
    return safe_pose


def home(rtde_c, rtde_r, acc, vel):
    """
    Move robot to home position with safety movement.
    
    Args:
        rtde_c: RTDE Control interface
        rtde_r: RTDE Receive interface
        acc (float): Acceleration for the movement
        vel (float): Velocity for the movement
    """
    safe_pose = move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=0.05)
    
    # Now move to home position
    home_pose = (deg2rad(180), deg2rad(-45), deg2rad(-135), deg2rad(-180), deg2rad(-90), deg2rad(0))
    print("Moving to home position")
    rtde_c.moveJ(home_pose, acc, vel)
    print("Home position reached")
    time.sleep(1)  # Delay between moves to catch any errors

def origin(rtde_c, rtde_r, acc, vel):
    """
    Move robot to the origin position with safety movements.
    
    Args:
        rtde_c: RTDE Control interface
        rtde_r: RTDE Receive interface
        acc (float): Acceleration for the movement
        vel (float): Velocity for the movement
    """
    # First move to a safe height
    safe_pose = move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=0.1)
    
    # Calculate the target position (10cm in X from current position)
    target_pose = safe_pose.copy()
    target_pose[0] -= 0.100  # Subtract 10cm from X position
    
    # Move horizontally at the safe height
    print(f"Moving horizontally to X position: {target_pose[0]:.4f}m")
    rtde_c.moveL(target_pose, acc, vel)
    time.sleep(0.5)
    
    # Now move down to the original Z-height
    target_pose[2] -= 0.1  # Return to original height
    print(f"Lowering to operating height: {target_pose[2]:.4f}m")
    rtde_c.moveL(target_pose, acc, vel)
    
    print("At origin position")
    time.sleep(1)  # Delay between moves to catch any errors

def house(rtde_r, rtde_c, acc, vel, width, length):
    """
    Move robot in a house-shaped pattern with safety movements.
    
    Args:
        rtde_r: RTDE Receive interface
        rtde_c: RTDE Control interface
        acc (float): Acceleration for movements
        vel (float): Velocity for movements
        width (float): Width of the house
        length (float): Length of the house
    """
    # First move to a safe height
    safe_pose = move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=0.05)
    
    # Lower to start position
    start_pose = safe_pose.copy()
    start_pose[2] -= 0.05  # Return to original height
    rtde_c.moveL(start_pose, acc, vel)
    time.sleep(0.5)
    
    # Main house outline
    print("Beginning object path")
    
    # Move 1
    linear_position = rtde_r.getActualTCPPose()
    linear_position[1] += 0.25 * width
    rtde_c.moveL(linear_position, acc, vel)

    # Move 2
    linear_position = rtde_r.getActualTCPPose()
    linear_position[0] -= 0.25 * length
    rtde_c.moveL(linear_position, acc, vel)

    # Move 3
    linear_position = rtde_r.getActualTCPPose()
    linear_position[1] += 0.25 * width
    rtde_c.moveL(linear_position, acc, vel)

    # Move 4
    linear_position = rtde_r.getActualTCPPose()
    linear_position[0] += 0.25 * width
    rtde_c.moveL(linear_position, acc, vel)

    # Move 5
    linear_position = rtde_r.getActualTCPPose()
    linear_position[1] += 0.25 * width
    rtde_c.moveL(linear_position, acc, vel)

    # Move 6
    linear_position = rtde_r.getActualTCPPose()
    linear_position[0] -= 0.5 * length
    rtde_c.moveL(linear_position, acc, vel)

    # Move 7
    linear_position = rtde_r.getActualTCPPose()
    linear_position[0] -= 0.5 * length
    linear_position[1] -= 0.5 * length
    rtde_c.moveL(linear_position, acc, vel)

    # Move 8
    linear_position = rtde_r.getActualTCPPose()
    linear_position[0] += 0.5 * length
    linear_position[1] -= 0.5 * length
    rtde_c.moveL(linear_position, acc, vel)

    # Move 9
    linear_position = rtde_r.getActualTCPPose()
    linear_position[0] += 0.5 * length
    rtde_c.moveL(linear_position, acc, vel)
    
    # Move back up to safe height when done
    move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=0.05)

def execute_stl_path(rtde_r, rtde_c, stl_path, acc, vel, z_offset=0.01, scale_factor=1, safety_height=0.05):
    """
    Execute a path derived from an STL file with safety movements.
    
    Args:
        rtde_r: RTDE Receive interface
        rtde_c: RTDE Control interface
        stl_path (str): Path to the STL file
        acc (float): Acceleration for robot movements
        vel (float): Velocity for robot movements
        z_offset (float): Z-offset to add to all movements (for clearance)
        scale_factor (float): Scale factor to apply to the STL vertices
        safety_height (float): Height to lift between operations for safety
    """
    # Get the current position as the reference
    current_pose = rtde_r.getActualTCPPose()
    reference_x = current_pose[0]
    reference_y = current_pose[1]
    reference_z = current_pose[2]
    
    # Read and process the STL file
    print(f"Reading STL file: {stl_path}")
    vertices = stl_reader.read_stl_file(stl_path)
    print(f"Read {len(vertices)} vertices from STL file")
    
    # Remove duplicates
    vertices = stl_reader.remove_duplicate_vertices(vertices)
    print(f"After removing duplicates: {len(vertices)} vertices")
    
    # Apply scaling - EXPLICITLY and ONLY here
    vertices = stl_reader.scale_vertices(vertices, scale_factor)
    print(f"Scaled vertices by factor {scale_factor}")
    
    # Align to bottom-left corner instead of centering
    vertices = stl_reader.align_to_bottom_left(vertices)
    print("Aligned to bottom-left corner as origin")
    
    # Find the min/max z after scaling and alignment
    min_z = min(z for _, _, z in vertices)
    max_z = max(z for _, _, z in vertices)
    z_range = max_z - min_z
    print(f"Z range after scaling: {min_z:.4f} to {max_z:.4f}, total range: {z_range:.4f}")
    
    # Create a single path (middle of z-range)
    z_height = min_z + z_range / 2
    layer_vertices = stl_reader.get_layer_vertices(vertices, z_height)
    
    if not layer_vertices:
        print("No vertices found at the selected Z-height. Trying a different approach...")
        # Try a different approach - just pick a middle range
        vertices.sort(key=lambda v: v[2])  # Sort by z-coordinate
        mid_index = len(vertices) // 2
        z_height = vertices[mid_index][2]
        layer_vertices = stl_reader.get_layer_vertices(vertices, z_height, tolerance=z_range/4)
    
    if not layer_vertices:
        print("No valid path found in the STL file.")
        return
    
    # Sort into a continuous path
    path = stl_reader.sort_vertices_by_path(layer_vertices)
    print(f"Created path with {len(path)} points at z={z_height:.4f}m")
    
    # First, move to a safe height
    safe_pose = move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=safety_height)
    time.sleep(0.5)
    
    # Move to a position above the starting point
    if path:
        approach_pose = safe_pose.copy()
        approach_pose[0] = reference_x + path[0][0]
        approach_pose[1] = reference_y + path[0][1]
        
        print(f"Moving to position above start point: ({approach_pose[0]:.4f}, {approach_pose[1]:.4f}, {approach_pose[2]:.4f})")
        rtde_c.moveL(approach_pose, acc, vel)
        time.sleep(0.5)
        
        # Now lower to the starting Z height
        start_pose = approach_pose.copy()
        start_pose[2] = reference_z + path[0][2] + z_offset
        
        print(f"Lowering to start point: ({start_pose[0]:.4f}, {start_pose[1]:.4f}, {start_pose[2]:.4f})")
        rtde_c.moveL(start_pose, acc, vel)
        time.sleep(0.5)
        
        # Execute the path
        for i, (x, y, z) in enumerate(path):
            target_pose = current_pose.copy()
            target_pose[0] = reference_x + x
            target_pose[1] = reference_y + y
            target_pose[2] = reference_z + z + z_offset
            
            # Print every 10th point to avoid console spam
            if i % 1 == 0:
                print(f"Moving to point {i+1}/{len(path)}: ({x:.4f}, {y:.4f}, {z:.4f})")
            
            rtde_c.moveL(target_pose, acc, vel)
            # Small delay for very intricate paths
            time.sleep(0.1)
    
    # Return to safe height when done
    move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=safety_height)

    # Return home when done
    home(rtde_c, rtde_r, acc, vel)

def trace_stl_contour(rtde_r, rtde_c, stl_path, acc, vel, z_offset=0.01, scale_factor=1, safety_height=0.05):
    """
    Trace only the outer contour of an STL file with safety movements.
    
    Args:
        rtde_r: RTDE Receive interface
        rtde_c: RTDE Control interface
        stl_path (str): Path to the STL file
        acc (float): Acceleration for robot movements
        vel (float): Velocity for robot movements
        z_offset (float): Z-offset to add to all movements (for clearance)
        scale_factor (float): Scale factor to apply to the STL vertices
        safety_height (float): Height to lift between operations for safety
    """
    # Get the current position as the reference
    current_pose = rtde_r.getActualTCPPose()
    reference_x = current_pose[0]
    reference_y = current_pose[1]
    reference_z = current_pose[2]
    
    # Read and process the STL file
    print(f"Reading STL file: {stl_path}")
    vertices = stl_reader.read_stl_file(stl_path)
    print(f"Read {len(vertices)} vertices from STL file")
    
    # Remove duplicates
    vertices = stl_reader.remove_duplicate_vertices(vertices)
    print(f"After removing duplicates: {len(vertices)} vertices")
    
    # Apply scaling - EXPLICITLY and ONLY here
    vertices = stl_reader.scale_vertices(vertices, scale_factor)
    print(f"Scaled vertices by factor {scale_factor}")
    
    # Align to bottom-left corner instead of centering
    vertices = stl_reader.align_to_bottom_left(vertices)
    print("Aligned to bottom-left corner as origin")
    
    # Get the contour vertices (outer shape)
    contour_vertices = stl_reader.extract_contour_vertices(vertices)
    contour_vertices = stl_reader.sort_vertices_by_path(contour_vertices)
    
    if not contour_vertices:
        print("No contour vertices found in the STL file.")
        return
    
    print(f"Extracted contour with {len(contour_vertices)} points")
    
    # First, move to a safe height
    safe_pose = move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=safety_height)
    time.sleep(0.5)
    
    # Move to a position above the starting point
    approach_pose = safe_pose.copy()
    approach_pose[0] = reference_x + contour_vertices[0][0]
    approach_pose[1] = reference_y + contour_vertices[0][1]
    
    print(f"Moving to position above start point: ({approach_pose[0]:.4f}, {approach_pose[1]:.4f}, {approach_pose[2]:.4f})")
    rtde_c.moveL(approach_pose, acc, vel)
    time.sleep(0.5)
    
    # Now lower to the starting Z height
    start_pose = approach_pose.copy()
    start_pose[2] = reference_z + contour_vertices[0][2] + z_offset
    
    print(f"Lowering to start point: ({start_pose[0]:.4f}, {start_pose[1]:.4f}, {start_pose[2]:.4f})")
    rtde_c.moveL(start_pose, acc, vel)
    time.sleep(0.5)
    
    # Execute the contour path
    for i, (x, y, z) in enumerate(contour_vertices):
        target_pose = current_pose.copy()
        target_pose[0] = reference_x + x
        target_pose[1] = reference_y + y
        target_pose[2] = reference_z + z + z_offset
        
        if i % 5 == 0:
            print(f"Moving to contour point {i+1}/{len(contour_vertices)}: ({x:.4f}, {y:.4f}, {z:.4f})")
        
        rtde_c.moveL(target_pose, acc, vel)
        # Small delay for stability
        time.sleep(0.1)
    
    # Close the loop by returning to the first point
    if len(contour_vertices) > 1:
        target_pose = current_pose.copy()
        target_pose[0] = reference_x + contour_vertices[0][0]
        target_pose[1] = reference_y + contour_vertices[0][1]
        target_pose[2] = reference_z + contour_vertices[0][2] + z_offset
        rtde_c.moveL(target_pose, acc, vel)
    
    # Return to safe height when done
    move_to_safe_height(rtde_c, rtde_r, acc, vel, height_offset=safety_height)

    # Return home when done
    home(rtde_c, rtde_r, acc, vel)

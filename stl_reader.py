import struct
import os
import numpy as np
import argparse
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull

def read_stl_file(file_path):
    """
    Read an STL file and return the list of vertices.
    Automatically detects whether the file is ASCII or binary.
    
    Args:
        file_path (str): Path to the STL file
        
    Returns:
        list: List of vertices (each vertex is a tuple of x, y, z coordinates)
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Try to determine if the file is ASCII or binary
    with open(file_path, 'rb') as f:
        header = f.read(5).decode('utf-8', errors='ignore')
        
    # If the file starts with "solid", it's probably ASCII
    if header.lower().startswith('solid'):
        try:
            return read_ascii_stl(file_path)
        except Exception as e:
            print(f"Failed to parse as ASCII STL: {e}. Trying binary format.")
            return read_binary_stl(file_path)
    else:
        return read_binary_stl(file_path)

def read_ascii_stl(file_path):
    """
    Read an ASCII STL file and return the list of vertices.
    
    Args:
        file_path (str): Path to the ASCII STL file
        
    Returns:
        list: List of vertices (each vertex is a tuple of x, y, z coordinates)
    """
    vertices = []
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('vertex'):
                # Extract x, y, z coordinates from the line
                parts = line.split()
                if len(parts) >= 4:  # 'vertex' + 3 coordinates
                    try:
                        x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                        vertices.append((x, y, z))
                    except ValueError:
                        continue
    
    return vertices

def read_binary_stl(file_path):
    """
    Read a binary STL file and return the list of vertices.
    
    Args:
        file_path (str): Path to the binary STL file
        
    Returns:
        list: List of vertices (each vertex is a tuple of x, y, z coordinates)
    """
    vertices = []
    triangles = 0
    
    with open(file_path, 'rb') as f:
        # Skip the header (80 bytes) and read the number of triangles (4 bytes)
        f.seek(80)
        num_triangles = struct.unpack('<I', f.read(4))[0]
        triangles = num_triangles
        
        # For each triangle, read 12 floats (3 for normal, 9 for vertices) and 2 unused bytes
        for _ in range(num_triangles):
            # Skip normal vector (3 floats, 12 bytes)
            f.read(12)
            
            # Read the 3 vertices of the triangle (9 floats, 36 bytes)
            for _ in range(3):
                data = f.read(12)  # Each vertex is 3 floats (x, y, z) and each float is 4 bytes
                x, y, z = struct.unpack('<fff', data)
                vertices.append((x, y, z))
            
            # Skip the attribute byte count (2 bytes)
            f.read(2)
    
    print(f"Read {triangles} triangles from binary STL file")
    return vertices

def remove_duplicate_vertices(vertices, tolerance=1e-6):
    """
    Remove duplicate vertices within a certain tolerance.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        tolerance (float): Tolerance for considering vertices as duplicates
        
    Returns:
        list: List of unique vertices
    """
    unique_vertices = []
    for vertex in vertices:
        # Check if this vertex is close to any already in the unique list
        is_duplicate = False
        for unique_vertex in unique_vertices:
            distance = np.sqrt(sum((a - b) ** 2 for a, b in zip(vertex, unique_vertex)))
            if distance < tolerance:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_vertices.append(vertex)
    
    return unique_vertices

def scale_vertices(vertices, scale_factor=1.0):
    """
    Scale vertices by a given factor.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        scale_factor (float): Scale factor to apply
        
    Returns:
        list: Scaled vertices
    """
    print(f"Scaling vertices by factor {scale_factor}")
    return [(x * scale_factor, y * scale_factor, z * scale_factor) for x, y, z in vertices]

def align_to_bottom_left(vertices, z_keep_min=True):
    """
    Align vertices so that the bottom-left corner is at the origin.
    "Bottom left" means minimum X and minimum Y.
    For Z, we can keep it at the minimum or preserve its position relative to XY plane.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        z_keep_min (bool): If True, move Z minimum to 0. If False, preserve Z positions.
        
    Returns:
        list: Aligned vertices
    """
    if not vertices:
        return []
    
    # Find the minimum x, y, and z coordinates
    min_x = min(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    min_z = min(v[2] for v in vertices) if z_keep_min else 0
    
    print(f"Aligning to bottom-left corner: ({min_x:.4f}, {min_y:.4f}, {min_z:.4f})")
    
    # Shift vertices so bottom-left corner is at (0,0,0) or (0,0,min_z)
    return [(x - min_x, y - min_y, z - min_z if z_keep_min else z) for x, y, z in vertices]

def center_vertices(vertices):
    """
    Center vertices around the origin.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        
    Returns:
        list: Centered vertices
    """
    # Find the center point
    x_sum = sum(v[0] for v in vertices)
    y_sum = sum(v[1] for v in vertices)
    z_sum = sum(v[2] for v in vertices)
    center_x = x_sum / len(vertices)
    center_y = y_sum / len(vertices)
    center_z = z_sum / len(vertices)
    
    # Center the vertices
    return [(x - center_x, y - center_y, z - center_z) for x, y, z in vertices]

def extract_contour_vertices(vertices):
    """
    Extract the contour vertices (outer shape) from a set of vertices.
    Uses 2D convex hull on the XY projection.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        
    Returns:
        list: List of vertices forming the contour
    """
    # Project to 2D (XY plane)
    points_2d = np.array([(x, y) for x, y, z in vertices])
    
    # Compute the convex hull
    hull = ConvexHull(points_2d)
    
    # Extract the vertices on the hull
    contour_indices = hull.vertices
    
    # Create the result, including the z-coordinate (using the average z at each xy point)
    contour_vertices = []
    for i in contour_indices:
        x, y = points_2d[i]
        # Find z values at this xy point
        z_values = [vertices[j][2] for j in range(len(vertices)) 
                   if abs(vertices[j][0] - x) < 1e-6 and abs(vertices[j][1] - y) < 1e-6]
        
        # Use average z
        avg_z = sum(z_values) / len(z_values) if z_values else 0
        contour_vertices.append((x, y, avg_z))
    
    return contour_vertices

def get_layer_vertices(vertices, z_height, tolerance=0.1):
    """
    Extract vertices at a specific Z height within tolerance.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        z_height (float): The Z height to extract
        tolerance (float): Tolerance for z-height
        
    Returns:
        list: List of vertices at the specified z-height
    """
    layer_vertices = []
    for x, y, z in vertices:
        if abs(z - z_height) <= tolerance:
            layer_vertices.append((x, y, z))
    
    return layer_vertices

def sort_vertices_by_path(vertices):
    """
    Sort vertices to create a continuous path.
    Uses a nearest-neighbor approach.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        
    Returns:
        list: Sorted vertices
    """
    if not vertices:
        return []
    
    remaining = vertices.copy()
    path = [remaining.pop(0)]
    
    while remaining:
        current = path[-1]
        # Find nearest unvisited vertex
        distances = [np.sqrt((x - current[0])**2 + (y - current[1])**2 + (z - current[2])**2) 
                    for x, y, z in remaining]
        nearest_idx = np.argmin(distances)
        path.append(remaining.pop(nearest_idx))
    
    return path

def stl_to_robot_path(vertices, z_slices=1):
    """
    Process vertices and convert to a robot path.
    Note: This version accepts preprocessed vertices (already scaled)
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        z_slices (int): Number of z-slices to create
        
    Returns:
        list: List of paths, where each path is a list of vertices
    """    
    # Find min/max z
    min_z = min(z for _, _, z in vertices)
    max_z = max(z for _, _, z in vertices)
    z_range = max_z - min_z
    
    print(f"Z range: {min_z:.4f} to {max_z:.4f}, total range: {z_range:.4f}")
    
    # Create paths for different z heights
    paths = []
    for i in range(z_slices):
        if z_slices == 1:
            # For single slice, use middle height
            z_height = min_z + z_range / 2
        else:
            z_height = min_z + (z_range * i / max(1, z_slices - 1))
        
        # Get vertices at this layer
        layer_vertices = get_layer_vertices(vertices, z_height)
        
        if layer_vertices:
            # Sort into a continuous path
            path = sort_vertices_by_path(layer_vertices)
            paths.append(path)
            print(f"Created path for z={z_height:.4f} with {len(path)} points")
    
    return paths

def get_stl_info(vertices):
    """
    Get comprehensive information about the vertices.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        
    Returns:
        dict: Dictionary containing information about the vertices
    """
    # Calculate bounding box
    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)
    min_z = min(v[2] for v in vertices)
    max_z = max(v[2] for v in vertices)
    
    # Calculate dimensions
    width = max_x - min_x
    depth = max_y - min_y
    height = max_z - min_z
    
    # Get unique vertices (approximation)
    unique_vertices = remove_duplicate_vertices(vertices)
    
    return {
        "total_vertices": len(vertices),
        "unique_vertices": len(unique_vertices),
        "triangles": len(vertices) // 3,
        "dimensions": {
            "width": width,
            "depth": depth,
            "height": height,
            "units": "model units (original)"
        },
        "bounding_box": {
            "min_x": min_x,
            "max_x": max_x,
            "min_y": min_y,
            "max_y": max_y,
            "min_z": min_z,
            "max_z": max_z
        }
    }

def export_vertices_to_file(vertices, output_file):
    """
    Export vertices to a text file.
    
    Args:
        vertices (list): List of vertices
        output_file (str): Path to the output file
    """
    with open(output_file, 'w') as f:
        for i, (x, y, z) in enumerate(vertices):
            f.write(f"Vertex {i+1}: {x}, {y}, {z}\n")
    
    print(f"Exported {len(vertices)} vertices to {output_file}")

def visualize_vertices(vertices, title="STL Visualization"):
    """
    Visualize the vertices in 3D.
    
    Args:
        vertices (list): List of vertices (each vertex is a tuple of x, y, z coordinates)
        title (str): Title for the plot
    """
    if not vertices:
        print("No vertices to visualize.")
        return
        
    # Convert vertices to numpy arrays for plotting
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]
    
    # Calculate bounding box
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)
    min_z, max_z = min(z), max(z)
    dimensions = f"Width: {max_x-min_x:.4f}, Depth: {max_y-min_y:.4f}, Height: {max_z-min_z:.4f}"
    
    # Create the 3D plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the vertices
    ax.scatter(x, y, z, c='b', marker='o', s=10, alpha=0.5)
    
    # Plot the bottom-left corner
    ax.scatter([min_x], [min_y], [min_z], c='r', marker='o', s=100)
    ax.text(min_x, min_y, min_z, "Origin", color='red')
    
    # Add bounding box dimensions to title
    title = f"{title}\n{dimensions}"
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    
    # Force equal aspect ratio
    max_range = max(max_x-min_x, max_y-min_y, max_z-min_z)
    mid_x = (max_x + min_x) / 2
    mid_y = (max_y + min_y) / 2
    mid_z = (max_z + min_z) / 2
    ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
    ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
    ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

def main():
    """
    Main function for standalone execution.
    """
    parser = argparse.ArgumentParser(description='STL File Reader and Processor')
    parser.add_argument('file', help='Path to the STL file')
    parser.add_argument('--info', action='store_true', help='Show information about the STL file')
    parser.add_argument('--export', type=str, help='Export vertices to a text file')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale factor to apply to vertices')
    parser.add_argument('--slice', type=int, default=1, help='Number of z-slices to create')
    parser.add_argument('--visualize', action='store_true', help='Visualize the STL file')
    parser.add_argument('--contour', action='store_true', help='Extract and show contour only')
    parser.add_argument('--bottom-left-origin', action='store_true', 
                        help='Align to bottom-left corner as origin (default is centered)')
    
    args = parser.parse_args()
    
    try:
        # Read the STL file
        vertices = read_stl_file(args.file)
        print(f"Successfully read STL file: {args.file}")
        print(f"Total vertices: {len(vertices)}")
        
        # Show original information if requested
        if args.info:
            print("\nOriginal STL File Information:")
            info = get_stl_info(vertices)
            print(json.dumps(info, indent=2))
        
        # Apply scale factor (only once)
        if args.scale != 1.0:
            vertices = scale_vertices(vertices, args.scale)
            
            # Show scaled information if requested
            if args.info:
                print("\nScaled STL File Information:")
                info = get_stl_info(vertices)
                print(json.dumps(info, indent=2))
        
        # Apply alignment if requested
        if args.bottom_left_origin:
            vertices = align_to_bottom_left(vertices)
            if args.info:
                print("\nAligned STL File Information:")
                info = get_stl_info(vertices)
                print(json.dumps(info, indent=2))
        
        # Extract contour if requested
        processed_vertices = vertices
        if args.contour:
            processed_vertices = extract_contour_vertices(vertices)
            print(f"Extracted contour with {len(processed_vertices)} vertices")
        
        # Process for slices if requested
        if args.slice > 1:
            paths = stl_to_robot_path(processed_vertices, args.slice)
            print(f"Created {len(paths)} paths for robot movement")
            
            # For visualization, flatten paths
            if args.visualize and paths:
                flattened_path = [vertex for path in paths for vertex in path]
                if flattened_path:
                    title = f"STL Path Visualization: {os.path.basename(args.file)}"
                    if args.contour:
                        title += " (Contour Only)"
                    if args.scale != 1.0:
                        title += f" (Scaled by {args.scale})"
                    if args.bottom_left_origin:
                        title += " (Bottom-Left Origin)"
                    
                    visualize_vertices(flattened_path, title)
        else:
            # Export if requested
            if args.export:
                export_vertices_to_file(processed_vertices, args.export)
            
            # Visualize if requested
            if args.visualize:
                title = f"STL Visualization: {os.path.basename(args.file)}"
                if args.contour:
                    title += " (Contour Only)"
                if args.scale != 1.0:
                    title += f" (Scaled by {args.scale})"
                if args.bottom_left_origin:
                    title += " (Bottom-Left Origin)"
                
                visualize_vertices(processed_vertices, title)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()

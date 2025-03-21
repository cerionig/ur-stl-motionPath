# UR-stl-motionPath
software to convert STL files into motion paths for UR robots
# UR16 STL Path Tracing System

A robust system for converting 3D STL models into robot movement paths for Universal Robots (UR) arms, with a focus on safety and precision.

![UR16 Robot Path Tracing](https://placeholder-for-robot-image.com)

## Overview

This system allows Universal Robots (particularly the UR16 model) to trace paths derived from STL files. The code provides options for tracing complete paths or just the outline contours of 3D models, with built-in safety movements and a bottom-left origin approach for consistent positioning.

## Features

- Read both binary and ASCII STL files
- Visualize STL models before robot execution
- Scale models appropriately (mm to m conversion)
- Use bottom-left corner as origin for predictable positioning
- Built-in safety movements (lifting for clearance during transitions)
- Options for full path or contour-only tracing
- Comprehensive visualization tools

## Dependencies

- Python 3.6 or higher
- NumPy
- SciPy
- Matplotlib
- rtde_control
- rtde_receive

## Installation

1. Ensure Python 3.6+ is installed on your system
   ```bash
   python --version
   ```

2. Install required Python packages:
   ```bash
   pip install numpy scipy matplotlib
   pip install rtde_control rtde_receive
   ```

3. Clone or download this repository to your local machine

4. Update the robot IP address in `play.py` (around line 17-18) to match your UR robot:
   ```python
   rtde_c = rtde_control.RTDEControlInterface("192.168.56.101")  # Change to your robot's IP
   rtde_r = rtde_receive.RTDEReceiveInterface("192.168.56.101")  # Change to your robot's IP
   ```

## File Structure

- `play.py` - Main script for executing robot movements
- `robot_control.py` - Functions for controlling the robot
- `stl_reader.py` - Functions for reading and processing STL files

## Usage

### Visualizing STL Files (Before Robot Execution)

It's recommended to visualize your STL file first to ensure it looks as expected:

```bash
python stl_reader.py your_model.stl --visualize --scale 0.001 --bottom-left-origin
```

This will show a 3D visualization of your model with the bottom-left origin point highlighted in red.

### Running the Robot

#### Testing with a Simple House Pattern

```bash
python play.py --mode house
```

#### Tracing a Full STL Path

```bash
python play.py --mode stl_full --stl your_model.stl --scale 0.001
```

#### Tracing Just the Contour (Outline)

```bash
python play.py --mode stl_contour --stl your_model.stl --scale 0.001
```

### Command-Line Options

The following options are available when running `play.py`:

| Option          | Description                                           | Default    |
|-----------------|-------------------------------------------------------|------------|
| `--stl`         | Path to STL file                                      | None       |
| `--mode`        | Mode: 'house', 'stl_full', or 'stl_contour'           | 'house'    |
| `--scale`       | Scale factor for STL model (mm to m = 0.001)          | 0.001      |
| `--z_offset`    | Z-offset in meters for clearance above surface        | 0.01       |
| `--safety_height`| Height to lift for safety movements (m)              | 0.05       |

The `stl_reader.py` script also accepts these options:

| Option               | Description                                      |
|----------------------|--------------------------------------------------|
| `--info`             | Show information about the STL file              |
| `--export FILENAME`  | Export vertices to a text file                   |
| `--scale FACTOR`     | Scale factor to apply                            |
| `--slice NUMBER`     | Number of z-slices to create                     |
| `--visualize`        | Show 3D visualization                            |
| `--contour`          | Extract and show contour only                    |
| `--bottom-left-origin` | Align to bottom-left corner as origin          |

## Understanding Scale Factors

STL files typically use different units than the robot:

- Most STL files use **millimeters** → use `--scale 0.001`
- STL files in centimeters → use `--scale 0.01`
- STL files in inches → use `--scale 0.0254`
- STL files already in meters → use `--scale 1.0`

If you're unsure, use this command to check your model's dimensions:
```bash
python stl_reader.py your_model.stl --info
```

## Safety Considerations

- Always ensure the robot's workspace is clear before operation
- Start with slow speeds until you're familiar with the system
- Keep the emergency stop accessible at all times
- The system includes safety lifts between movements, but always monitor the robot

## Examples

### Example 1: Visualize and trace a simple STL file

```bash
# First visualize
python stl_reader.py simple_shape.stl --visualize --scale 0.001 --bottom-left-origin

# Then trace the contour
python play.py --mode stl_contour --stl simple_shape.stl --scale 0.001
```

### Example 2: Trace with custom safety parameters

```bash
python play.py --mode stl_full --stl detailed_model.stl --scale 0.001 --z_offset 0.005 --safety_height 0.08
```

## Troubleshooting

### Connection Issues
- Verify the robot IP address is correct in `play.py`
- Ensure your computer and robot are on the same network
- Check that the robot is powered on and operational

### Movement Issues
- If movements are too small/large, adjust the `--scale` parameter
- If the robot reaches protective stops, your model may be too large or positioned outside the workspace
- Use the visualization tool first to verify the model looks as expected

### STL File Issues
- If you get "No valid path found", your STL file may not have suitable geometry for tracing
- Try using `--mode stl_contour` instead of `stl_full` for complex models
- Ensure your STL file is properly formed (watertight, no errors)

## Advanced Usage

### Getting STL File Information

```bash
python stl_reader.py your_model.stl --info
```

### Exporting Processed Vertices

```bash
python stl_reader.py your_model.stl --scale 0.001 --bottom-left-origin --export processed_points.txt
```

### Processing Multiple Layers

```bash
python stl_reader.py your_model.stl --slice 5 --visualize
```

## License

[Insert License Information Here]

## Acknowledgments

- Universal Robots for their RTDE interface
- Contributors to NumPy, SciPy, and Matplotlib
- All contributors to this project
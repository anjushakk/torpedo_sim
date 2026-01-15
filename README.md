Here is the complete project documentation formatted as a `README.md` file. You can save this as `README.md` in the root of your repository.

```markdown
# Torpedo Simulation Project (ROS 2 + Gazebo)

**Project Overview**
This project simulates the Tethys LRAUV (Long Range Autonomous Underwater Vehicle) using **Gazebo** for physics/hydrodynamics and **ROS 2** for control and visualization. The system uses a bridge to communicate between the simulation (Ignition/Gazebo) and the ROS 2 ecosystem.

---

## 1. Setup & Installation
Ensure you are in the root of your workspace (`~/new_ws`) before running these commands.

### Build the Workspace
Every time you modify C++ code or change configuration files, rebuild the project:
```bash
cd ~/new_ws
colcon build
source install/setup.bash

```

---

## 2. Launching the Simulation

### Step 1: Start the Backend (Gazebo + Bridge)

This command launches the Gazebo physics engine, loads the `underwater_world`, spawns the `tethys` torpedo, and automatically starts the `ros_gz_bridge` to link topics.

```bash
# Terminal 1
source install/setup.bash
ros2 launch torpedo_sim sim.launch.py

```

### Step 2: Start Visualization (RViz)

This launches RViz2 and the `robot_state_publisher` to visualize the robot's structure, transforms, and sensor data in real-time.

```bash
# Terminal 2
source install/setup.bash
ros2 launch torpedo_sim viz.launch.py

```

* **Note:** In RViz, ensure the **Fixed Frame** is set to `tethys/base_link` and add the **RobotModel** display.

---

## 3. Controlling the Robot

You can control the torpedo using a Python script or C++ node.

### Option A: Python Teleop (Recommended)

Run the script directly using Python 3.

```bash
# Terminal 3
source install/setup.bash
python3 src/torpedo_sim/scripts/teleop_node.py

```

### Option B: C++ Teleop (If Compiled)

If you have compiled the C++ node in `CMakeLists.txt`:

```bash
# Terminal 3
source install/setup.bash
ros2 run torpedo_sim teleop_node

```

**Controls:**
| Key | Action |
| :--- | :--- |
| **W / S** | Increase / Decrease Propeller Thrust |
| **UP / DOWN** | Pitch Fins (Dive / Surface) |
| **LEFT / RIGHT** | Yaw Fins (Turn Left / Right) |
| **SPACE** | Emergency Stop (Zero all commands) |

---

## 4. Debugging & Manual Verification

If the robot is not moving, use these commands to verify the system is working.

### Check System Status

Verify that nodes and topics are active:

```bash
ros2 node list
ros2 topic list

```

### Manual Topic Publishing

Force the robot to move by sending raw commands directly to the bridge.

**Test 1: Spin Propeller (Move Forward)**

```bash
ros2 topic pub /model/tethys/joint/propeller_joint/cmd_pos std_msgs/msg/Float64 "data: 10.0"

```

**Test 2: Lock Vertical Fins (Turn Circle)**

```bash
ros2 topic pub /tethys/vertical_fins std_msgs/msg/Float64 "data: 0.5"

```

```

```

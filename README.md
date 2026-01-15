

# **Torpedo Simulation Project (ROS 2 + Gazebo)**

**Overview:** This project simulates the Tethys LRAUV (Long Range Autonomous Underwater Vehicle) using Gazebo for physics and ROS 2 for control, connected via a bridge.

### **1. Setup & Build**

Every time you modify code or open a new terminal, ensure the workspace is built and sourced.

```bash
cd ~/new_ws
colcon build
source install/setup.bash

```

### **2. Launching the Simulation**

This command starts the Gazebo physics engine, loads the `underwater_world`, spawns the `tethys` model, and activates the `ros_gz_bridge`.

```bash
# Terminal 1
ros2 launch torpedo_sim sim.launch.py

```

### **3. Launching Visualization**

This starts RViz2 and the `robot_state_publisher` to visualize the robot's structure and sensor data.

```bash
# Terminal 2
source install/setup.bash
ros2 launch torpedo_sim viz.launch.py

```

*Note: In RViz, set Fixed Frame to `tethys/base_link` and add the "RobotModel" display.*

### **4. Running the Controller**

Use the keyboard to drive the torpedo.

**Option A: Python Teleop (Recommended)**

```bash
# Terminal 3
source install/setup.bash
python3 src/torpedo_sim/scripts/teleop_node.py

```


**Controls:**

* **W / S:** Increase / Decrease Thrust (Propeller)
* **UP / DOWN:** Pitch Up / Down (Horizontal Fins)
* **LEFT / RIGHT:** Yaw Left / Right (Vertical Fins)
* **SPACE:** Stop All Motion

### **5. Debugging & Verification**

If the robot does not move, use these commands to force specific actions and check connections.

**Check Active Topics:**

```bash
ros2 topic list
# You should see: /tethys/vertical_fins, /joint_states

```

**Manual Movement Test:**

```bash
# Spin Propeller (Thrust)
ros2 topic pub /model/tethys/joint/propeller_joint/cmd_pos std_msgs/msg/Float64 "data: 10.0"

# Rotate Vertical Fins (Steering)
ros2 topic pub /tethys/vertical_fins std_msgs/msg/Float64 "data: 0.5"

```

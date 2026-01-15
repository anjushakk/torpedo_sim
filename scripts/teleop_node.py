#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import sys, select, termios, tty

msg = """
Control Your Torpedo!
---------------------------
w/s : Increase/Decrease Propeller (Angle)
a/d : Steer Left/Right (Vertical Fins)
Up/Down Arrow : Pitch Up/Down (Horizontal Fins)

IMPORTANT: If using 'cmd_pos', the propeller will only 
turn to an angle, not spin continuously!
---------------------------
CTRL-C to quit
"""

class TorpedoTeleop(Node):
    def __init__(self):
        super().__init__('torpedo_teleop')
        
        # Verify these match exactly with 'ros2 topic list'
        # Try removing the leading slash if 'Waiting for matching subscriptions' appears
        self.prop_pub = self.create_publisher(Float64, '/model/tethys/joint/propeller_joint/cmd_pos', 10)
        self.h_fin_pub = self.create_publisher(Float64, '/tethys/horizontal_fins', 10)
        self.v_fin_pub = self.create_publisher(Float64, '/tethys/vertical_fins', 10)
        
        self.prop_val = 0.0
        self.h_val = 0.0
        self.v_val = 0.0

    def publish_cmds(self):
        self.prop_pub.publish(Float64(data=self.prop_val))
        self.h_fin_pub.publish(Float64(data=self.h_val))
        self.v_fin_pub.publish(Float64(data=self.v_val))
        sys.stdout.write(f"\rProp: {self.prop_val:.1f} | H-Fin: {self.h_val:.2f} | V-Fin: {self.v_val:.2f}   ")
        sys.stdout.flush()

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = TorpedoTeleop()
    print(msg)

    try:
        while rclpy.ok():
            key = get_key(settings)
            
            if key == 'w':
                node.prop_val -= 0.1 # Smaller increments for better control
            elif key == 's':
                node.prop_val += 0.1
            elif key == 'a':
                node.v_val = min(0.26, node.v_val + 0.02) # Added limits based on your SDF
            elif key == 'd':
                node.v_val = max(-0.26, node.v_val - 0.02)
            elif key == '\x1b': # Arrow key escape sequence
                key2 = get_key(settings)
                key3 = get_key(settings)
                if key3 == 'A': # Up
                    node.h_val = min(0.26, node.h_val + 0.02)
                elif key3 == 'B': # Down
                    node.h_val = max(-0.26, node.h_val - 0.02)
            elif key == '\x03': # Ctrl-C
                break
            
            if key != '':
                node.publish_cmds()

    except Exception as e:
        print(f"\nTeleop Error: {e}")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import sys
import termios
import tty
import select
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

# --- SETTINGS ---
THRUST_STEP = 50.0   # Increase thrust by 50 per click
FIN_STEP = 0.1       # Turn fins by 0.1 rad (~5 degrees)
MAX_FIN_ANGLE = 0.6  # Limit fins to ~35 degrees

INSTRUCTIONS = """
---------------------------------------
TETHYS TELEOP CONTROLLER
---------------------------------------
    W
  A   D    (Steer with Vertical Fins)
    S

I / K  : Pitch Up / Down (Horizontal Fins)
SPACE  : Emergency Stop (All Zero)

CTRL-C to quit
---------------------------------------
"""

class TethysTeleop(Node):
    def __init__(self):
        super().__init__('tethys_teleop_node')
        
        # 1. Initialize Publishers (Using your CLEAN topics)
        self.pub_thrust = self.create_publisher(Float64, '/model/tethys/joint/propeller_joint/cmd_thrust', 10)
        self.pub_v_fin = self.create_publisher(Float64, '/tethys/vertical_fins', 10)
        self.pub_h_fin = self.create_publisher(Float64, '/tethys/horizontal_fins', 10)

        # 2. State Variables
        self.thrust = 0.0
        self.v_fin = 0.0
        self.h_fin = 0.0
        
        self.settings = termios.tcgetattr(sys.stdin)

    def get_key(self):
        """Reads a single keypress without waiting for Enter"""
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def publish_state(self):
        """Publishes the current state to all topics"""
        # Create messages
        t_msg = Float64(); t_msg.data = self.thrust
        v_msg = Float64(); v_msg.data = self.v_fin
        h_msg = Float64(); h_msg.data = self.h_fin

        # Publish
        self.pub_thrust.publish(t_msg)
        self.pub_v_fin.publish(v_msg)
        self.pub_h_fin.publish(h_msg)

        # Update terminal UI
        print(f"\rThrust: {self.thrust:.1f} | Vert: {self.v_fin:.2f} | Horiz: {self.h_fin:.2f}   ", end='')

    def run(self):
        print(INSTRUCTIONS)
        try:
            while True:
                key = self.get_key()
                
                if key == 'w':
                    self.thrust += THRUST_STEP
                elif key == 's':
                    self.thrust -= THRUST_STEP
                elif key == 'a':
                    self.v_fin = min(self.v_fin + FIN_STEP, MAX_FIN_ANGLE)
                elif key == 'd':
                    self.v_fin = max(self.v_fin - FIN_STEP, -MAX_FIN_ANGLE)
                elif key == 'i':
                    self.h_fin = max(self.h_fin - FIN_STEP, -MAX_FIN_ANGLE)
                elif key == 'k':
                    self.h_fin = min(self.h_fin + FIN_STEP, MAX_FIN_ANGLE)
                elif key == ' ':
                    self.thrust = 0.0
                    self.v_fin = 0.0
                    self.h_fin = 0.0
                elif key == '\x03': # CTRL-C
                    break

                # Only publish if a key was pressed or just to keep alive
                if key != '':
                    self.publish_state()

        except Exception as e:
            print(e)

        finally:
            # STOP ROBOT ON EXIT
            self.thrust = 0.0
            self.v_fin = 0.0
            self.h_fin = 0.0
            self.publish_state()
            print("\n\nStopping robot and exiting...")
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

def main(args=None):
    rclpy.init(args=args)
    node = TethysTeleop()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()



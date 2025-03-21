import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/gcerioni/ws_ur16/install/ros2_controllers_test_nodes'

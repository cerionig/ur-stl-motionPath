ros2 action send_goal /joint_trajectory_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
  trajectory: {
    joint_names: ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'],
    points: [
      { 
        positions: [0.0, 0.0, 0.0, 0.2, 0.0, 0.0],
        time_from_start: { sec: 2, nanosec: 0 }
      }
    ]
  }
}"

ros2 action send_goal /joint_trajectory_controller/follow_joint_trajectory control_msgs/action/FollowJointTrajectory "{
  trajectory: {
    joint_names: ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'],
    points: [
      { 
        positions: [0.0, 1.75, 0.0, 0.2, 0.0, 0.0],
        time_from_start: { sec: 2, nanosec: 0 }
      }
    ]
  }
}"
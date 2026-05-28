---
name: ROS Message Types
description: |
  Use this skill when the user asks about ROS message types, message fields, sensor_msgs, geometry_msgs,
  std_msgs, nav_msgs, or needs to understand how to work with specific message structures like
  sensor_msgs/Imu, geometry_msgs/Twist, nav_msgs/Odometry, etc.

  Trigger examples:
  - "What fields are in sensor_msgs/Imu?"
  - "How do I publish a Twist message?"
  - "What's the difference between Pose and PoseStamped?"
  - "Show me the Odometry message structure"
  - "What units does IMU use?"
version: 1.0.0
---

# ROS Message Types Reference

This skill provides comprehensive information about ROS message types commonly used in robotics applications.

## Quick Message Lookup

Use these commands to inspect any message type:

```bash
# Show message structure
rosmsg show sensor_msgs/Imu

# List all messages in a package
rosmsg package sensor_msgs

# Find messages by name pattern
rosmsg list | grep -i imu
```

---

## sensor_msgs - Sensor Data Messages

### sensor_msgs/Imu

IMU (Inertial Measurement Unit) data.

```
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
geometry_msgs/Quaternion orientation
  float64 x, y, z, w
float64[9] orientation_covariance
geometry_msgs/Vector3 angular_velocity
  float64 x, y, z
float64[9] angular_velocity_covariance
geometry_msgs/Vector3 linear_acceleration
  float64 x, y, z
float64[9] linear_acceleration_covariance
```

**Units:**
- angular_velocity: rad/s
- linear_acceleration: m/s^2
- orientation: quaternion (unitless)

**Covariance:** Row-major 3x3 matrix. Set first element to -1 if data not available.

**Example - Publishing IMU:**
```python
from sensor_msgs.msg import Imu
msg = Imu()
msg.header.stamp = rospy.Time.now()
msg.header.frame_id = "imu_link"
msg.linear_acceleration.z = 9.81  # gravity
msg.angular_velocity.x = 0.0
# Set covariance[0] = -1 if orientation not provided
msg.orientation_covariance[0] = -1
```

### sensor_msgs/LaserScan

2D LIDAR scan data.

```
std_msgs/Header header
float32 angle_min        # start angle [rad]
float32 angle_max        # end angle [rad]
float32 angle_increment  # angular step [rad]
float32 time_increment   # time between measurements [s]
float32 scan_time        # time for full scan [s]
float32 range_min        # minimum range [m]
float32 range_max        # maximum range [m]
float32[] ranges         # range data [m]
float32[] intensities    # intensity data (optional)
```

### sensor_msgs/Image

Camera image data.

```
std_msgs/Header header
uint32 height            # image height (rows)
uint32 width             # image width (columns)
string encoding          # pixel encoding (rgb8, bgr8, mono8, etc.)
uint8 is_bigendian       # endianness
uint32 step              # row length in bytes
uint8[] data             # actual image data
```

**Common encodings:** `rgb8`, `bgr8`, `rgba8`, `mono8`, `mono16`, `32FC1`

### sensor_msgs/PointCloud2

3D point cloud data.

```
std_msgs/Header header
uint32 height
uint32 width
sensor_msgs/PointField[] fields
bool is_bigendian
uint32 point_step        # bytes per point
uint32 row_step          # bytes per row
uint8[] data
bool is_dense            # true if no invalid points
```

### sensor_msgs/NavSatFix

GPS/GNSS data.

```
std_msgs/Header header
sensor_msgs/NavSatStatus status
float64 latitude         # degrees
float64 longitude        # degrees
float64 altitude         # meters above ellipsoid
float64[9] position_covariance
uint8 position_covariance_type
```

### sensor_msgs/JointState

Robot joint state.

```
std_msgs/Header header
string[] name            # joint names
float64[] position       # radians or meters
float64[] velocity       # rad/s or m/s
float64[] effort         # Nm or N
```

---

## geometry_msgs - Geometric Primitives

### geometry_msgs/Twist

Velocity in free space (linear + angular).

```
geometry_msgs/Vector3 linear
  float64 x, y, z        # m/s
geometry_msgs/Vector3 angular
  float64 x, y, z        # rad/s
```

**Usage:** Robot velocity commands, typically on `/cmd_vel`.

**Example - Sending velocity command:**
```python
from geometry_msgs.msg import Twist
cmd = Twist()
cmd.linear.x = 0.5   # forward 0.5 m/s
cmd.angular.z = 0.1  # rotate 0.1 rad/s
pub.publish(cmd)
```

### geometry_msgs/Pose

Position + orientation in 3D.

```
geometry_msgs/Point position
  float64 x, y, z        # meters
geometry_msgs/Quaternion orientation
  float64 x, y, z, w     # quaternion
```

### geometry_msgs/PoseStamped

Pose with header (timestamped and framed).

```
std_msgs/Header header
geometry_msgs/Pose pose
```

### geometry_msgs/Transform

Coordinate frame transformation.

```
geometry_msgs/Vector3 translation
  float64 x, y, z        # meters
geometry_msgs/Quaternion rotation
  float64 x, y, z, w     # quaternion
```

### geometry_msgs/TransformStamped

Stamped transform with parent/child frames.

```
std_msgs/Header header
string child_frame_id
geometry_msgs/Transform transform
```

### geometry_msgs/Wrench

Force/torque in free space.

```
geometry_msgs/Vector3 force
  float64 x, y, z        # Newtons
geometry_msgs/Vector3 torque
  float64 x, y, z        # Newton-meters
```

---

## nav_msgs - Navigation Messages

### nav_msgs/Odometry

Robot odometry (pose + velocity estimate).

```
std_msgs/Header header
string child_frame_id
geometry_msgs/PoseWithCovariance pose
  geometry_msgs/Pose pose
  float64[36] covariance   # 6x6 pose covariance
geometry_msgs/TwistWithCovariance twist
  geometry_msgs/Twist twist
  float64[36] covariance   # 6x6 velocity covariance
```

### nav_msgs/Path

Planned path (sequence of poses).

```
std_msgs/Header header
geometry_msgs/PoseStamped[] poses
```

### nav_msgs/OccupancyGrid

2D occupancy map.

```
std_msgs/Header header
nav_msgs/MapMetaData info
  time map_load_time
  float32 resolution      # meters/cell
  uint32 width, height    # cells
  geometry_msgs/Pose origin
int8[] data              # occupancy: 0=free, 100=occupied, -1=unknown
```

---

## std_msgs - Standard Primitives

### std_msgs/Header

Standard message header.

```
uint32 seq               # sequence ID
time stamp               # timestamp
string frame_id          # coordinate frame
```

### Common Types

| Type | Description |
|------|-------------|
| Bool | true/false |
| Int8, Int16, Int32, Int64 | Signed integers |
| UInt8, UInt16, UInt32, UInt64 | Unsigned integers |
| Float32, Float64 | Floating point |
| String | UTF-8 string |
| Time | ROS time (secs + nsecs) |
| Duration | ROS duration |
| Empty | Empty message (for triggers) |

---

## Unit Conventions

| Quantity | Unit | Notes |
|----------|------|-------|
| Linear distance | meters | Always SI |
| Angular distance | radians | Not degrees |
| Linear velocity | m/s | |
| Angular velocity | rad/s | |
| Linear acceleration | m/s^2 | |
| Force | Newtons (N) | |
| Torque | Newton-meters (Nm) | |
| Time | seconds.nanoseconds | ROS Time format |
| Temperature | Kelvin or Celsius | Depends on message |

---

## Covariance Matrices

Many messages include covariance as a flat array:
- 6x6 matrices (pose): 36 elements, row-major
- 3x3 matrices (3D vector): 9 elements, row-major

Index mapping for 3x3:
```
[0  1  2 ]   [xx xy xz]
[3  4  5 ] = [yx yy yz]
[6  7  8 ]   [zx zy zz]
```

**Unknown covariance:** Set all to 0
**Data not available:** Set [0] to -1

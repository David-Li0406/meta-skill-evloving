---
name: ROS Troubleshooting
description: |
  Use this skill when the user encounters ROS errors, issues, or unexpected behavior.
  Covers common error messages, diagnostic approaches, and proven solutions for
  roscore issues, topic problems, build errors, network issues, and more.

  Trigger examples:
  - "Unable to communicate with master"
  - "Topic not found"
  - "Node crashed"
  - "Transform error"
  - "Build failed"
  - "roswtf shows warnings"
  - "Message type mismatch"
version: 1.0.0
---

# ROS Troubleshooting Guide

Quick reference for diagnosing and fixing common ROS issues.

## Quick Diagnostics

```bash
# Source environment

# Run diagnostics
roswtf

# Check environment
env | grep ROS

# Check master
rostopic list

# Check nodes
rosnode list
rosnode ping /node_name
```

---

## Error: Unable to Communicate with Master

**Message:**
```
ERROR: Unable to communicate with master!
```

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| roscore not running | Start `roscore` or use `roslaunch` |
| Wrong ROS_MASTER_URI | `export ROS_MASTER_URI=http://localhost:11311` |
| Firewall blocking port | Open port 11311 |
| Network unreachable | Check connectivity to master host |

**Diagnostic:**
```bash
echo $ROS_MASTER_URI
ping $(echo $ROS_MASTER_URI | sed 's|http://||' | cut -d: -f1)
```

---

## Error: Topic Not Found

**Message:**
```
ERROR: Cannot find topic /topic_name
```

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| Publisher not running | Start the publishing node |
| Wrong topic name | Check `rostopic list` for correct name |
| Namespace issue | Use full topic path `/namespace/topic` |
| Remapping problem | Check launch file remappings |

**Diagnostic:**
```bash
rostopic list | grep -i keyword
rosnode list
rosnode info /suspected_publisher
```

---

## Error: Message Type Mismatch

**Message:**
```
ERROR: Message type 'X' does not match type 'Y'
```

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| Different message versions | Rebuild all packages |
| Wrong message type in code | Fix code to use correct type |
| Stale rosbag | Re-record with current messages |

**Diagnostic:**
```bash
rostopic type /topic_name
rosmsg show $(rostopic type /topic_name)
```

---

## Error: Transform Errors

**Messages:**
```
Lookup would require extrapolation into the future
Could not find transform from X to Y
```

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| TF publisher not running | Start TF broadcaster |
| Clock skew | Sync system clocks (NTP) |
| Missing static transform | Add static_transform_publisher |
| Too slow TF rate | Increase TF publish rate |

**Diagnostic:**
```bash
rosrun tf tf_monitor
rosrun tf tf_echo frame1 frame2
rostopic echo /tf
```

---

## Build Errors

### "Could not find package"

```bash
# Install ROS dependencies
rosdep install --from-paths src --ignore-src -r -y

# Source ROS environment
```

### "CMake Error: Could not find..."

```bash
# Check if dependency is installed
dpkg -l | grep ros-noetic-dependency

# Install missing package
sudo apt install ros-noetic-package-name
```

### "fatal error: header.h: No such file"

```bash
# Check package.xml for missing dependencies
cat package.xml | grep depend

# Add missing dependency to CMakeLists.txt
# find_package(catkin REQUIRED COMPONENTS missing_pkg)
```

---

## Node Crashes

### Segmentation Fault

**Debug with gdb:**
```xml
<node pkg="pkg" type="node" name="node" launch-prefix="gdb -ex run --args"/>
```

```bash
# After crash, in gdb:
bt full  # Full backtrace
```

### Node Exits Immediately

**Check for:**
1. Missing parameters - Check `rosparam list`
2. Missing topics - Check `rostopic list`
3. Missing files - Check paths in code
4. Initialization errors - Check rosout

```bash
rostopic echo /rosout | grep -i error
```

---

## Network Issues (Multi-Machine)

### Nodes Can't See Each Other

```bash
# On ALL machines, set:
export ROS_MASTER_URI=http://MASTER_IP:11311
export ROS_IP=$(hostname -I | awk '{print $1}')

# Verify connectivity
rostopic list
rosnode ping /remote_node
```

### Topics Not Received

**Check:**
1. Firewall rules (allow ROS ports)
2. ROS_IP set correctly on both machines
3. Hostname resolution working

```bash
# Test direct connection
rosnode info /remote_node  # Shows URI
# Try connecting to that URI directly
```

---

## Common roswtf Warnings

### "Cannot ping node"

Node is unresponsive. Kill and restart:
```bash
rosnode kill /node_name
rosnode cleanup
```

### "Topic /X has no subscribers"

May be expected if no consumer running. Check if:
- Consumer node started
- Topic name matches (namespace, remapping)

### "Package X not found"

```bash
rospack find package_name
```

---

## Performance Issues

### High Latency

```bash
# Check message delay
rostopic delay /topic_name

# Check network bandwidth
rostopic bw /topic_name
```

**Fixes:**
- Reduce message rate
- Use compression for images
- Check network bandwidth
- Use nodelets for zero-copy

### Dropped Messages

```bash
# Check topic statistics
rostopic hz /topic_name
rostopic bw /topic_name
```

**Fixes:**
- Increase subscriber queue_size
- Reduce publisher rate
- Use TCP_NODELAY for small messages
- Check network reliability

---

## Quick Reference: ROS Environment

```bash
# Essential environment variables
echo $ROS_DISTRO        # Should be: noetic
echo $ROS_MASTER_URI    # Default: http://localhost:11311
echo $ROS_PACKAGE_PATH  # Should include your workspace
echo $ROS_IP            # Your IP (for multi-machine)

# Reset environment

# Check what's sourced
echo $CMAKE_PREFIX_PATH
```

---

## When All Else Fails

1. **Clean rebuild:**
   ```bash
   cd catkin_ws
   catkin clean -y
   catkin build
   ```

2. **Kill everything:**
   ```bash
   killall -9 rosmaster roscore rosout
   ```

3. **Check logs:**
   ```bash
   cat ~/.ros/log/latest/*.log | grep -i error
   ```

4. **Start fresh:**
   ```bash
   rosclean purge
   roscore &
   ```

5. **Check for zombie nodes:**
   ```bash
   rosnode cleanup
   ```

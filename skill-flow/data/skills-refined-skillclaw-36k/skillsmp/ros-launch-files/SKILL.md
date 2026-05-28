---
name: ROS Launch Files
description: |
  Use this skill when the user needs help writing, understanding, or modifying ROS launch files.
  Covers launch XML syntax, arguments, parameters, node configuration, includes, conditionals,
  namespaces, remapping, and common patterns.

  Trigger examples:
  - "How do I create a launch file?"
  - "Add an argument to this launch file"
  - "What does $(find pkg) do?"
  - "How do I include another launch file?"
  - "Set up conditional launching"
  - "Configure node parameters in launch"
version: 1.0.0
---

# ROS Launch Files Guide

Launch files define how to start ROS nodes, set parameters, and configure the system. They use XML format with ROS-specific tags.

## Basic Structure

```xml
<launch>
  <!-- Comments use XML syntax -->

  <!-- Arguments (input parameters) -->
  <arg name="robot_name" default="robot1" doc="Name of the robot"/>

  <!-- Parameters on parameter server -->
  <param name="global_param" value="some_value"/>

  <!-- Node definition -->
  <node pkg="package_name" type="node_executable" name="node_name" output="screen">
    <param name="~private_param" value="$(arg robot_name)"/>
    <remap from="input" to="sensor/data"/>
  </node>

  <!-- Include other launch files -->
  <include file="$(find other_pkg)/launch/other.launch">
    <arg name="arg_name" value="arg_value"/>
  </include>
</launch>
```

---

## Core Tags

### `<launch>`

Root element. All other tags must be inside.

```xml
<launch>
  <!-- content -->
</launch>
```

### `<node>`

Start a ROS node.

```xml
<node pkg="package_name"
      type="executable_name"
      name="node_name"
      output="screen"
      respawn="true"
      required="false"
      ns="namespace"
      args="--flag value"
      launch-prefix="gdb -ex run --args">
  <!-- node-specific params, remaps -->
</node>
```

| Attribute | Description |
|-----------|-------------|
| `pkg` | Package containing the node (required) |
| `type` | Executable name (required) |
| `name` | Node name in ROS graph (required) |
| `output` | `screen` (terminal) or `log` (file) |
| `respawn` | Restart if node dies |
| `required` | Shutdown launch if node dies |
| `ns` | Namespace for the node |
| `args` | Command line arguments |
| `launch-prefix` | Prefix command (gdb, valgrind, etc.) |

### `<arg>`

Define launch file arguments.

```xml
<!-- With default value -->
<arg name="robot" default="turtlebot"/>

<!-- Required (no default) -->
<arg name="config_file"/>

<!-- With documentation -->
<arg name="rate" default="10" doc="Publishing rate in Hz"/>

<!-- Usage -->
<param name="robot_name" value="$(arg robot)"/>
```

**Passing arguments:**
```bash
roslaunch pkg file.launch robot:=my_robot rate:=20
```

### `<param>`

Set parameter on parameter server.

```xml
<!-- Direct value -->
<param name="speed" value="1.5" type="double"/>
<param name="enabled" value="true" type="bool"/>
<param name="name" value="robot1" type="string"/>
<param name="count" value="10" type="int"/>

<!-- From file -->
<param name="description" textfile="$(find pkg)/urdf/robot.urdf"/>

<!-- Command output -->
<param name="description" command="cat $(find pkg)/urdf/robot.urdf"/>

<!-- Private parameter (inside node tag) -->
<node ...>
  <param name="~rate" value="10"/>  <!-- becomes /node_name/rate -->
</node>
```

### `<rosparam>`

Load/dump YAML parameter files.

```xml
<!-- Load YAML file -->
<rosparam file="$(find pkg)/config/params.yaml" command="load"/>

<!-- Load into namespace -->
<rosparam file="$(find pkg)/config/params.yaml" command="load" ns="robot1"/>

<!-- Inline YAML -->
<rosparam>
  gains:
    p: 1.0
    i: 0.1
    d: 0.05
</rosparam>

<!-- Delete parameters -->
<rosparam command="delete" param="old_param"/>
```

### `<remap>`

Remap topic/service names.

```xml
<node ...>
  <remap from="input" to="/sensor/data"/>
  <remap from="cmd_vel" to="/robot1/cmd_vel"/>
</node>
```

### `<include>`

Include another launch file.

```xml
<include file="$(find other_pkg)/launch/other.launch">
  <arg name="robot" value="$(arg robot)"/>
  <arg name="sim" value="true"/>
</include>

<!-- Pass all args -->
<include file="..." pass_all_args="true"/>

<!-- Include in namespace -->
<include file="..." ns="robot1"/>
```

### `<group>`

Group tags together for namespace or conditionals.

```xml
<!-- Namespace -->
<group ns="robot1">
  <node .../>  <!-- All nodes get /robot1 prefix -->
</group>

<!-- Conditional -->
<group if="$(arg use_sim)">
  <node pkg="simulator" .../>
</group>

<group unless="$(arg use_sim)">
  <node pkg="driver" .../>
</group>
```

---

## Substitution Arguments

| Syntax | Description | Example |
|--------|-------------|---------|
| `$(arg name)` | Argument value | `$(arg robot)` |
| `$(find pkg)` | Package path | `$(find your_pkg)/launch` |
| `$(env VAR)` | Environment variable | `$(env HOME)` |
| `$(optenv VAR default)` | Env var with default | `$(optenv ROS_IP localhost)` |
| `$(dirname)` | Launch file directory | `$(dirname)/config` |
| `$(eval expr)` | Python expression | `$(eval arg('rate') * 2)` |
| `$(anon name)` | Anonymous unique name | `$(anon node)` |

---

## Conditionals

```xml
<!-- if: execute when true -->
<node if="$(arg enable_feature)" .../>
<include if="$(arg use_sim)" file="..."/>
<param if="$(arg debug)" name="log_level" value="DEBUG"/>

<!-- unless: execute when false -->
<node unless="$(arg headless)" pkg="rviz" .../>

<!-- With eval for complex conditions -->
<group if="$(eval arg('mode') == 'simulation')">
  ...
</group>
```

---

## Common Patterns

### Multi-Robot Launch

```xml
<launch>
  <arg name="robot_name" default="robot1"/>

  <group ns="$(arg robot_name)">
    <param name="tf_prefix" value="$(arg robot_name)"/>
    <include file="$(find robot_pkg)/launch/robot.launch">
      <arg name="name" value="$(arg robot_name)"/>
    </include>
  </group>
</launch>
```

### Simulation vs Real

```xml
<launch>
  <arg name="sim" default="false"/>

  <!-- Simulation -->
  <group if="$(arg sim)">
    <include file="$(find gazebo_ros)/launch/gazebo.launch"/>
    <node pkg="sim_driver" type="sim_node" name="driver"/>
  </group>

  <!-- Real hardware -->
  <group unless="$(arg sim)">
    <node pkg="real_driver" type="driver_node" name="driver"/>
  </group>
</launch>
```

### Debug Mode

```xml
<launch>
  <arg name="debug" default="false"/>

  <node pkg="my_pkg" type="my_node" name="node"
        launch-prefix="$(eval 'gdb -ex run --args' if arg('debug') else '')"/>
</launch>
```

### Machine Deployment

```xml
<launch>
  <machine name="robot" address="192.168.1.100" user="ros"
           env-loader="/home/ros/catkin_ws/devel/env.sh"/>

  <node machine="robot" pkg="driver" type="driver_node" name="driver"/>
</launch>
```

---

## Best Practices

1. **Use arguments for configuration** - Don't hardcode values
2. **Document arguments** - Use `doc` attribute
3. **Use namespaces** - Prevent name collisions
4. **Separate concerns** - One launch file per subsystem
5. **Include, don't duplicate** - Reuse launch files
6. **Use $(find)** - Never hardcode paths
7. **Set output="screen" for debugging** - See node output
8. **Use required="true" for critical nodes** - Auto-shutdown on failure

---

## Debugging Launch Files

```bash
# Check syntax
roslaunch --ros-args pkg file.launch

# See all arguments
roslaunch --ros-args pkg file.launch

# Dry run (don't start nodes)
roslaunch pkg file.launch --dry-run

# Print generated XML
roslaunch pkg file.launch --dump-params
```

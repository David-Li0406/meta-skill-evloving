---
name: roblox-physics
description: Roblox physics and parts: BasePart, Model, constraints, welds, motors, collision. Use when working with 3D objects and physics.
---

# Physics Reference

## Quick Reference

- **Adaptive timestepping**: Adaptive timestepping automatically assigns physical parts to varying simulation timesteps.
- **Assemblies**: Explains physical assemblies and how they behave in Robloxs rigid body physics engine.
- **Character controllers**: Controller instances can be used as a component in a custom character implementation.
- **AlignOrientation**: The AlignOrientation constraint applies torque to align two attachments, or to align one attachment with a goal orientation.
- **AlignPosition**: The AlignPosition constraint applies force to move two attachments together, or to move one attachment to a goal position.
- **AngularVelocity**: The AngularVelocity constraint applies torque on an assembly to maintain a constant angular velocity.
- **BallSocket**: BallSocketConstraint forces its two attachments into the same position and allows them to freely rotate about all three axes, with optional limits to restrict both tilt and twist.
- **Cylindrical**: CylindricalConstraint allows its attachments to slide along one axis and rotate about another axis, with optional assigned angular and/or linear power.
- **Hinge**: HingeConstraint allows its two attachments to rotate about one axis, with optional assigned power for motor or servo behavior.
- **LineForce**: The LineForce constraint applies force along the theoretical line connecting its two attachments.

## Detailed Reference

### Physics
See [physics.md](physics.md) for:
- Adaptive timestepping
- Assemblies
- Character controllers
- AlignOrientation
- AlignPosition
- ...and 24 more

### Workspace
See [workspace.md](workspace.md) for:
- Customize the camera
- CFrames
- Collisions
- 3D workspace
- Raycasting
- ...and 1 more


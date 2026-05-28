# Physics Simulation - Validations

## Forward Euler for Dynamics Simulation

### **Id**
euler-for-dynamics
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - y\s*\+=\s*dt\s*\*\s*f\(|position\s*\+=\s*velocity\s*\*\s*dt(?!.*verlet)
### **Message**
Forward Euler is unstable for oscillatory systems. Consider RK4 or Verlet.
### **Fix Action**
Use RK4 for general systems, Verlet for Hamiltonian systems
### **Applies To**
  - **/*.py

## Hardcoded Timestep Without Stability Check

### **Id**
hardcoded-timestep
### **Severity**
info
### **Type**
regex
### **Pattern**
  - dt\s*=\s*0\.\d+\s*(?!#.*stab)
### **Message**
Timestep should be chosen based on system stability limits.
### **Fix Action**
Calculate dt from CFL condition or spring stability: dt < 2*sqrt(m/k)
### **Applies To**
  - **/*.py

## Contact Force Without Damping

### **Id**
no-damping-contact
### **Severity**
info
### **Type**
regex
### **Pattern**
  - contact.*force.*=.*stiffness.*penetration(?!.*damp)
  - k\s*\*\s*overlap(?!.*veloc)
### **Message**
Contact forces without damping cause jitter. Add velocity-based damping.
### **Fix Action**
Add damping term: f = k*penetration + c*velocity_into_contact
### **Applies To**
  - **/*.py

## Float32 for Large-Scale Simulation

### **Id**
float32-simulation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - np\.zeros.*float32.*position|dtype=np\.float32.*coord
### **Message**
Float32 loses precision at large coordinates. Consider float64.
### **Fix Action**
Use dtype=np.float64 for physics simulation state
### **Applies To**
  - **/*.py

## Stiff Spring Without Substepping

### **Id**
no-substep-spring
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - stiffness\s*=\s*[1-9]\d{4,}(?!.*substep|sub_step)
### **Message**
High stiffness may cause instability. Consider substepping.
### **Fix Action**
Substep or use implicit integration for stiff springs
### **Applies To**
  - **/*.py

## Matrix Inversion Inside Loop

### **Id**
matrix-inversion-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*:.*np\.linalg\.inv|while.*inv\(
### **Message**
Matrix inversion inside loop is expensive. Precompute or use solve().
### **Fix Action**
Use np.linalg.solve() or precompute inverse outside loop
### **Applies To**
  - **/*.py

## Velocity Without Upper Bound

### **Id**
unbounded-velocity
### **Severity**
info
### **Type**
regex
### **Pattern**
  - velocity\s*\+=.*(?!.*clip|max|clamp)
### **Message**
Unbounded velocity can cause tunneling. Consider velocity limits.
### **Fix Action**
Add velocity clamping: velocity = np.clip(velocity, -v_max, v_max)
### **Applies To**
  - **/*.py

## Direction Vector Not Normalized

### **Id**
non-normalized-direction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - direction\s*=\s*\w+\s*-\s*\w+(?!.*norm|/.*norm)
### **Message**
Direction vectors should be normalized before use.
### **Fix Action**
Normalize: direction = diff / np.linalg.norm(diff)
### **Applies To**
  - **/*.py
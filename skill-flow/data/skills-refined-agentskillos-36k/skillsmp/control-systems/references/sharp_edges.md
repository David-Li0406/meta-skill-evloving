# Control Systems - Sharp Edges

## Wrong PID Tuning Order Causes Oscillation

### **Id**
pid-tuning-order
### **Severity**
critical
### **Summary**
Tuning I before P, or D before I, leads to instability
### **Symptoms**
  - System oscillates at any gain setting
  - Increasing gain makes things worse
  - Controller never stabilizes
### **Why**
  PID terms interact. Tuning in wrong order creates instability:
  
  - P alone: Proportional response, steady-state error
  - I without P: Phase lag, guaranteed oscillation
  - D without P: Amplifies noise, no steady tracking
  
  Correct order: P first (for response), then I (eliminate error),
  finally D (reduce overshoot).
  
  Starting with I or having too much I relative to P
  causes phase lag that leads to oscillation.
  
### **Gotcha**
  # Common mistake: Starting with integral
  pid = PIDController(kp=0, ki=10, kd=0)  # Will oscillate!
  
  # Or: Too much I relative to P
  pid = PIDController(kp=1, ki=100, kd=0)  # Integral dominates, oscillates
  
### **Solution**
  # Systematic tuning procedure
  # 1. Set I = 0, D = 0, increase P until oscillation
  pid = PIDController(kp=0, ki=0, kd=0)
  
  # Find critical gain (Ku) where oscillation starts
  for kp in np.linspace(0, 100, 100):
      pid.gains.kp = kp
      # Test and check for sustained oscillation
  
  # 2. Use Ziegler-Nichols or similar method
  ku = 50  # Critical gain
  tu = 0.5  # Oscillation period
  
  # PID: kp = 0.6*ku, ki = 1.2*ku/tu, kd = 0.075*ku*tu
  gains = ziegler_nichols_tuning(ku, tu, 'PID')
  
  # 3. Fine-tune from there
  # Reduce I if overshoot, increase D if oscillating
  

## Continuous PID Formulas Don't Work at Low Sample Rates

### **Id**
discrete-time-pid
### **Severity**
high
### **Summary**
Textbook PID formulas assume continuous time, fail when sampled slowly
### **Symptoms**
  - Controller works at 1kHz, fails at 100Hz
  - Derivative term is noisy or wrong
  - Integral accumulates incorrectly
### **Why**
  Continuous PID: u = Kp*e + Ki*integral(e) + Kd*de/dt
  
  Discrete implementation matters:
  - Integral: Euler vs trapezoidal vs exact
  - Derivative: Forward vs backward vs filtered
  
  At low sample rates, these differences are significant.
  Bilinear (Tustin) transform preserves stability better
  than simple Euler integration.
  
### **Gotcha**
  # Simple Euler integration
  self.integral += error * dt
  derivative = (error - self.prev_error) / dt  # Noisy!
  
  # Works at 1kHz, fails at 50Hz
  
### **Solution**
  # Use proper discrete-time formulation
  
  # 1. Trapezoidal integration (more accurate)
  self.integral += 0.5 * (error + self.prev_error) * dt
  
  # 2. Filtered derivative (reduces noise)
  # First-order filter: d_filt = alpha * d_raw + (1-alpha) * d_prev
  tau_d = 0.1  # Filter time constant
  alpha = dt / (tau_d + dt)
  d_raw = (error - self.prev_error) / dt
  d_filtered = alpha * d_raw + (1 - alpha) * self.prev_derivative
  
  # 3. Or use bilinear transform for entire controller
  # s -> 2/T * (z-1)/(z+1)
  
  # 4. Derivative on measurement, not error
  d_raw = -(measurement - self.prev_measurement) / dt
  

## MPC Model Mismatch Causes Poor Performance

### **Id**
mpc-model-mismatch
### **Severity**
critical
### **Summary**
MPC relies on accurate model; errors cause suboptimal or unstable control
### **Symptoms**
  - MPC works in simulation, fails on real system
  - Controller is sluggish or oscillatory
  - Constraints violated despite MPC
### **Why**
  MPC optimizes based on predicted future states.
  If the model is wrong, predictions are wrong,
  and the "optimal" control is actually suboptimal.
  
  Common model errors:
  - Wrong time constants
  - Unmodeled friction/backlash
  - Linearization at wrong operating point
  - Ignored coupling between axes
  
  MPC is more sensitive to model errors than PID
  because it plans ahead based on the model.
  
### **Gotcha**
  # MPC with nominal model
  Ad_nominal = np.array([[1, 0.1], [0, 1]])  # Assumes no friction
  
  mpc = LinearMPC(Ad_nominal, Bd, params)
  
  # Real system has friction - model predicts wrong trajectory
  # MPC optimizes for wrong predictions
  
### **Solution**
  # 1. System identification
  from scipy.optimize import curve_fit
  
  def system_response(t, tau, K):
      return K * (1 - np.exp(-t/tau))
  
  # Fit model to step response data
  params, _ = curve_fit(system_response, t_data, y_data)
  
  # 2. Add disturbance estimation
  class DisturbanceObserver:
      """Estimate and compensate for model mismatch."""
      def __init__(self, model):
          self.model = model
          self.d_hat = 0  # Estimated disturbance
  
      def update(self, x, x_predicted, L=0.5):
          # Disturbance = difference between prediction and reality
          self.d_hat = L * self.d_hat + (1-L) * (x - x_predicted)
          return self.d_hat
  
  # 3. Robust MPC with uncertainty bounds
  # Tighten constraints to account for model error
  
  # 4. Adaptive MPC (update model online)
  

## Control Loop Sample Rate Too Low

### **Id**
sample-rate-control
### **Severity**
high
### **Summary**
Slow sample rate causes phase lag and instability
### **Symptoms**
  - System oscillates at high frequencies
  - Controller can't track fast references
  - Adding D gain makes oscillation worse
### **Why**
  Rule of thumb: sample rate should be 10-20x the
  system's fastest dynamics (bandwidth).
  
  For motor control:
  - Current loop: 10-20 kHz
  - Velocity loop: 1-10 kHz
  - Position loop: 100-1000 Hz
  
  Too slow sampling adds phase lag, reducing stability margins.
  It also aliases high-frequency disturbances.
  
### **Gotcha**
  # Motor position control at 10 Hz
  while True:
      time.sleep(0.1)  # 10 Hz - WAY too slow for motors
      u = pid.update(setpoint, position)
      motor.set_command(u)
  
  # Motor dynamics are ~100Hz, need at least 1kHz control
  
### **Solution**
  # 1. Use hardware timer for precise control loop
  def timer_isr():
      """1kHz control interrupt."""
      global position, setpoint
      u = pid.update(setpoint, position)
      motor.set_pwm(u)
  
  setup_timer_interrupt(frequency=1000, callback=timer_isr)
  
  # 2. Separate fast and slow loops
  # Fast: current/velocity (hardware timer, 1-10kHz)
  # Slow: position/trajectory (software, 100-500Hz)
  
  # 3. For ROS2: Use realtime-safe callback groups
  from rclpy.callback_groups import RealtimeCallbackGroup
  
  self.control_timer = self.create_timer(
      0.001,  # 1ms = 1kHz
      self.control_callback,
      callback_group=RealtimeCallbackGroup()
  )
  

## Ignoring Actuator Saturation

### **Id**
actuator-saturation
### **Severity**
high
### **Summary**
Controller commands exceed physical limits, causes windup and instability
### **Symptoms**
  - Large overshoot on step response
  - Slow recovery after large errors
  - Oscillation after hitting limits
### **Why**
  Every actuator has limits:
  - Motors: max current, max voltage
  - Servos: max position, max velocity
  - Pumps: max flow rate
  
  If controller outputs exceed these, the actuator saturates.
  The controller keeps integrating error, causing windup.
  When error reduces, the accumulated integral causes overshoot.
  
  MPC handles this naturally via constraints.
  PID needs explicit anti-windup.
  
### **Gotcha**
  # PID without output limits
  pid = PIDController(gains, dt)  # No limits!
  
  u = pid.update(setpoint, measurement)  # Could be 1000V
  motor.set_voltage(u)  # Motor saturates at 24V
  
  # Integral keeps growing during saturation
  # Huge overshoot when setpoint reached
  
### **Solution**
  # 1. Clamp output and implement anti-windup
  pid = PIDController(
      gains, dt,
      output_limits=(-24.0, 24.0)  # Voltage limits
  )
  
  # 2. Back-calculation anti-windup
  output_unsat = p + i + d
  output = np.clip(output_unsat, -24, 24)
  if ki != 0:
      anti_windup = (output - output_unsat) / ki
      integral += anti_windup
  
  # 3. Conditional integration
  if not saturated:
      integral += error * dt
  # Don't integrate while saturated
  
  # 4. Use MPC with explicit constraints
  mpc = LinearMPC(
      A, B, params,
      u_min=np.array([-24.0]),
      u_max=np.array([24.0])
  )
  

## Setpoint Jump Causes Actuator Stress

### **Id**
setpoint-jump
### **Severity**
medium
### **Summary**
Step changes in setpoint cause aggressive control action
### **Symptoms**
  - Motor jerks on setpoint change
  - Mechanical stress and wear
  - Overshoot on step response
### **Why**
  Derivative term amplifies sudden changes.
  Step change in setpoint = infinite derivative = kick.
  
  Even without D, large step = large error = aggressive P action.
  This stresses mechanical systems and can cause vibration.
  
### **Solution**
  # 1. Derivative on measurement (not error)
  derivative = -(measurement - prev_measurement) / dt
  # Not: derivative = (error - prev_error) / dt
  
  # 2. Setpoint ramping/filtering
  class SetpointFilter:
      def __init__(self, rate_limit, dt):
          self.rate = rate_limit
          self.dt = dt
          self.filtered = 0
  
      def update(self, setpoint):
          delta = setpoint - self.filtered
          max_delta = self.rate * self.dt
          delta = np.clip(delta, -max_delta, max_delta)
          self.filtered += delta
          return self.filtered
  
  # 3. Use trajectory generator
  # Instead of step: use minimum-jerk or trapezoidal profile
  
  # 4. Setpoint weighting (P acts on weighted setpoint)
  # u = Kp * (b * setpoint - measurement) + ...
  # b < 1 reduces kick
  
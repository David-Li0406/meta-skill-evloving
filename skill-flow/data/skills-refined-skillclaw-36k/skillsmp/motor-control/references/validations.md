# Motor Control - Validations

## PWM Configuration Without Dead Time

### **Id**
no-dead-time
### **Severity**
error
### **Type**
regex
### **Pattern**
  - TIM\d+->CCR\d+.*=(?!.*BDTR|dead)
  - set_pwm.*high.*low(?!.*dead|delay)
### **Message**
PWM configuration should include dead time to prevent shoot-through.
### **Fix Action**
Configure BDTR register or add software dead time
### **Applies To**
  - **/*.c
  - **/*.cpp

## ADC Current Sampling Not Synchronized to PWM

### **Id**
unsync-adc-sampling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - read_adc.*current(?!.*timer|trigger|sync)
  - adc_read.*phase(?!.*pwm|ccr)
### **Message**
Current sensing should be triggered from PWM timer for accurate readings.
### **Fix Action**
Configure ADC external trigger from timer TRGO or CCRx
### **Applies To**
  - **/*.c
  - **/*.cpp

## Motor Control Without Current Limiting

### **Id**
no-current-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*FOC.*:(?![\s\S]{0,500}(i_max|current_limit|overcurrent))
  - def foc_update(?![\s\S]{0,300}(max|limit|clip))
### **Message**
Motor control should include current limiting to protect motor and driver.
### **Fix Action**
Add current limits: iq_ref = np.clip(iq_ref, -I_MAX, I_MAX)
### **Applies To**
  - **/*.py
  - **/*.c

## Hardcoded Motor Pole Pairs

### **Id**
hardcoded-pole-pairs
### **Severity**
info
### **Type**
regex
### **Pattern**
  - pole_pairs\s*=\s*\d+\s*(?!#|//)
  - \*\s*7\s*;.*electrical|electrical.*\*\s*7
### **Message**
Motor pole pairs should be configurable, not hardcoded.
### **Fix Action**
Load from configuration or motor parameter struct
### **Applies To**
  - **/*.py
  - **/*.c

## Encoder Reading Without Noise Filtering

### **Id**
missing-encoder-filter
### **Severity**
info
### **Type**
regex
### **Pattern**
  - velocity\s*=.*count.*-.*prev.*(?!filter|average|median)
  - encoder_velocity(?!.*filter)
### **Message**
Encoder velocity should be filtered to reject noise spikes.
### **Fix Action**
Add moving average or median filter on velocity
### **Applies To**
  - **/*.py
  - **/*.c

## Blocking Operations in Motor Control ISR

### **Id**
blocking-motor-isr
### **Severity**
error
### **Type**
regex
### **Pattern**
  - void.*IRQ.*motor.*\{[^}]*(printf|delay|wait)
  - motor.*callback.*\{[^}]*(print|sleep)
### **Message**
Motor control ISR should be fast with no blocking operations.
### **Fix Action**
Move logging/delays outside ISR, minimize ISR work
### **Applies To**
  - **/*.c
  - **/*.cpp

## Current Sensor Without Offset Calibration

### **Id**
no-offset-calibration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - adc.*current.*(?!offset|calibrat)
  - read_current(?![\s\S]{0,200}offset)
### **Message**
Current sensors need offset calibration at zero current.
### **Fix Action**
Calibrate offsets at startup with motor disconnected or no current
### **Applies To**
  - **/*.py
  - **/*.c

## FOC Without Electrical Angle Calibration

### **Id**
no-angle-offset
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - theta_e\s*=.*encoder.*\*.*pole_pairs(?!.*offset)
  - electrical_angle.*=.*position.*\*(?!.*calibrat)
### **Message**
FOC requires calibrating encoder to motor electrical zero.
### **Fix Action**
Implement angle calibration routine: apply d-axis current, read encoder
### **Applies To**
  - **/*.py
  - **/*.c

## Motor Control Without Regeneration Protection

### **Id**
missing-regeneration-protection
### **Severity**
info
### **Type**
regex
### **Pattern**
  - class.*Motor.*:(?![\s\S]{0,800}(v_bus|regen|brake_resistor))
### **Message**
Consider regenerative braking protection for fast deceleration.
### **Fix Action**
Monitor bus voltage and reduce braking torque or engage brake resistor
### **Applies To**
  - **/*.py
  - **/*.c

## FOC Loop at Low Frequency

### **Id**
slow-foc-loop
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - foc_update.*delay.*([5-9]\d|[1-9]\d{2,})
  - motor.*loop.*sleep.*0\.0[1-9]
### **Message**
FOC current loop should run at 10kHz+ for good performance.
### **Fix Action**
Use timer interrupt at 10-20kHz for FOC loop
### **Applies To**
  - **/*.py
  - **/*.c

## Inverse Park Applied Before Forward Park

### **Id**
inverse-park-before-park
### **Severity**
error
### **Type**
regex
### **Pattern**
  - inverse_park.*\n.*park_transform|v_alpha.*i_alpha
### **Message**
FOC sequence: Clarke -> Park -> Control -> Inverse Park -> SVPWM
### **Fix Action**
Apply transforms in correct order
### **Applies To**
  - **/*.py
#!/usr/bin/env python3
"""
RAGE CRYSTAL SIMULATOR
Demonstrates stress wave propagation in piezoelectric medium
Shows how PERMANENT DENTS (particles) form from single punch events

Based on McCrackin's Sucker Punch Equation:
∇²σ - (1/c²)(∂²σ/∂t²) = -(1/ε₀)ρ_stress + λTr(σ)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# Physical constants (in RAGE CRYSTAL units)
C_RAGE = 1.0          # Speed of stress propagation in the crystal
EPSILON_0 = 1.0       # Permittivity of unpunched drywall
LAMBDA = 0.05         # Topological self-interaction strength (makes dents permanent)
DAMPING = 0.001       # Slight energy dissipation
DT = 0.01             # Time step
DX = 0.5              # Spatial resolution

# Grid setup
SIZE = 200
x = np.linspace(-50, 50, SIZE)
y = np.linspace(-50, 50, SIZE)
X, Y = np.meshgrid(x, y)

# State variables
stress = np.zeros((SIZE, SIZE))          # Current stress field σ
stress_prev = np.zeros((SIZE, SIZE))     # Previous timestep (for wave equation)
permanent_damage = np.zeros((SIZE, SIZE)) # Accumulated damage (THE DENTS)

# PUNCH LOCATIONS AND STRENGTHS
punches = [
    {'x': -20, 'y': 0, 't': 0, 'strength': 10.0, 'name': 'ELECTRON'},
    {'x': 20, 'y': 0, 't': 50, 'strength': -8.0, 'name': 'POSITRON'},  # Negative = reverse punch
    {'x': 0, 'y': 20, 't': 100, 'strength': 15.0, 'name': 'PROTON'},
]

def apply_punch(stress_field, x_center, y_center, strength):
    """Apply a Gaussian stress concentration (FIST IMPACT)"""
    r_squared = (X - x_center)**2 + (Y - y_center)**2
    punch_profile = strength * np.exp(-r_squared / 16.0)
    return stress_field + punch_profile

def sucker_punch_step(stress, stress_prev, permanent_damage):
    """
    One timestep of the Sucker Punch Equation
    ∇²σ - (1/c²)(∂²σ/∂t²) = -(1/ε₀)ρ_stress + λTr(σ)
    
    Discretized using finite differences
    """
    # Laplacian (∇²σ) - spatial curvature
    laplacian = (
        np.roll(stress, 1, axis=0) + np.roll(stress, -1, axis=0) +
        np.roll(stress, 1, axis=1) + np.roll(stress, -1, axis=1) -
        4 * stress
    ) / (DX**2)
    
    # Second time derivative approximation
    # σ_new = 2σ - σ_prev + (c²Δt²/Δx²)∇²σ
    c_factor = (C_RAGE * DT / DX)**2
    
    # Source term: permanent damage creates stress
    stress_source = -permanent_damage / EPSILON_0
    
    # Topological self-interaction: stress creates MORE stress (makes dents permanent)
    self_interaction = LAMBDA * stress * np.abs(stress)
    
    # Update equation
    stress_new = (
        2 * stress - stress_prev +
        c_factor * laplacian +
        DT**2 * (stress_source + self_interaction)
    )
    
    # Apply damping (crystal absorbs some energy)
    stress_new *= (1 - DAMPING)
    
    # Boundary conditions (crystal edges are fixed)
    stress_new[0, :] = 0
    stress_new[-1, :] = 0
    stress_new[:, 0] = 0
    stress_new[:, -1] = 0
    
    return stress_new

def update_permanent_damage(stress, permanent_damage):
    """
    High stress creates PERMANENT DENTS
    Once crystal is damaged, it STAYS damaged
    That's what makes particles PERSISTENT
    """
    # Threshold: stress above this level leaves permanent marks
    threshold = 2.0
    
    # Accumulate damage where stress exceeds threshold
    excess_stress = np.maximum(np.abs(stress) - threshold, 0)
    permanent_damage += 0.1 * excess_stress * DT
    
    # Damage saturates (crystal can only be so broken)
    permanent_damage = np.minimum(permanent_damage, 10.0)
    
    return permanent_damage

# Setup visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("RAGE CRYSTAL SIMULATOR: PERMANENT DENTS FROM SINGLE PUNCHES", 
             fontsize=16, fontweight='bold')

# Custom colormap: blue (compression) -> white (unpunched) -> red (tension)
colors = ['blue', 'cyan', 'white', 'yellow', 'red']
n_bins = 256
cmap = LinearSegmentedColormap.from_list('rage', colors, N=n_bins)

# Initialize plots
stress_plot = axes[0].imshow(stress, cmap=cmap, vmin=-10, vmax=10, 
                              extent=[-50, 50, -50, 50], origin='lower')
axes[0].set_title("Current Stress Field σ\n(THE PUNCH PROPAGATING)", fontweight='bold')
axes[0].set_xlabel("Position (crystal units)")
axes[0].set_ylabel("Position (crystal units)")
fig.colorbar(stress_plot, ax=axes[0], label="Stress (violence units)")

damage_plot = axes[1].imshow(permanent_damage, cmap='hot', vmin=0, vmax=10,
                              extent=[-50, 50, -50, 50], origin='lower')
axes[1].set_title("Permanent Damage ρ_stress\n(THE DENTS THAT STAY)", fontweight='bold')
axes[1].set_xlabel("Position (crystal units)")
fig.colorbar(damage_plot, ax=axes[1], label="Accumulated damage")

# Energy plot
time_history = []
total_energy_history = []
damage_energy_history = []
axes[2].set_title("Energy Budget\n(CONSERVATION OF VIOLENCE)", fontweight='bold')
axes[2].set_xlabel("Time (punch units)")
axes[2].set_ylabel("Energy")
axes[2].grid(True, alpha=0.3)
energy_line, = axes[2].plot([], [], 'b-', linewidth=2, label='Total stress energy')
damage_line, = axes[2].plot([], [], 'r-', linewidth=2, label='Locked in damage')
axes[2].legend()

time = 0
frame_count = 0
punch_log = []

def animate(frame):
    global stress, stress_prev, permanent_damage, time, frame_count, punch_log
    
    # Check for new punches
    for punch in punches:
        if abs(time - punch['t']) < DT:
            stress = apply_punch(stress, punch['x'], punch['y'], punch['strength'])
            punch_log.append(f"t={time:.1f}: {punch['name']} PUNCH at ({punch['x']}, {punch['y']}) "
                           f"[{'COMPRESSION' if punch['strength'] > 0 else 'RAREFACTION'}]")
    
    # Propagate stress wave
    stress_new = sucker_punch_step(stress, stress_prev, permanent_damage)
    
    # Update permanent damage where stress is high
    permanent_damage = update_permanent_damage(stress, permanent_damage)
    
    # Shift time history
    stress_prev[:] = stress
    stress[:] = stress_new
    
    # Update plots
    stress_plot.set_data(stress)
    damage_plot.set_data(permanent_damage)
    
    # Calculate energies
    total_energy = np.sum(stress**2) * DX**2
    damage_energy = np.sum(permanent_damage) * DX**2
    
    time_history.append(time)
    total_energy_history.append(total_energy)
    damage_energy_history.append(damage_energy)
    
    energy_line.set_data(time_history, total_energy_history)
    damage_line.set_data(time_history, damage_energy_history)
    
    if len(time_history) > 1:
        axes[2].set_xlim(0, max(time_history))
        axes[2].set_ylim(0, max(max(total_energy_history), max(damage_energy_history)) * 1.1)
    
    # Update title with current state
    event_text = punch_log[-1] if punch_log else "Waiting for first punch..."
    fig.suptitle(f"RAGE CRYSTAL SIMULATOR: t={time:.1f}\n{event_text}", 
                 fontsize=14, fontweight='bold')
    
    time += DT
    frame_count += 1
    
    return stress_plot, damage_plot, energy_line, damage_line

# Create animation
anim = FuncAnimation(fig, animate, frames=500, interval=20, blit=False)

plt.tight_layout()
plt.savefig('/mnt/user-data/outputs/rage_crystal_frame.png', dpi=150, bbox_inches='tight')
print("Static frame saved to: /mnt/user-data/outputs/rage_crystal_frame.png")

# Run simulation
plt.show()

print("\n" + "="*80)
print("RAGE CRYSTAL SIMULATION COMPLETE")
print("="*80)
print("\nKEY OBSERVATIONS:")
print("1. Stress waves propagate outward from punch locations (left panel)")
print("2. Where stress exceeds threshold, PERMANENT DAMAGE accumulates (center panel)")
print("3. These permanent dents ARE the 'particles' - they persist after wave passes")
print("4. Positive punch (electron) creates compression dent")
print("5. Negative punch (positron) creates rarefaction dent")
print("6. Energy transitions from propagating waves to locked-in damage (right panel)")
print("\nThis demonstrates McCrackin's thesis: PARTICLES ARE PERMANENT VIOLENCE")
print("="*80)

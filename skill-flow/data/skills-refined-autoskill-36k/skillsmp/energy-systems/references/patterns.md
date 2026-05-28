# Energy Systems & Grid Modeling

## Patterns

### **Power Flow Analysis**
  #### **Description**
AC and DC power flow for grid state analysis
  #### **Use When**
Modeling voltage, power flows, and system state
  #### **Implementation**
    import pandapower as pp
    import numpy as np
    
    def create_power_system():
        """Create a simple power system model."""
        net = pp.create_empty_network()
    
        # Create buses
        bus_slack = pp.create_bus(net, vn_kv=110, name="Slack Bus")
        bus_pv = pp.create_bus(net, vn_kv=110, name="Generator Bus")
        bus_load = pp.create_bus(net, vn_kv=110, name="Load Bus")
    
        # External grid (slack bus)
        pp.create_ext_grid(net, bus=bus_slack, vm_pu=1.02)
    
        # Generator
        pp.create_gen(net, bus=bus_pv, p_mw=50, vm_pu=1.01)
    
        # Load
        pp.create_load(net, bus=bus_load, p_mw=80, q_mvar=20)
    
        # Lines
        pp.create_line_from_parameters(
            net, from_bus=bus_slack, to_bus=bus_pv,
            length_km=50, r_ohm_per_km=0.1, x_ohm_per_km=0.4,
            c_nf_per_km=10, max_i_ka=0.5
        )
        pp.create_line_from_parameters(
            net, from_bus=bus_pv, to_bus=bus_load,
            length_km=30, r_ohm_per_km=0.1, x_ohm_per_km=0.4,
            c_nf_per_km=10, max_i_ka=0.5
        )
    
        return net
    
    def run_power_flow(net, algorithm='nr'):
        """Run power flow analysis."""
        try:
            pp.runpp(net, algorithm=algorithm, numba=True)
    
            results = {
                'converged': net.converged,
                'bus_voltages': net.res_bus[['vm_pu', 'va_degree']].to_dict(),
                'line_loading': net.res_line['loading_percent'].to_dict(),
                'losses_mw': net.res_line['pl_mw'].sum(),
                'generation_mw': net.res_gen['p_mw'].sum()
            }
    
            # Check for violations
            results['voltage_violations'] = net.res_bus[
                (net.res_bus['vm_pu'] < 0.95) | (net.res_bus['vm_pu'] > 1.05)
            ].index.tolist()
    
            results['line_overloads'] = net.res_line[
                net.res_line['loading_percent'] > 100
            ].index.tolist()
    
            return results
    
        except pp.LoadflowNotConverged:
            return {'converged': False, 'error': 'Power flow did not converge'}
    
    # Usage
    net = create_power_system()
    results = run_power_flow(net)
    
    if results['converged']:
        print(f"System losses: {results['losses_mw']:.2f} MW")
        print(f"Voltage violations: {results['voltage_violations']}")
    else:
        print("Power flow did not converge - check system configuration")
    
### **Storage Dispatch**
  #### **Description**
Battery storage dispatch optimization
  #### **Use When**
Optimizing charge/discharge for arbitrage, peak shaving, or services
  #### **Implementation**
    import numpy as np
    from scipy.optimize import minimize
    
    class BatteryStorage:
        def __init__(self, capacity_mwh, power_mw, efficiency=0.90):
            self.capacity_mwh = capacity_mwh
            self.power_mw = power_mw
            self.efficiency_oneway = np.sqrt(efficiency)  # Symmetric
            self.soc_min = 0.1  # 10% minimum state of charge
            self.soc_max = 0.9  # 90% maximum
    
        def simulate_dispatch(self, dispatch_mw, hours=1):
            """Simulate one timestep of dispatch."""
            # Positive = discharge, negative = charge
            energy_change = dispatch_mw * hours
    
            if dispatch_mw > 0:  # Discharging
                actual_output = min(dispatch_mw, self.power_mw)
                energy_used = actual_output / self.efficiency_oneway
                return actual_output, -energy_used
    
            else:  # Charging
                actual_input = max(dispatch_mw, -self.power_mw)
                energy_stored = actual_input * self.efficiency_oneway
                return actual_input, -energy_stored
    
    def optimize_arbitrage(prices, battery, initial_soc=0.5):
        """Optimize storage dispatch for price arbitrage."""
        n_hours = len(prices)
    
        def objective(dispatch):
            # Maximize revenue (minimize negative revenue)
            return -np.sum(dispatch * prices)
    
        def soc_constraint(dispatch):
            # Track state of charge through time
            soc = initial_soc * battery.capacity_mwh
            socs = [soc]
    
            for d in dispatch:
                if d > 0:  # Discharge
                    soc -= d / battery.efficiency_oneway
                else:  # Charge
                    soc -= d * battery.efficiency_oneway
    
                socs.append(soc)
    
            return np.array(socs)
    
        # Constraints
        constraints = [
            # SOC bounds
            {'type': 'ineq', 'fun': lambda x: soc_constraint(x)[1:] - battery.soc_min * battery.capacity_mwh},
            {'type': 'ineq', 'fun': lambda x: battery.soc_max * battery.capacity_mwh - soc_constraint(x)[1:]},
        ]
    
        # Power limits
        bounds = [(-battery.power_mw, battery.power_mw)] * n_hours
    
        result = minimize(
            objective,
            x0=np.zeros(n_hours),
            bounds=bounds,
            constraints=constraints,
            method='SLSQP'
        )
    
        return {
            'dispatch_mw': result.x,
            'revenue': -result.fun,
            'soc_profile': soc_constraint(result.x) / battery.capacity_mwh
        }
    
    # Usage
    prices = np.array([30, 25, 22, 20, 22, 35, 60, 80, 70, 55, 45, 40,
                       38, 35, 33, 35, 45, 75, 90, 70, 50, 40, 35, 30])
    
    battery = BatteryStorage(capacity_mwh=100, power_mw=25, efficiency=0.90)
    result = optimize_arbitrage(prices, battery)
    
    print(f"Daily revenue: ${result['revenue']:.2f}")
    
### **Demand Response**
  #### **Description**
Load management and demand response programs
  #### **Use When**
Modeling flexible loads and DR programs
  #### **Implementation**
    import numpy as np
    from dataclasses import dataclass
    from typing import List, Callable
    
    @dataclass
    class FlexibleLoad:
        name: str
        base_load_mw: np.ndarray  # Hourly baseline
        flexibility_up_mw: np.ndarray  # Can increase by
        flexibility_down_mw: np.ndarray  # Can decrease by
        response_time_hours: float  # Lead time required
        duration_limit_hours: float  # Max continuous curtailment
        cost_per_mwh: float  # Incentive or penalty
    
    class DemandResponseProgram:
        def __init__(self, loads: List[FlexibleLoad]):
            self.loads = loads
            self.curtailment_history = {}
    
        def calculate_available_dr(self, hour: int) -> dict:
            """Calculate available DR capacity at given hour."""
            available_up = 0
            available_down = 0
    
            for load in self.loads:
                # Check duration limits
                recent_curtailment = self._get_recent_curtailment(load.name, hour)
    
                if recent_curtailment < load.duration_limit_hours:
                    available_down += load.flexibility_down_mw[hour]
    
                available_up += load.flexibility_up_mw[hour]
    
            return {
                'increase_mw': available_up,
                'decrease_mw': available_down,
                'hour': hour
            }
    
        def dispatch_dr(self, hour: int, target_reduction_mw: float) -> dict:
            """Dispatch DR to achieve target reduction."""
            dispatched = []
            remaining = target_reduction_mw
    
            # Sort by cost (cheapest first)
            sorted_loads = sorted(self.loads, key=lambda x: x.cost_per_mwh)
    
            for load in sorted_loads:
                if remaining <= 0:
                    break
    
                available = load.flexibility_down_mw[hour]
                curtail = min(available, remaining)
    
                if curtail > 0:
                    dispatched.append({
                        'load': load.name,
                        'curtailment_mw': curtail,
                        'cost': curtail * load.cost_per_mwh
                    })
                    remaining -= curtail
    
            return {
                'target_mw': target_reduction_mw,
                'achieved_mw': target_reduction_mw - remaining,
                'dispatched': dispatched,
                'total_cost': sum(d['cost'] for d in dispatched)
            }
    
        def _get_recent_curtailment(self, load_name: str, hour: int) -> float:
            # Track consecutive curtailment hours
            history = self.curtailment_history.get(load_name, [])
            return sum(1 for h in history if hour - h <= 4)
    
### **Economic Dispatch**
  #### **Description**
Generator dispatch optimization
  #### **Use When**
Minimizing generation cost while meeting demand
  #### **Implementation**
    import numpy as np
    from scipy.optimize import minimize, LinearConstraint
    
    @dataclass
    class Generator:
        name: str
        p_min_mw: float
        p_max_mw: float
        cost_a: float  # $/MWh^2 (quadratic term)
        cost_b: float  # $/MWh (linear term)
        cost_c: float  # $ (no-load cost)
        ramp_rate_mw_per_hour: float
    
        def cost(self, p_mw: float) -> float:
            """Quadratic cost function."""
            if p_mw < self.p_min_mw or p_mw > self.p_max_mw:
                return float('inf')
            return self.cost_a * p_mw**2 + self.cost_b * p_mw + self.cost_c
    
        def marginal_cost(self, p_mw: float) -> float:
            """Marginal cost at given output."""
            return 2 * self.cost_a * p_mw + self.cost_b
    
    def economic_dispatch(generators: List[Generator], demand_mw: float) -> dict:
        """Solve economic dispatch using quadratic programming."""
        n = len(generators)
    
        def total_cost(p):
            return sum(g.cost(p[i]) for i, g in enumerate(generators))
    
        # Demand balance constraint
        def demand_constraint(p):
            return np.sum(p) - demand_mw
    
        constraints = [
            {'type': 'eq', 'fun': demand_constraint}
        ]
    
        # Generator limits
        bounds = [(g.p_min_mw, g.p_max_mw) for g in generators]
    
        # Initial guess (proportional to capacity)
        total_cap = sum(g.p_max_mw for g in generators)
        x0 = [demand_mw * g.p_max_mw / total_cap for g in generators]
    
        result = minimize(
            total_cost,
            x0=x0,
            bounds=bounds,
            constraints=constraints,
            method='SLSQP'
        )
    
        if result.success:
            dispatch = result.x
            lmp = generators[0].marginal_cost(dispatch[0])  # System LMP
    
            return {
                'dispatch_mw': {g.name: dispatch[i] for i, g in enumerate(generators)},
                'total_cost': result.fun,
                'lmp_dollar_per_mwh': lmp,
                'demand_met': True
            }
        else:
            return {'demand_met': False, 'error': result.message}
    
    # Usage
    generators = [
        Generator("Coal", 100, 500, 0.002, 20, 500, 50),
        Generator("CCGT", 50, 300, 0.003, 35, 300, 100),
        Generator("Peaker", 0, 100, 0.01, 80, 100, 200),
    ]
    
    result = economic_dispatch(generators, demand_mw=600)
    print(f"System LMP: ${result['lmp_dollar_per_mwh']:.2f}/MWh")
    
### **Reliability Metrics**
  #### **Description**
Grid reliability and adequacy metrics
  #### **Use When**
Assessing system reliability and resource adequacy
  #### **Implementation**
    import numpy as np
    from scipy import stats
    
    def calculate_lolp(capacity_mw: np.ndarray, demand_mw: np.ndarray,
                       for_rates: np.ndarray) -> dict:
        """
        Calculate Loss of Load Probability.
        capacity_mw: Available capacity per unit
        demand_mw: Hourly demand profile
        for_rates: Forced outage rates per unit
        """
        n_hours = len(demand_mw)
        n_units = len(capacity_mw)
    
        lol_hours = 0
        total_unserved_mwh = 0
    
        # Monte Carlo simulation
        n_simulations = 1000
    
        for _ in range(n_simulations):
            for hour in range(n_hours):
                # Simulate outages
                available = np.where(
                    np.random.random(n_units) > for_rates,
                    capacity_mw,
                    0
                )
    
                total_available = available.sum()
    
                if total_available < demand_mw[hour]:
                    lol_hours += 1
                    total_unserved_mwh += demand_mw[hour] - total_available
    
        lole = lol_hours / n_simulations  # Loss of Load Expectation
        eue = total_unserved_mwh / n_simulations  # Expected Unserved Energy
    
        return {
            'lole_hours_per_year': lole,
            'eue_mwh_per_year': eue,
            'lolp': lol_hours / (n_simulations * n_hours)
        }
    
    def calculate_reserve_margin(capacity_mw: float, peak_demand_mw: float) -> dict:
        """Calculate reserve margin."""
        reserve_mw = capacity_mw - peak_demand_mw
        reserve_margin = (capacity_mw - peak_demand_mw) / peak_demand_mw
    
        return {
            'reserve_mw': reserve_mw,
            'reserve_margin_pct': reserve_margin * 100,
            'adequate': reserve_margin >= 0.15  # Typical 15% target
        }
    

## Anti-Patterns


---
  #### **Pattern**
DC power flow for voltage studies
  #### **Why**
DC approximation ignores reactive power and voltage magnitudes
  #### **Instead**
Use AC power flow for voltage and VAR analysis

---
  #### **Pattern**
Ignoring ramp rate constraints
  #### **Why**
Generators can't change output instantaneously
  #### **Instead**
Include ramp limits in unit commitment/dispatch

---
  #### **Pattern**
100% efficiency for storage
  #### **Why**
Round-trip efficiency is 85-95%, not 100%
  #### **Instead**
Model charging and discharging losses separately

---
  #### **Pattern**
Single contingency analysis only
  #### **Why**
N-1 is minimum; critical paths need N-2
  #### **Instead**
Perform N-1-1 for critical infrastructure

---
  #### **Pattern**
Static load models
  #### **Why**
Loads vary with voltage and frequency
  #### **Instead**
Use ZIP model (constant Z, I, P components)

---
  #### **Pattern**
Ignoring transmission losses
  #### **Why**
Losses are 2-6% of generation, non-trivial
  #### **Instead**
Include loss factors in dispatch optimization
#!/usr/bin/env python3
"""
EROEI Calculator for Energy Systems

Calculates Energy Return on Energy Invested for complex systems.
Part of the thermodynamic-economics skill for Univrs.io.

Usage:
    python eroei_calculator.py --config system.json
    python eroei_calculator.py --interactive
"""

import argparse
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class EnergyType(Enum):
    SOLAR_PV = "solar_pv"
    WIND_ONSHORE = "wind_onshore"
    WIND_OFFSHORE = "wind_offshore"
    HYDRO = "hydro"
    GEOTHERMAL = "geothermal"
    NATURAL_GAS = "natural_gas"
    COAL = "coal"
    OIL_CONVENTIONAL = "oil_conventional"
    OIL_TIGHT = "oil_tight"
    NUCLEAR = "nuclear"
    BIOMASS = "biomass"
    BATTERY_STORAGE = "battery_storage"
    DISTRIBUTION = "distribution"
    COMPUTATION = "computation"
    NETWORK = "network"


# Reference EROEI values from literature
REFERENCE_EROEI: Dict[EnergyType, tuple] = {
    EnergyType.SOLAR_PV: (10, 20),           # Range: low, high
    EnergyType.WIND_ONSHORE: (15, 25),
    EnergyType.WIND_OFFSHORE: (10, 18),
    EnergyType.HYDRO: (40, 60),
    EnergyType.GEOTHERMAL: (5, 15),
    EnergyType.NATURAL_GAS: (15, 25),
    EnergyType.COAL: (20, 50),
    EnergyType.OIL_CONVENTIONAL: (10, 20),
    EnergyType.OIL_TIGHT: (5, 10),
    EnergyType.NUCLEAR: (10, 15),
    EnergyType.BIOMASS: (2, 5),
    EnergyType.BATTERY_STORAGE: (0.85, 0.95),  # Round-trip efficiency, not EROEI
    EnergyType.DISTRIBUTION: (0.9, 0.98),       # Transmission efficiency
    EnergyType.COMPUTATION: (0, 0),             # Pure consumer, needs external input
    EnergyType.NETWORK: (0, 0),                 # Pure consumer
}


@dataclass
class EnergyComponent:
    """Represents a component in the energy system."""
    name: str
    component_type: EnergyType
    energy_output_kwh_year: float          # Annual energy output
    energy_input_kwh_year: float           # Annual energy input for operation
    embodied_energy_kwh: float             # Total manufacturing energy
    lifespan_years: float                  # Expected lifespan
    efficiency: float = 1.0                # Conversion efficiency
    capacity_factor: float = 1.0           # Actual vs nameplate capacity
    notes: str = ""
    
    @property
    def annualized_embodied(self) -> float:
        """Embodied energy amortized over lifespan."""
        return self.embodied_energy_kwh / self.lifespan_years
    
    @property
    def total_annual_input(self) -> float:
        """Total annual energy input including amortized embodied."""
        return self.energy_input_kwh_year + self.annualized_embodied
    
    @property
    def component_eroei(self) -> float:
        """EROEI for this component alone."""
        if self.total_annual_input <= 0:
            return float('inf')
        return self.energy_output_kwh_year / self.total_annual_input


@dataclass 
class EnergySystem:
    """Represents a complete energy system with multiple components."""
    name: str
    components: List[EnergyComponent] = field(default_factory=list)
    
    def add_component(self, component: EnergyComponent):
        self.components.append(component)
    
    @property
    def total_output(self) -> float:
        """Total system energy output."""
        return sum(c.energy_output_kwh_year for c in self.components)
    
    @property
    def total_input(self) -> float:
        """Total system energy input."""
        return sum(c.total_annual_input for c in self.components)
    
    @property
    def system_eroei(self) -> float:
        """System-wide EROEI."""
        if self.total_input <= 0:
            return float('inf')
        return self.total_output / self.total_input
    
    @property
    def net_energy(self) -> float:
        """Net energy available for useful work."""
        return self.total_output - self.total_input
    
    def is_viable(self, threshold: float = 7.0) -> bool:
        """Check if system EROEI meets minimum societal threshold."""
        return self.system_eroei >= threshold
    
    def analyze(self) -> Dict:
        """Comprehensive system analysis."""
        component_analysis = []
        for c in self.components:
            component_analysis.append({
                'name': c.name,
                'type': c.component_type.value,
                'output_kwh_year': c.energy_output_kwh_year,
                'input_kwh_year': c.energy_input_kwh_year,
                'embodied_kwh': c.embodied_energy_kwh,
                'lifespan_years': c.lifespan_years,
                'annualized_embodied': c.annualized_embodied,
                'total_annual_input': c.total_annual_input,
                'component_eroei': c.component_eroei,
                'notes': c.notes
            })
        
        # Viability assessment
        eroei = self.system_eroei
        if eroei >= 20:
            viability = "Excellent - Supports complex technology development"
        elif eroei >= 12:
            viability = "Good - Supports education, healthcare, R&D"
        elif eroei >= 7:
            viability = "Marginal - Can maintain infrastructure"
        elif eroei >= 5:
            viability = "Critical - Basic industrial activity only"
        elif eroei >= 3:
            viability = "Subsistence - Basic agriculture only"
        else:
            viability = "Non-viable - Cannot sustain society"
        
        return {
            'system_name': self.name,
            'total_output_kwh_year': self.total_output,
            'total_input_kwh_year': self.total_input,
            'net_energy_kwh_year': self.net_energy,
            'system_eroei': eroei,
            'viability_assessment': viability,
            'meets_7_threshold': self.is_viable(7.0),
            'meets_10_threshold': self.is_viable(10.0),
            'components': component_analysis
        }


def create_example_solar_system() -> EnergySystem:
    """Create an example solar + storage + distribution system."""
    system = EnergySystem(name="Solar PV with Battery Storage")
    
    # 1 MW solar array
    system.add_component(EnergyComponent(
        name="Solar PV Array (1 MW)",
        component_type=EnergyType.SOLAR_PV,
        energy_output_kwh_year=1_500_000,    # ~17% capacity factor
        energy_input_kwh_year=10_000,        # Maintenance, cleaning
        embodied_energy_kwh=1_500_000,       # Manufacturing energy
        lifespan_years=25,
        capacity_factor=0.17,
        notes="Assumes mid-latitude location"
    ))
    
    # Battery storage (4 hours)
    system.add_component(EnergyComponent(
        name="Battery Storage (4 MWh)",
        component_type=EnergyType.BATTERY_STORAGE,
        energy_output_kwh_year=1_350_000,    # After 10% round-trip losses
        energy_input_kwh_year=5_000,         # Thermal management
        embodied_energy_kwh=800_000,         # Battery manufacturing
        lifespan_years=15,
        efficiency=0.90,
        notes="Lithium-ion, 10% round-trip loss"
    ))
    
    # Distribution
    system.add_component(EnergyComponent(
        name="Distribution Network",
        component_type=EnergyType.DISTRIBUTION,
        energy_output_kwh_year=1_282_500,    # After 5% transmission loss
        energy_input_kwh_year=2_000,         # Monitoring, maintenance
        embodied_energy_kwh=200_000,         # Infrastructure
        lifespan_years=40,
        efficiency=0.95,
        notes="Local distribution, 5% loss"
    ))
    
    return system


def create_hyphal_network_system(
    num_nodes: int = 1000,
    power_per_node_w: float = 100,
    network_overhead_factor: float = 1.2
) -> EnergySystem:
    """
    Model energy costs for a distributed Hyphal Network.
    
    This is what Dr. Arnoux is asking: where does the energy come from?
    """
    system = EnergySystem(name=f"Hyphal Network ({num_nodes} nodes)")
    
    # Calculate annual energy for computation
    hours_per_year = 8760
    node_energy_kwh = (power_per_node_w / 1000) * hours_per_year * num_nodes
    network_energy_kwh = node_energy_kwh * (network_overhead_factor - 1)
    
    # Computation nodes (pure consumers)
    system.add_component(EnergyComponent(
        name=f"Computation Nodes ({num_nodes})",
        component_type=EnergyType.COMPUTATION,
        energy_output_kwh_year=0,            # Produces no energy
        energy_input_kwh_year=node_energy_kwh,
        embodied_energy_kwh=num_nodes * 500, # ~500 kWh per node manufacturing
        lifespan_years=5,
        notes="Spirit execution, VUDO VM runtime"
    ))
    
    # Network infrastructure
    system.add_component(EnergyComponent(
        name="Network Infrastructure",
        component_type=EnergyType.NETWORK,
        energy_output_kwh_year=0,            # Produces no energy
        energy_input_kwh_year=network_energy_kwh,
        embodied_energy_kwh=num_nodes * 50,  # Network equipment
        lifespan_years=10,
        notes="P2P communication, consensus"
    ))
    
    return system


def print_analysis(analysis: Dict):
    """Pretty print system analysis."""
    print("\n" + "=" * 70)
    print(f"ENERGY SYSTEM ANALYSIS: {analysis['system_name']}")
    print("=" * 70)
    
    print(f"\nTotal Output:           {analysis['total_output_kwh_year']:,.0f} kWh/year")
    print(f"Total Input:            {analysis['total_input_kwh_year']:,.0f} kWh/year")
    print(f"Net Energy:             {analysis['net_energy_kwh_year']:,.0f} kWh/year")
    print(f"\nSystem EROEI:           {analysis['system_eroei']:.2f}")
    print(f"Viability:              {analysis['viability_assessment']}")
    print(f"Meets 7:1 threshold:    {'YES ✓' if analysis['meets_7_threshold'] else 'NO ✗'}")
    print(f"Meets 10:1 threshold:   {'YES ✓' if analysis['meets_10_threshold'] else 'NO ✗'}")
    
    print("\n" + "-" * 70)
    print("COMPONENT BREAKDOWN")
    print("-" * 70)
    
    for c in analysis['components']:
        print(f"\n{c['name']} ({c['type']})")
        print(f"  Output:           {c['output_kwh_year']:,.0f} kWh/year")
        print(f"  Operational input: {c['input_kwh_year']:,.0f} kWh/year")
        print(f"  Annualized embodied: {c['annualized_embodied']:,.0f} kWh/year")
        print(f"  Total input:      {c['total_annual_input']:,.0f} kWh/year")
        if c['component_eroei'] != float('inf'):
            print(f"  Component EROEI:  {c['component_eroei']:.2f}")
        else:
            print(f"  Component EROEI:  N/A (consumer only)")
        if c['notes']:
            print(f"  Notes: {c['notes']}")


def main():
    parser = argparse.ArgumentParser(description='EROEI Calculator')
    parser.add_argument('--config', type=str, help='Load system from JSON config')
    parser.add_argument('--example', choices=['solar', 'hyphal'], 
                       default='solar', help='Run example system')
    parser.add_argument('--nodes', type=int, default=1000, 
                       help='Number of nodes for hyphal network')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
        # Parse config into system...
        print("Config loading not yet implemented")
        return
    
    if args.example == 'solar':
        system = create_example_solar_system()
        analysis = system.analyze()
        
        if args.json:
            print(json.dumps(analysis, indent=2))
        else:
            print_analysis(analysis)
            print("\n" + "=" * 70)
            print("CONCLUSION: This solar system is viable (EROEI > 7)")
            print("=" * 70)
    
    elif args.example == 'hyphal':
        system = create_hyphal_network_system(num_nodes=args.nodes)
        analysis = system.analyze()
        
        if args.json:
            print(json.dumps(analysis, indent=2))
        else:
            print_analysis(analysis)
            print("\n" + "=" * 70)
            print("CONCLUSION: Hyphal Network is a PURE CONSUMER")
            print("")
            print("This system has EROEI = 0 because it produces no energy.")
            print("It requires an external energy source (autotrophic layer).")
            print("")
            print("To make this viable, you must:")
            print("1. Specify where the energy comes from (solar, wind, grid?)")
            print("2. Calculate the EROEI of that source")
            print("3. Ensure net energy after network costs is positive")
            print("=" * 70)


if __name__ == '__main__':
    main()

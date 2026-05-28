# Ecosystem Health Integration Specification

## Purpose

This document defines how thermodynamic metrics integrate with the `/ecosystem-health` skill, enabling continuous monitoring of the Univrs.io ecosystem's autopoietic closure and energy viability.

**Goal**: Make thermodynamic reality visible, not hideable.

---

## Metrics Configuration

```yaml
# /ecosystem-health thermodynamic integration
# Version: 1.0.0
# Date: 2026-01-02

ecosystem_health:
  name: "Univrs.io Ecosystem Health"
  version: "1.0.0"

  metrics:
    # =========================================================================
    # THERMODYNAMIC VALIDITY
    # =========================================================================
    thermodynamic_validity:
      source: "spirits/eroei-calculator"
      description: "Energy Return on Energy Invested for the ecosystem"
      calculation: |
        EROEI = total_energy_output / total_energy_input
        Where:
          total_energy_output = energy produced by renewable sources
          total_energy_input = operational + amortized embodied energy
      threshold: "eroei >= 7.0"
      warning_threshold: "eroei >= 3.0"
      critical_threshold: "eroei < 3.0"
      unit: "ratio"
      frequency: "daily"

      data_sources:
        - name: "solar_production"
          endpoint: "spirit://univrs/solar-monitor"
          metric: "daily_kwh"

        - name: "node_consumption"
          endpoint: "spirit://univrs/power-meter"
          metric: "daily_kwh"

        - name: "network_overhead"
          calculation: "node_consumption * 0.20"

      assessment_levels:
        - range: [20, null]
          status: "excellent"
          message: "Supports complex technology development"
        - range: [12, 20]
          status: "good"
          message: "Supports education, healthcare, R&D"
        - range: [7, 12]
          status: "viable"
          message: "Can maintain infrastructure"
        - range: [5, 7]
          status: "marginal"
          message: "Basic industrial activity only"
        - range: [3, 5]
          status: "critical"
          message: "Basic agriculture only"
        - range: [0, 3]
          status: "non_viable"
          message: "Cannot sustain operations"

    # =========================================================================
    # NETWORK TOPOLOGY VALIDITY
    # =========================================================================
    network_topology_validity:
      source: "spirits/small-world-metrics"
      description: "Small-world coefficient of the Hyphal Network"
      calculation: |
        sigma = (C / C_random) / (L / L_random)
        Where:
          C = actual clustering coefficient
          L = actual average path length
          C_random = clustering of equivalent random graph
          L_random = path length of equivalent random graph
      threshold: "sigma > 1.0"
      warning_threshold: "sigma > 0.8"
      critical_threshold: "sigma <= 0.5"
      unit: "ratio"
      frequency: "hourly"

      data_sources:
        - name: "network_graph"
          endpoint: "spirit://univrs/network-topology"
          metric: "adjacency_matrix"

        - name: "node_count"
          endpoint: "spirit://univrs/network-stats"
          metric: "active_nodes"

        - name: "edge_count"
          endpoint: "spirit://univrs/network-stats"
          metric: "active_connections"

      supplementary_metrics:
        clustering_coefficient:
          description: "Local clustering (Watts-Strogatz C)"
          threshold: "C > 0.3"
          unit: "ratio"

        average_path_length:
          description: "Mean shortest path between nodes"
          threshold: "L < log(N)"
          unit: "hops"

        degree_distribution:
          description: "Node connectivity distribution"
          expected: "right-skewed (hub structure)"

      assessment_levels:
        - range: [3, null]
          status: "strongly_small_world"
          message: "Excellent small-world properties"
        - range: [1.5, 3]
          status: "small_world"
          message: "Good small-world properties"
        - range: [1, 1.5]
          status: "borderline"
          message: "Minimal small-world properties"
        - range: [0.5, 1]
          status: "weak"
          message: "Weak network topology"
        - range: [0, 0.5]
          status: "random"
          message: "No small-world structure"

    # =========================================================================
    # AUTOPOIETIC CLOSURE
    # =========================================================================
    autopoietic_closure:
      source: "analysis/autopoiesis-audit"
      description: "Percentage of system components self-produced"
      calculation: |
        closure = weighted_sum(component_closure_scores)
        Where each component is assessed for:
          - Can it be produced internally?
          - What external dependencies exist?
          - What is the gap to full closure?
      threshold: "closure_percentage >= 0.5"
      warning_threshold: "closure_percentage >= 0.3"
      critical_threshold: "closure_percentage < 0.2"
      unit: "percentage"
      frequency: "weekly"

      components:
        spirit_production:
          weight: 0.20
          metrics:
            - "spirits_compiled_internally"
            - "total_spirits_produced"
          calculation: "spirits_compiled_internally / total_spirits_produced"

        network_self_healing:
          weight: 0.15
          metrics:
            - "auto_recovered_failures"
            - "total_failures"
          calculation: "auto_recovered_failures / total_failures"

        vm_self_configuration:
          weight: 0.10
          metrics:
            - "auto_configs"
            - "total_config_changes"
          calculation: "auto_configs / total_config_changes"

        energy_self_sufficiency:
          weight: 0.25
          metrics:
            - "energy_from_renewables"
            - "total_energy_consumed"
          calculation: "energy_from_renewables / total_energy_consumed"

        hardware_self_production:
          weight: 0.10
          value: 0.0  # Not achievable, always 0
          note: "Level 2 autopoiesis not feasible"

        protocol_self_evolution:
          weight: 0.10
          metrics:
            - "automated_protocol_updates"
            - "total_protocol_updates"
          calculation: "automated_protocol_updates / total_protocol_updates"

        community_self_sustaining:
          weight: 0.10
          metrics:
            - "organic_developer_joins"
            - "total_developer_joins"
          calculation: "organic_developer_joins / total_developer_joins"

      assessment_levels:
        - range: [0.7, 1.0]
          status: "highly_autopoietic"
          message: "System approaches self-sufficiency"
        - range: [0.5, 0.7]
          status: "partially_autopoietic"
          message: "Significant self-production capability"
        - range: [0.3, 0.5]
          status: "developing"
          message: "Growing self-production capability"
        - range: [0.1, 0.3]
          status: "dependent"
          message: "Largely dependent on external systems"
        - range: [0, 0.1]
          status: "heteronomous"
          message: "Fully dependent on external systems"

    # =========================================================================
    # COMMUNITY FEEDBACK
    # =========================================================================
    community_feedback:
      source: "krzy.ai/critiques"
      description: "Active engagement with external critiques"
      threshold: "active_engagement"
      frequency: "weekly"

      indicators:
        critiques_received:
          description: "Number of substantive critiques"
          source: "krzy.ai/critiques/count"

        critiques_responded:
          description: "Critiques with formal responses"
          source: "krzy.ai/critiques/responded"

        response_time_days:
          description: "Average days to respond"
          threshold: "< 14"

        actions_taken:
          description: "Concrete changes from critiques"
          source: "krzy.ai/critiques/actions"

        learning_initiatives:
          description: "Educational content from critiques"
          source: "learn.univrs.io/from-critiques"

      engagement_score:
        calculation: |
          score = (
            (critiques_responded / critiques_received) * 0.30 +
            (1 - min(response_time_days, 30) / 30) * 0.20 +
            (actions_taken / critiques_responded) * 0.30 +
            (learning_initiatives > 0 ? 0.20 : 0)
          )

      assessment_levels:
        - range: [0.8, 1.0]
          status: "highly_engaged"
          message: "Excellent critique responsiveness"
        - range: [0.5, 0.8]
          status: "engaged"
          message: "Good critique engagement"
        - range: [0.3, 0.5]
          status: "passive"
          message: "Limited critique engagement"
        - range: [0, 0.3]
          status: "unresponsive"
          message: "Poor critique engagement"
```

---

## Dashboard Specification

### Overview Panel

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    UNIVRS.IO ECOSYSTEM HEALTH                              │
│                    Last Updated: 2026-01-02 14:30 UTC                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  THERMODYNAMIC VALIDITY          NETWORK TOPOLOGY                          │
│  ┌────────────────────┐          ┌────────────────────┐                    │
│  │ EROEI: 0.0         │          │ sigma: 0.00        │                    │
│  │ Status: NON-VIABLE │          │ Status: NO DATA    │                    │
│  │ [████████████████] │          │ [                ] │                    │
│  │ Target: >= 7.0     │          │ Target: > 1.0      │                    │
│  └────────────────────┘          └────────────────────┘                    │
│                                                                             │
│  AUTOPOIETIC CLOSURE             COMMUNITY ENGAGEMENT                      │
│  ┌────────────────────┐          ┌────────────────────┐                    │
│  │ Closure: 6%        │          │ Score: 0.75        │                    │
│  │ Status: DEPENDENT  │          │ Status: ENGAGED    │                    │
│  │ [█                ]│          │ [████████████     ]│                    │
│  │ Target: >= 50%     │          │ Target: >= 0.5     │                    │
│  └────────────────────┘          └────────────────────┘                    │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ OVERALL HEALTH: CRITICAL - System requires external energy dependency      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Metrics View

```yaml
# JSON output format for /ecosystem-health
{
  "timestamp": "2026-01-02T14:30:00Z",
  "overall_status": "critical",
  "overall_message": "System requires external energy dependency",

  "metrics": {
    "thermodynamic_validity": {
      "value": 0.0,
      "unit": "ratio",
      "status": "non_viable",
      "message": "Cannot sustain operations",
      "threshold": 7.0,
      "details": {
        "energy_output_kwh": 0,
        "energy_input_kwh": 2880,
        "notes": "No renewable energy integration"
      }
    },

    "network_topology_validity": {
      "value": null,
      "unit": "ratio",
      "status": "no_data",
      "message": "Insufficient nodes for measurement",
      "threshold": 1.0,
      "details": {
        "node_count": 0,
        "minimum_required": 10,
        "notes": "Network not yet deployed"
      }
    },

    "autopoietic_closure": {
      "value": 0.06,
      "unit": "percentage",
      "status": "heteronomous",
      "message": "Fully dependent on external systems",
      "threshold": 0.5,
      "details": {
        "spirit_production": 0.0,
        "network_self_healing": 0.45,
        "vm_self_configuration": 0.30,
        "energy_self_sufficiency": 0.0,
        "hardware_self_production": 0.0,
        "protocol_self_evolution": 0.0,
        "community_self_sustaining": 0.20
      }
    },

    "community_feedback": {
      "value": 0.75,
      "unit": "score",
      "status": "engaged",
      "message": "Good critique engagement",
      "threshold": 0.5,
      "details": {
        "critiques_received": 1,
        "critiques_responded": 1,
        "response_time_days": 1,
        "actions_taken": 1,
        "learning_initiatives": 1,
        "reference": "krzy.ai/critiques/arnoux-2026"
      }
    }
  },

  "roadmap_progress": {
    "milestone_1_1_spirit_compilation": {
      "status": "not_started",
      "target_date": "2026-03-31",
      "progress": 0.0
    },
    "milestone_1_2_self_healing_network": {
      "status": "not_started",
      "target_date": "2026-06-30",
      "progress": 0.0
    },
    "milestone_3_1_first_solar_node": {
      "status": "not_started",
      "target_date": "2026-03-31",
      "progress": 0.0
    }
  },

  "alerts": [
    {
      "severity": "critical",
      "metric": "thermodynamic_validity",
      "message": "EROEI is 0.0, below critical threshold of 3.0",
      "action": "Integrate renewable energy sources"
    },
    {
      "severity": "warning",
      "metric": "autopoietic_closure",
      "message": "Closure at 6%, below target of 50%",
      "action": "Progress on roadmap milestones"
    }
  ]
}
```

---

## Integration with /evolve

The `/evolve` skill triggers skill evolution based on ecosystem health metrics:

```yaml
evolution:
  trigger: "phase_completion OR metric_threshold_crossed"

  rules:
    - name: "thermodynamic_alert"
      condition: "thermodynamic_validity.status == 'critical'"
      action: "prioritize_energy_milestone"
      notification: "Energy integration is critical path"

    - name: "topology_degraded"
      condition: "network_topology_validity.value < 0.8"
      action: "analyze_network_structure"
      notification: "Network losing small-world properties"

    - name: "closure_improving"
      condition: "autopoietic_closure.delta > 0.05"
      action: "update_roadmap_progress"
      notification: "Closure improved by {delta}%"

    - name: "critique_received"
      condition: "community_feedback.critiques_received > previous"
      action: "create_learning_initiative"
      notification: "New critique requires response"

  reporting:
    endpoint: "learn.univrs.io/ecosystem-health/"
    format: "markdown"
    frequency: "weekly"
    include:
      - metric_trends
      - roadmap_progress
      - alert_history
      - improvement_suggestions
```

---

## Spirit Implementation

### EROEI Calculator Spirit

```dol
// spirit://univrs/eroei-calculator
// Version: 1.0.0

domain EROEICalculation {
  entity EnergySource {
    name: String
    type: SourceType
    output_kwh_year: Energy
    input_kwh_year: Energy
    embodied_kwh: Energy
    lifespan_years: Duration
  }

  enum SourceType {
    SOLAR_PV
    WIND
    HYDRO
    BATTERY_STORAGE
    GRID
    COMPUTATION
    NETWORK
  }

  function calculateEROEI(sources: [EnergySource]) -> EROEIResult {
    let totalOutput = sum(s.output_kwh_year for s in sources)
    let totalInput = sum(
      s.input_kwh_year + s.embodied_kwh / s.lifespan_years
      for s in sources
    )

    let eroei = if totalInput > 0 then totalOutput / totalInput else 0.0

    return EROEIResult {
      eroei: eroei,
      total_output: totalOutput,
      total_input: totalInput,
      net_energy: totalOutput - totalInput,
      status: assessViability(eroei)
    }
  }

  function assessViability(eroei: Ratio) -> ViabilityStatus {
    match eroei {
      x if x >= 20 -> Excellent
      x if x >= 12 -> Good
      x if x >= 7  -> Viable
      x if x >= 5  -> Marginal
      x if x >= 3  -> Critical
      _            -> NonViable
    }
  }
}
```

### Small World Metrics Spirit

```dol
// spirit://univrs/small-world-metrics
// Version: 1.0.0

domain SmallWorldAnalysis {
  entity NetworkGraph {
    nodes: [NodeId]
    edges: [(NodeId, NodeId)]
  }

  struct SmallWorldMetrics {
    clustering_coefficient: Ratio      // C
    average_path_length: Number        // L
    random_clustering: Ratio           // C_random
    random_path_length: Number         // L_random
    sigma: Ratio                       // Small-world coefficient
    is_small_world: Boolean
  }

  function analyzeNetwork(graph: NetworkGraph) -> SmallWorldMetrics {
    let n = len(graph.nodes)
    let k = 2 * len(graph.edges) / n  // Average degree

    // Calculate actual metrics
    let C = calculateClustering(graph)
    let L = calculatePathLength(graph)

    // Generate equivalent random graph metrics
    let C_random = k / n
    let L_random = ln(n) / ln(k)

    // Small-world coefficient
    let sigma = (C / C_random) / (L / L_random)

    return SmallWorldMetrics {
      clustering_coefficient: C,
      average_path_length: L,
      random_clustering: C_random,
      random_path_length: L_random,
      sigma: sigma,
      is_small_world: sigma > 1.0
    }
  }

  function calculateClustering(graph: NetworkGraph) -> Ratio {
    // Watts-Strogatz clustering coefficient
    let sum = 0.0
    for node in graph.nodes {
      let neighbors = getNeighbors(graph, node)
      let possible = len(neighbors) * (len(neighbors) - 1) / 2
      let actual = countEdgesBetween(graph, neighbors)
      sum += if possible > 0 then actual / possible else 0.0
    }
    return sum / len(graph.nodes)
  }

  function calculatePathLength(graph: NetworkGraph) -> Number {
    // BFS-based average shortest path
    let totalPaths = 0.0
    let pathCount = 0
    for source in graph.nodes {
      let distances = bfs(graph, source)
      for (target, dist) in distances {
        if dist < infinity {
          totalPaths += dist
          pathCount += 1
        }
      }
    }
    return totalPaths / pathCount
  }
}
```

### Autopoiesis Monitor Spirit

```dol
// spirit://univrs/autopoiesis-monitor
// Version: 1.0.0

domain AutopoiesisMonitoring {
  struct ClosureMetrics {
    spirit_production: Ratio
    network_self_healing: Ratio
    vm_self_configuration: Ratio
    energy_self_sufficiency: Ratio
    hardware_self_production: Ratio  // Always 0
    protocol_self_evolution: Ratio
    community_self_sustaining: Ratio
    overall_closure: Ratio
  }

  const WEIGHTS = {
    spirit_production: 0.20,
    network_self_healing: 0.15,
    vm_self_configuration: 0.10,
    energy_self_sufficiency: 0.25,
    hardware_self_production: 0.10,
    protocol_self_evolution: 0.10,
    community_self_sustaining: 0.10
  }

  function calculateClosure(metrics: ClosureMetrics) -> Ratio {
    return sum(
      metrics[key] * WEIGHTS[key]
      for key in WEIGHTS.keys
    )
  }

  function assessStatus(closure: Ratio) -> ClosureStatus {
    match closure {
      x if x >= 0.7 -> HighlyAutopoietic
      x if x >= 0.5 -> PartiallyAutopoietic
      x if x >= 0.3 -> Developing
      x if x >= 0.1 -> Dependent
      _             -> Heteronomous
    }
  }

  function generateReport(metrics: ClosureMetrics) -> Report {
    let closure = calculateClosure(metrics)
    let status = assessStatus(closure)

    let gaps = []
    for (key, weight) in WEIGHTS {
      if metrics[key] < 0.5 {
        gaps.push({
          component: key,
          current: metrics[key],
          gap: 0.5 - metrics[key],
          impact: weight * (0.5 - metrics[key])
        })
      }
    }

    return Report {
      overall_closure: closure,
      status: status,
      component_scores: metrics,
      priority_gaps: gaps.sortBy(g => -g.impact),
      recommendations: generateRecommendations(gaps)
    }
  }
}
```

---

## Alerting Configuration

```yaml
# Alert configuration for ecosystem health
alerts:
  channels:
    - name: "ecosystem-health-log"
      type: "file"
      path: "/var/log/univrs/ecosystem-health.log"

    - name: "kritik-channel"
      type: "spirit"
      endpoint: "spirit://univrs/kritik-notifier"

  rules:
    - name: "eroei_critical"
      condition: "thermodynamic_validity.value < 3.0"
      severity: "critical"
      message: "EROEI below viability threshold"
      channels: ["ecosystem-health-log", "kritik-channel"]
      cooldown: "24h"

    - name: "eroei_warning"
      condition: "thermodynamic_validity.value < 7.0 AND thermodynamic_validity.value >= 3.0"
      severity: "warning"
      message: "EROEI below optimal threshold"
      channels: ["ecosystem-health-log"]
      cooldown: "72h"

    - name: "network_degraded"
      condition: "network_topology_validity.value < 1.0"
      severity: "warning"
      message: "Network losing small-world properties"
      channels: ["ecosystem-health-log"]
      cooldown: "6h"

    - name: "closure_regressed"
      condition: "autopoietic_closure.delta < -0.05"
      severity: "warning"
      message: "Autopoietic closure regressed"
      channels: ["ecosystem-health-log", "kritik-channel"]
      cooldown: "24h"

    - name: "critique_unresponded"
      condition: "community_feedback.response_time_days > 14"
      severity: "info"
      message: "Critique awaiting response"
      channels: ["ecosystem-health-log"]
      cooldown: "24h"
```

---

## Implementation Checklist

### Phase 1: Core Metrics (Q1 2026)

- [ ] Deploy EROEI Calculator Spirit
- [ ] Deploy Small World Metrics Spirit
- [ ] Deploy Autopoiesis Monitor Spirit
- [ ] Create /ecosystem-health skill command
- [ ] Implement basic dashboard

### Phase 2: Data Collection (Q2 2026)

- [ ] Integrate solar monitor data sources
- [ ] Implement network topology crawler
- [ ] Create critique tracking database
- [ ] Set up metric storage (time series)

### Phase 3: Alerting & Evolution (Q3 2026)

- [ ] Configure alert channels
- [ ] Integrate with /evolve skill
- [ ] Create weekly reporting pipeline
- [ ] Implement trend analysis

### Phase 4: Public Dashboard (Q4 2026)

- [ ] Deploy at learn.univrs.io/ecosystem-health
- [ ] Create public API for metrics
- [ ] Enable community contributions
- [ ] Document interpretation guide

---

## References

1. autopoiesis-audit.md - Current closure assessment
2. autopoiesis-roadmap.md - Improvement milestones
3. eroei_calculator.py - Python reference implementation
4. small_world_metrics.py - Python reference implementation
5. thermodynamic-economics-swarm.yaml - Initiative structure

---

*Specification Date: 2026-01-02*
*Version: 1.0.0*
*Status: Draft*

# Game AI & NPC Behavior

## Patterns

### **Behavior Tree Design**
  #### **Name**
Modular Behavior Tree Architecture
  #### **Description**
Design BTs with reusable subtrees and clear node responsibilities
  #### **When**
Building behavior trees for NPCs
  #### **Implementation**
    ```
    // PATTERN: Separate concerns into subtrees
    BehaviorTree EnemyAI {
      Selector {
        // Priority 1: Immediate threats
        Subtree(CombatBehavior)
    
        // Priority 2: Investigation
        Subtree(InvestigateBehavior)
    
        // Priority 3: Patrol/Idle
        Subtree(PatrolBehavior)
      }
    }
    
    // Each subtree is self-contained and testable
    Subtree CombatBehavior {
      Sequence {
        Condition(HasTarget)
        Selector {
          Sequence {
            Condition(InAttackRange)
            Action(Attack)
          }
          Sequence {
            Condition(CanSeeTarget)
            Action(MoveToTarget)
          }
          Action(SearchForTarget)
        }
      }
    }
    ```
    
### **Hierarchical State Machine**
  #### **Name**
Hierarchical FSM with Clean Transitions
  #### **Description**
Use HFSM to manage complexity while keeping states focused
  #### **When**
State machine would have too many transitions
  #### **Implementation**
    ```csharp
    // PATTERN: Hierarchical states reduce transition explosion
    public class CombatState : State {
        // Sub-states handle combat specifics
        private StateMachine combatSubFSM;
    
        public override void Enter() {
            combatSubFSM = new StateMachine();
            combatSubFSM.AddState(new ApproachState());
            combatSubFSM.AddState(new AttackState());
            combatSubFSM.AddState(new RetreatState());
            combatSubFSM.SetInitialState<ApproachState>();
        }
    
        public override void Update() {
            // Global combat transitions checked first
            if (!HasTarget) {
                machine.TransitionTo<IdleState>();
                return;
            }
    
            // Then delegate to sub-FSM
            combatSubFSM.Update();
        }
    }
    ```
    
### **Goap Action Design**
  #### **Name**
GOAP with Preconditions and Effects
  #### **Description**
Design atomic actions with clear world state dependencies
  #### **When**
Building goal-oriented AI that plans sequences
  #### **Implementation**
    ```csharp
    // PATTERN: Atomic actions with explicit preconditions/effects
    public class AttackAction : GOAPAction {
        public override float Cost => 1.0f;
    
        public override Dictionary<string, bool> Preconditions => new() {
            { "hasWeapon", true },
            { "targetVisible", true },
            { "inAttackRange", true }
        };
    
        public override Dictionary<string, bool> Effects => new() {
            { "targetDead", true }
        };
    
        public override bool CheckProceduralPrecondition(Agent agent) {
            // Runtime checks that can't be in world state
            return agent.Weapon.HasAmmo &&
                   !agent.IsStunned;
        }
    }
    
    // Goals define desired end state
    public class KillEnemyGoal : GOAPGoal {
        public override Dictionary<string, bool> DesiredState => new() {
            { "targetDead", true }
        };
    
        public override float Priority(Agent agent) {
            // Dynamic priority based on context
            return agent.IsInCombat ? 1.0f : 0.0f;
        }
    }
    ```
    
### **Utility Ai Curves**
  #### **Name**
Utility AI with Response Curves
  #### **Description**
Use mathematical curves to score decisions naturally
  #### **When**
Need nuanced decision making beyond binary conditions
  #### **Implementation**
    ```csharp
    // PATTERN: Response curves for natural decision scoring
    public class UtilityAI {
        public class Consideration {
            public Func<Agent, float> InputFunction;  // 0-1 normalized
            public AnimationCurve ResponseCurve;       // Transforms input
    
            public float Score(Agent agent) {
                float input = Mathf.Clamp01(InputFunction(agent));
                return ResponseCurve.Evaluate(input);
            }
        }
    
        public class Action {
            public List<Consideration> Considerations;
            public float BaseWeight = 1.0f;
    
            public float Score(Agent agent) {
                // Geometric mean prevents one 0 from killing action
                float product = BaseWeight;
                int count = 0;
    
                foreach (var c in Considerations) {
                    float score = c.Score(agent);
                    if (score <= 0) return 0; // Hard fail
                    product *= score;
                    count++;
                }
    
                // Compensation factor for number of considerations
                float modFactor = 1.0f - (1.0f / count);
                float makeUpValue = (1.0f - product) * modFactor;
                return product + (makeUpValue * product);
            }
        }
    }
    
    // Usage: Attack when health high, distance close
    var attackAction = new Action {
        Considerations = new List<Consideration> {
            new() {
                InputFunction = a => a.Health / a.MaxHealth,
                ResponseCurve = CreateLogisticCurve(k: 5, midpoint: 0.3f)
            },
            new() {
                InputFunction = a => 1f - (a.DistanceToTarget / a.MaxRange),
                ResponseCurve = CreateExponentialCurve(exponent: 2)
            }
        }
    };
    ```
    
### **Astar Optimization**
  #### **Name**
Optimized A* with Proper Heuristics
  #### **Description**
Implement A* with performance considerations
  #### **When**
Implementing grid or graph-based pathfinding
  #### **Implementation**
    ```csharp
    // PATTERN: Optimized A* with tie-breaking
    public class AStarPathfinder {
        // Use priority queue with proper tie-breaking
        private PriorityQueue<Node, float> openSet;
        private Dictionary<Node, float> gScores;
    
        public List<Node> FindPath(Node start, Node goal) {
            openSet = new PriorityQueue<Node, float>();
            gScores = new Dictionary<Node, float>();
            var cameFrom = new Dictionary<Node, Node>();
    
            gScores[start] = 0;
            float h = Heuristic(start, goal);
            // Tie-breaker: prefer nodes closer to goal
            float tieBreaker = 1.0f + (1.0f / 1000.0f);
            openSet.Enqueue(start, h * tieBreaker);
    
            while (openSet.Count > 0) {
                var current = openSet.Dequeue();
    
                if (current == goal)
                    return ReconstructPath(cameFrom, current);
    
                foreach (var neighbor in current.Neighbors) {
                    float tentativeG = gScores[current] +
                                      Cost(current, neighbor);
    
                    if (!gScores.ContainsKey(neighbor) ||
                        tentativeG < gScores[neighbor]) {
                        cameFrom[neighbor] = current;
                        gScores[neighbor] = tentativeG;
                        float f = tentativeG +
                                 Heuristic(neighbor, goal) * tieBreaker;
                        openSet.Enqueue(neighbor, f);
                    }
                }
            }
            return null; // No path
        }
    
        // Octile distance for 8-directional grids
        private float Heuristic(Node a, Node b) {
            float dx = Math.Abs(a.X - b.X);
            float dy = Math.Abs(a.Y - b.Y);
            return Math.Max(dx, dy) + 0.414f * Math.Min(dx, dy);
        }
    }
    ```
    
### **Steering Behaviors**
  #### **Name**
Combined Steering Behaviors
  #### **Description**
Blend multiple steering forces for natural movement
  #### **When**
Implementing smooth NPC movement and avoidance
  #### **Implementation**
    ```csharp
    // PATTERN: Weighted steering behavior blending
    public class SteeringAgent {
        public Vector3 Position;
        public Vector3 Velocity;
        public float MaxSpeed = 5f;
        public float MaxForce = 10f;
    
        public Vector3 CalculateSteering() {
            Vector3 steering = Vector3.zero;
    
            // Priority-weighted blending
            steering += Seek(target) * 1.0f;
            steering += ObstacleAvoidance() * 2.0f;  // Higher priority
            steering += Separation(neighbors) * 1.5f;
            steering += Alignment(neighbors) * 0.5f;
            steering += Cohesion(neighbors) * 0.3f;
    
            // Clamp total force
            if (steering.magnitude > MaxForce)
                steering = steering.normalized * MaxForce;
    
            return steering;
        }
    
        private Vector3 Seek(Vector3 target) {
            Vector3 desired = (target - Position).normalized * MaxSpeed;
            return desired - Velocity;
        }
    
        private Vector3 ObstacleAvoidance() {
            // Raycast ahead
            float lookAhead = Velocity.magnitude * 0.5f + 2f;
            if (Physics.SphereCast(Position, 0.5f, Velocity.normalized,
                                   out var hit, lookAhead)) {
                // Steer away from obstacle
                Vector3 avoidDir = Vector3.Cross(Vector3.up, hit.normal);
                float urgency = 1f - (hit.distance / lookAhead);
                return avoidDir * MaxForce * urgency;
            }
            return Vector3.zero;
        }
    }
    ```
    
### **Perception System**
  #### **Name**
Efficient AI Perception System
  #### **Description**
Implement sight, sound, and memory with performance in mind
  #### **When**
NPCs need to detect and track player/entities
  #### **Implementation**
    ```csharp
    // PATTERN: Perception with staggered updates and memory
    public class PerceptionSystem {
        public float SightRange = 20f;
        public float SightAngle = 120f;
        public float HearingRange = 15f;
        public float MemoryDuration = 5f;
    
        private Dictionary<Entity, PerceptionRecord> memory = new();
        private int updateFrame = 0;
    
        public void Update(Entity self, List<Entity> potentialTargets) {
            // Stagger perception checks across frames
            updateFrame++;
            if (updateFrame % 3 != self.Id % 3) return;
    
            foreach (var target in potentialTargets) {
                var record = GetOrCreateRecord(target);
    
                // Visual detection
                if (CanSee(self, target)) {
                    record.LastSeenPosition = target.Position;
                    record.LastSeenTime = Time.time;
                    record.Awareness = Mathf.Min(1f, record.Awareness + 0.3f);
                    record.IsVisible = true;
                } else {
                    record.IsVisible = false;
                    record.Awareness -= Time.deltaTime * 0.1f;
                }
    
                // Expire old memories
                if (Time.time - record.LastSeenTime > MemoryDuration) {
                    record.Awareness = 0;
                }
            }
        }
    
        private bool CanSee(Entity self, Entity target) {
            Vector3 toTarget = target.Position - self.Position;
            float distance = toTarget.magnitude;
    
            if (distance > SightRange) return false;
    
            float angle = Vector3.Angle(self.Forward, toTarget);
            if (angle > SightAngle / 2) return false;
    
            // Line of sight check (expensive, do last)
            return !Physics.Linecast(self.EyePosition,
                                     target.Position,
                                     obstacleMask);
        }
    }
    
    public class PerceptionRecord {
        public Vector3 LastSeenPosition;
        public float LastSeenTime;
        public float Awareness;  // 0-1, builds up over time
        public bool IsVisible;
    }
    ```
    
### **Blackboard Pattern**
  #### **Name**
Blackboard for AI Knowledge Sharing
  #### **Description**
Centralized data store for behavior tree and AI decisions
  #### **When**
Multiple AI systems need to share state
  #### **Implementation**
    ```csharp
    // PATTERN: Type-safe blackboard with events
    public class Blackboard {
        private Dictionary<string, object> data = new();
        private Dictionary<string, List<Action<object>>> observers = new();
    
        public void Set<T>(string key, T value) {
            data[key] = value;
            NotifyObservers(key, value);
        }
    
        public T Get<T>(string key, T defaultValue = default) {
            if (data.TryGetValue(key, out var value) && value is T typed)
                return typed;
            return defaultValue;
        }
    
        public bool Has(string key) => data.ContainsKey(key);
    
        public void Observe(string key, Action<object> callback) {
            if (!observers.ContainsKey(key))
                observers[key] = new List<Action<object>>();
            observers[key].Add(callback);
        }
    
        private void NotifyObservers(string key, object value) {
            if (observers.TryGetValue(key, out var callbacks)) {
                foreach (var cb in callbacks) cb(value);
            }
        }
    }
    
    // Usage with behavior tree
    public class SetTargetNode : BTNode {
        public override NodeState Execute(Blackboard bb) {
            var perception = bb.Get<PerceptionSystem>("perception");
            var target = perception.GetMostThreateningTarget();
    
            if (target != null) {
                bb.Set("currentTarget", target);
                bb.Set("lastKnownPosition", target.Position);
                return NodeState.Success;
            }
            return NodeState.Failure;
        }
    }
    ```
    
### **Tactical Positioning**
  #### **Name**
Tactical Cover and Position Selection
  #### **Description**
AI-driven cover system with scoring
  #### **When**
Combat AI needs to use cover and tactical positions
  #### **Implementation**
    ```csharp
    // PATTERN: Scored cover selection
    public class TacticalSystem {
        public CoverPoint SelectBestCover(Agent agent, Vector3 threat) {
            var candidates = FindCoverPointsInRange(agent.Position, 15f);
    
            CoverPoint best = null;
            float bestScore = float.MinValue;
    
            foreach (var cover in candidates) {
                float score = ScoreCoverPoint(cover, agent, threat);
                if (score > bestScore) {
                    bestScore = score;
                    best = cover;
                }
            }
    
            return best;
        }
    
        private float ScoreCoverPoint(CoverPoint cover, Agent agent,
                                      Vector3 threat) {
            float score = 0;
    
            // Does it block line of sight to threat?
            if (cover.BlocksLineOfSight(threat))
                score += 50;
    
            // Distance from current position (prefer closer)
            float distance = Vector3.Distance(agent.Position, cover.Position);
            score -= distance * 2;
    
            // Flanking angle (prefer side cover)
            Vector3 coverToThreat = (threat - cover.Position).normalized;
            Vector3 coverForward = cover.Forward;
            float flankAngle = Vector3.Angle(coverToThreat, coverForward);
            if (flankAngle > 45 && flankAngle < 135)
                score += 20;  // Good flanking position
    
            // Escape routes
            score += cover.ExitPoints.Count * 5;
    
            // Already occupied penalty
            if (cover.IsOccupied)
                score -= 100;
    
            return score;
        }
    }
    ```
    

## Anti-Patterns

### **God State Machine**
  #### **Name**
Monolithic State Machine
  #### **Description**
Single FSM with dozens of states and hundreds of transitions
  #### **Why Bad**
Impossible to debug, extend, or understand. Transition explosion.
  #### **Example**
    // BAD: 20+ states all at one level
    switch (currentState) {
        case State.Idle: ...
        case State.Walking: ...
        case State.Running: ...
        case State.Attacking: ...
        case State.AttackingMelee: ...
        case State.AttackingRanged: ...
        // 15 more states...
    }
    
  #### **Fix**
Use hierarchical state machine or behavior tree
### **Polling Perception**
  #### **Name**
Per-Frame Full Perception Updates
  #### **Description**
Running expensive perception checks every frame for all AI
  #### **Why Bad**
O(n*m) every frame destroys performance with many NPCs
  #### **Example**
    // BAD: Every AI checks every potential target every frame
    void Update() {
        foreach (var target in allEntities) {
            if (CanSee(target)) {  // Raycast!
                // ...
            }
        }
    }
    
  #### **Fix**
Stagger updates, use spatial partitioning, cache results
### **Synchronous Pathfinding**
  #### **Name**
Blocking Pathfinding Calls
  #### **Description**
Running A* on main thread blocking game loop
  #### **Why Bad**
Causes frame spikes, especially with many simultaneous requests
  #### **Example**
    // BAD: Blocking path request
    void Update() {
        if (needsNewPath) {
            path = pathfinder.FindPath(position, target);  // Blocks!
            needsNewPath = false;
        }
    }
    
  #### **Fix**
Use async pathfinding, request queue, or coroutines
### **Hardcoded Values**
  #### **Name**
Magic Numbers in AI Logic
  #### **Description**
Hardcoded thresholds scattered through AI code
  #### **Why Bad**
Impossible to tune, different for each enemy type
  #### **Example**
    // BAD: Magic numbers everywhere
    if (distance < 5.0f) Attack();
    if (health < 30) Flee();
    if (awareness > 0.7f) Investigate();
    
  #### **Fix**
Use data-driven configs or ScriptableObjects
### **Determinism Ignorance**
  #### **Name**
Non-Deterministic Multiplayer AI
  #### **Description**
Using Random without seed, Time.time, or frame-dependent logic
  #### **Why Bad**
AI behaves differently on each client, causes desync
  #### **Example**
    // BAD: Random without seed
    if (Random.value > 0.5f) Attack();
    
    // BAD: Time-dependent
    if (Time.time > lastAttack + 1.0f) Attack();
    
  #### **Fix**
Use seeded RNG, deterministic time source, run AI on server
### **Over Complicated Bt**
  #### **Name**
Deep Nested Behavior Trees
  #### **Description**
BTs with 10+ levels of nesting and unclear control flow
  #### **Why Bad**
Hard to debug, visualize, and maintain
  #### **Example**
    // BAD: Excessive nesting
    Selector {
      Sequence {
        Selector {
          Sequence {
            Selector {
              // 5 more levels...
            }
          }
        }
      }
    }
    
  #### **Fix**
Use subtrees, flatten where possible, max 4-5 levels deep
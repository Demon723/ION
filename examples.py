"""
ION Example Intent Specifications
Demonstrating the 7 Impossibilities and core ION features
Based on ION Research & Code Compendium

Developer: ADITYA KAMBLE
"""

from intent_system import (
    IntentSpecification, IntentType, Constraint, ConstraintType,
    Endpoint, Invariant, TemporalHandler, QuantumHandler,
    NeuralSymbolicHandler, AntifragileHandler, SpatialHandler,
    IntentRegistry, IntentVerifier, create_api_intent, create_temporal_intent
)
from ion_compiler import IONCompiler
from deterministic_verification import (
    DeterministicVerifier, SecurityPolicy, SecurityLevel, ResourceEnvelope
)


def example_1_basic_api_intent():
    """Example 1: Basic API Intent - User Service"""
    print("Example 1: Basic API Intent - User Service")
    print("=" * 50)
    
    user_service = create_api_intent(
        name="UserService",
        endpoints=[
            {'method': 'get', 'path': '/users', 'function': 'list_all'},
            {'method': 'post', 'path': '/users', 'function': 'create_user'},
            {'method': 'get', 'path': '/users/{id}', 'function': 'get_user'},
            {'method': 'delete', 'path': '/users/{id}', 'function': 'delete_user'}
        ],
        constraints=[
            {'name': 'auth', 'type': 'auth', 'value': 'jwt'},
            {'name': 'rate', 'type': 'rate', 'value': '100/min'},
            {'name': 'memory', 'type': 'memory', 'value': '64MB'}
        ]
    )
    
    # Add invariants
    user_service.invariants.append(Invariant(
        condition="user.email is unique",
        description="Email addresses must be unique across all users",
        priority=1
    ))
    user_service.invariants.append(Invariant(
        condition="user.age >= 0",
        description="User age cannot be negative",
        priority=1
    ))
    
    user_service.description = "User management service with authentication and rate limiting"
    
    print(user_service.to_json())
    print()
    return user_service


def example_2_temporal_awareness():
    """Example 2: Temporal Awareness - Financial System"""
    print("Example 2: Temporal Awareness - Financial System")
    print("=" * 50)
    
    financial_system = IntentSpecification(
        name="FinancialSystem",
        intent_type=IntentType.TEMPORAL,
        description="Financial trading system with temporal causality guarantees"
    )
    
    # Add temporal handler
    market_handler = TemporalHandler(
        trigger="when market_opens",
        causality_checks=[
            "future.price does_not_exceed constraint.max_drawdown",
            "future.volume implies future.liquidity > threshold"
        ],
        rollback_capability=True,
        branch_analysis=True
    )
    financial_system.temporal_handlers.append(market_handler)
    
    # Add anomaly handler
    anomaly_handler = TemporalHandler(
        trigger="on anomaly_detected",
        causality_checks=[
            "state_at(t - 3600s) is consistent",
            "branch.outcome is comparable to actual.outcome"
        ],
        rollback_capability=True,
        branch_analysis=True
    )
    financial_system.temporal_handlers.append(anomaly_handler)
    
    # Add temporal constraints
    financial_system.constraints.append(Constraint(
        name="temporal_integrity",
        constraint_type=ConstraintType.TEMPORAL,
        value="no_race_conditions across all_timelines"
    ))
    financial_system.constraints.append(Constraint(
        name="causality_preservation",
        constraint_type=ConstraintType.TEMPORAL,
        value="causality_preserved in all_branches"
    ))
    
    # Add invariants
    financial_system.invariants.append(Invariant(
        condition="future.probability_safe > 0.9999",
        description="Trading decisions must have 99.99% safety probability",
        priority=1
    ))
    financial_system.invariants.append(Invariant(
        condition="information_never_flows_backward",
        description="Temporal information must flow forward only",
        priority=1
    ))
    
    print(financial_system.to_json())
    print()
    return financial_system


def example_3_quantum_classical_fusion():
    """Example 3: Quantum-Classical Fusion - Drug Discovery"""
    print("Example 3: Quantum-Classical Fusion - Drug Discovery")
    print("=" * 50)
    
    drug_discovery = IntentSpecification(
        name="DrugDiscovery",
        intent_type=IntentType.QUANTUM,
        description="Drug discovery system using quantum-classical hybrid computing"
    )
    
    # Add quantum handler
    quantum_handler = QuantumHandler(
        classical_component="screen_billions(molecules)",
        quantum_component="optimize_fold(protein)",
        verification_method="verify_result(classical, quantum)",
        budget_constraints={
            'quantum_budget': '< $1000 per_experiment',
            'max_experiments': 100,
            'coherence_threshold': 0.95
        }
    )
    drug_discovery.quantum_handlers.append(quantum_handler)
    
    # Add constraints
    drug_discovery.constraints.append(Constraint(
        name="toxicity_constraint",
        constraint_type=ConstraintType.QUANTUM,
        value="toxicity < 0.01"
    ))
    drug_discovery.constraints.append(Constraint(
        name="synthesizability",
        constraint_type=ConstraintType.QUANTUM,
        value="synthesizable: true"
    ))
    
    # Add invariants
    drug_discovery.invariants.append(Invariant(
        condition="quantum_result.classical_simulation_matches",
        description="Quantum results must match classical simulations",
        priority=1
    ))
    drug_discovery.invariants.append(Invariant(
        condition="no_decoherence_artifacts",
        description="Results must be free from quantum decoherence artifacts",
        priority=1
    ))
    
    print(drug_discovery.to_json())
    print()
    return drug_discovery


def example_4_neural_symbolic_continuum():
    """Example 4: Neural-Symbolic Continuum - Autonomous Vehicle"""
    print("Example 4: Neural-Symbolic Continuum - Autonomous Vehicle")
    print("=" * 50)
    
    autonomous_vehicle = IntentSpecification(
        name="AutonomousVehicle",
        intent_type=IntentType.NEURAL_SYMBOLIC,
        description="Autonomous vehicle with neural policy and symbolic verification"
    )
    
    # Add neural-symbolic handler
    ns_handler = NeuralSymbolicHandler(
        neural_component="neural_policy(state)",
        symbolic_component="symbolic_planner(state)",
        verification_criteria=[
            "no_collision_in_5s(action)",
            "lane_change_legal(action)",
            "traffic_rules_obeyed(action)"
        ],
        fallback_mechanism="symbolic_planner(state)"
    )
    autonomous_vehicle.neural_symbolic_handlers.append(ns_handler)
    
    # Add critical invariants
    autonomous_vehicle.invariants.append(Invariant(
        condition="never_hit_pedestrian",
        description="Vehicle must never collide with pedestrians",
        priority=1
    ))
    autonomous_vehicle.invariants.append(Invariant(
        condition="always_stop_at_red",
        description="Vehicle must always stop at red lights",
        priority=1
    ))
    autonomous_vehicle.invariants.append(Invariant(
        condition="rejection_rate < 0.0001",
        description="Neural policy rejection rate must be extremely low",
        priority=2
    ))
    
    # Add learning handler
    learning_handler = NeuralSymbolicHandler(
        neural_component="vision_model(camera_feed)",
        symbolic_component="predict_driver_behavior(lidar)",
        verification_criteria=["spatial_awareness", "temporal_consistency"],
        fallback_mechanism="emergency_brake()"
    )
    autonomous_vehicle.neural_symbolic_handlers.append(learning_handler)
    
    print(autonomous_vehicle.to_json())
    print()
    return autonomous_vehicle


def example_5_antifragile_architecture():
    """Example 5: Antifragile Architecture - Distributed System"""
    print("Example 5: Antifragile Architecture - Distributed System")
    print("=" * 50)
    
    distributed_system = IntentSpecification(
        name="DistributedSystem",
        intent_type=IntentType.ANTIFRAGILE,
        description="Self-strengthening distributed system that learns from attacks"
    )
    
    # Add antifragile handlers
    ddos_handler = AntifragileHandler(
        stress_condition="ddos_attack",
        response_strategy="absorb load into honeypot_shards, analyze attack_pattern, generate countermeasure",
        learning_mechanism="deploy immunization to all_nodes",
        improvement_metric="system_now_resists_10x_attack"
    )
    distributed_system.antifragile_handlers.append(ddos_handler)
    
    leak_handler = AntifragileHandler(
        stress_condition="memory_leak_detected",
        response_strategy="isolate leaking_component, clone healthy_state from twin, patch leak",
        learning_mechanism="system_now_immune_to_that_leak",
        improvement_metric="memory_stability_improved"
    )
    distributed_system.antifragile_handlers.append(leak_handler)
    
    # Add entropy reduction handler
    entropy_handler = AntifragileHandler(
        stress_condition="entropy_increasing",
        response_strategy="restructure_architecture, consolidate_knowledge, prune dead_code",
        learning_mechanism="system_becomes_more_efficient",
        improvement_metric="entropy_decreased"
    )
    distributed_system.antifragile_handlers.append(entropy_handler)
    
    # Add invariants
    distributed_system.invariants.append(Invariant(
        condition="system_entropy decreases_over_time",
        description="System must become more ordered over time",
        priority=1
    ))
    distributed_system.invariants.append(Invariant(
        condition="performance improves_over_time",
        description="System performance must improve through learning",
        priority=2
    ))
    
    print(distributed_system.to_json())
    print()
    return distributed_system


def example_6_reality_first_spatial():
    """Example 6: Reality-First Spatial - Smart Factory"""
    print("Example 6: Reality-First Spatial - Smart Factory")
    print("=" * 50)
    
    smart_factory = IntentSpecification(
        name="SmartFactory",
        intent_type=IntentType.SPATIAL,
        description="Smart factory with 3D spatial safety constraints"
    )
    
    # Add spatial handler
    spatial_handler = SpatialHandler(
        entities=[
            {
                'type': 'robot_arm',
                'position': {'x': 12, 'y': 5, 'z': 0, 'unit': 'm'},
                'intent': 'weld_chassis',
                'safety_zone': {'type': 'sphere', 'radius': 2, 'unit': 'm'}
            },
            {
                'type': 'human_worker',
                'position': {'x': 8, 'y': 5, 'z': 0, 'unit': 'm'},
                'intent': 'inspect_weld'
            }
        ],
        safety_zones=[
            {'type': 'exclusion_zone', 'coordinates': [(10, 5, 0), (14, 7, 2)], 'description': 'Robot operating area'}
        ],
        spatial_constraints=[
            "robot_arm.safety_zone never_intersects human_worker",
            "human_worker maintains 2m distance from robot_arm",
            "emergency_stop activates when distance < 1.5m"
        ]
    )
    smart_factory.spatial_handlers.append(spatial_handler)
    
    # Add spatial constraints
    smart_factory.constraints.append(Constraint(
        name="spatial_separation",
        constraint_type=ConstraintType.SPATIAL,
        value="minimum_distance: 2.0m"
    ))
    
    # Add invariants
    smart_factory.invariants.append(Invariant(
        condition="no_spatial_violations",
        description="Spatial constraints must never be violated",
        priority=1
    ))
    smart_factory.invariants.append(Invariant(
        condition="emergency_stop_available",
        description="Emergency stop must always be available",
        priority=1
    ))
    
    print(smart_factory.to_json())
    print()
    return smart_factory


def example_7_entropy_reversal():
    """Example 7: Entropy Reversal - Living System"""
    print("Example 7: Entropy Reversal - Living System")
    print("=" * 50)
    
    living_system = IntentSpecification(
        name="LivingSystem",
        intent_type=IntentType.ENTROPY_REVERSAL,
        description="Self-improving system that becomes more ordered over time"
    )
    
    # Add antifragile handlers for entropy reversal
    evolution_handler = AntifragileHandler(
        stress_condition="every transaction",
        response_strategy="extract pattern, generalize to principle, update intent_specification",
        learning_mechanism="regenerate optimized_code",
        improvement_metric="understanding_deepens"
    )
    living_system.antifragile_handlers.append(evolution_handler)
    
    # Add lifecycle handlers
    lifecycle_handler = AntifragileHandler(
        stress_condition="system_lifecycle",
        response_strategy="birth -> growth -> maturity -> wisdom",
        learning_mechanism="teach_other_systems",
        improvement_metric="collective_intelligence_increases"
    )
    living_system.antifragile_handlers.append(lifecycle_handler)
    
    # Add evolution constraints
    living_system.constraints.append(Constraint(
        name="evolution_direction",
        constraint_type=ConstraintType.RESOURCE,
        value="entropy_decreases_over_time"
    ))
    
    # Add invariants
    living_system.invariants.append(Invariant(
        condition="bug_rate decreases_over_time",
        description="System must become more reliable over time",
        priority=1
    ))
    living_system.invariants.append(Invariant(
        condition="performance improves_over_time",
        description="System must become more efficient over time",
        priority=2
    ))
    living_system.invariants.append(Invariant(
        condition="understanding deepens_over_time",
        description="System understanding must improve through experience",
        priority=2
    ))
    
    print(living_system.to_json())
    print()
    return living_system


def example_8_full_compilation_workflow():
    """Example 8: Full compilation workflow with verification"""
    print("Example 8: Full Compilation Workflow")
    print("=" * 50)
    
    # Create compiler and verifier
    compiler = IONCompiler()
    verifier = DeterministicVerifier()
    
    # Create a comprehensive intent
    user_service = example_1_basic_api_intent()
    
    # Register intent
    registry = IntentRegistry()
    intent_hash = registry.register_intent(user_service)
    print(f"Intent registered with hash: {intent_hash[:16]}...")
    
    # Run verification
    status, proof, results = verifier.verify_intent(user_service)
    print(f"\nVerification Status: {status.value}")
    print(f"Proof Certificate Generated: {proof is not None}")
    
    # Compile the intent
    ion_source = """
intent UserService:
    get /users -> list_all()
    post /users -> create_user(body)
    
    constraint auth: jwt
    constraint rate: 100/min
    constraint memory: < 64MB
"""
    
    compilation_result = compiler.compile_source(ion_source)
    print(f"\nCompilation Success: {compilation_result.success}")
    print(f"Phases Completed: {[p.value for p in compilation_result.phases_completed]}")
    print(f"Compilation Time: {compilation_result.compilation_time_ms}ms")
    print(f"Artifacts Generated: {list(compilation_result.generated_artifacts.keys())}")
    
    if compilation_result.intent_bundle:
        print(f"\nIntent Bundle:")
        print(f"  Version: {compilation_result.intent_bundle.version}")
        print(f"  Signature: {compilation_result.intent_bundle.signature[:16]}...")
    
    print("\nGenerated Documentation Preview:")
    doc = compilation_result.generated_artifacts.get('documentation', '')
    print(doc[:500] + "..." if len(doc) > 500 else doc)
    
    print()
    return compilation_result


def example_9_security_policy_enforcement():
    """Example 9: Security policy enforcement"""
    print("Example 9: Security Policy Enforcement")
    print("=" * 50)
    
    from deterministic_verification import SecurityEnforcer
    
    # Create verifier and enforcer
    verifier = DeterministicVerifier()
    enforcer = SecurityEnforcer(verifier)
    
    # Apply NASA-grade security policy
    nasa_policy = SecurityPolicy(
        name="nasa_std_8719",
        level=SecurityLevel.CRITICAL,
        policies=[
            "formal_verification_required",
            "memory_safety_mandatory",
            "information_flow_control",
            "trusted_components_only",
            "authentication_required"
        ],
        enforcement="compile_time"
    )
    enforcer.apply_policy(nasa_policy)
    
    # Create intent
    user_service = example_1_basic_api_intent()
    
    # Enforce policies
    violations = enforcer.enforce_compile_time(user_service)
    
    print(f"Security Policy: {nasa_policy.name}")
    print(f"Security Level: {nasa_policy.level.value}")
    print(f"Policy Violations: {len(violations)}")
    
    if violations:
        print("Violations:")
        for violation in violations:
            print(f"  - {violation}")
    else:
        print("No policy violations - intent is compliant")
    
    print()


def example_10_resource_monitoring():
    """Example 10: Resource monitoring and enforcement"""
    print("Example 10: Resource Monitoring")
    print("=" * 50)
    
    from deterministic_verification import ResourceMonitor
    
    # Create resource envelope
    envelope = ResourceEnvelope(
        max_memory_mb=64,
        max_cpu_time_ms=1000,
        max_network_io_mb=10,
        max_storage_mb=100,
        max_threads=4
    )
    
    # Create resource monitor
    monitor = ResourceMonitor(envelope)
    
    print("Resource Envelope:")
    print(f"  Max Memory: {envelope.max_memory_mb}MB")
    print(f"  Max CPU Time: {envelope.max_cpu_time_ms}ms")
    print(f"  Max Network I/O: {envelope.max_network_io_mb}MB")
    print(f"  Max Storage: {envelope.max_storage_mb}MB")
    print(f"  Max Threads: {envelope.max_threads}")
    
    print("\nResource Allocation Tests:")
    
    # Test memory allocation
    print(f"  Allocate 32MB memory: {monitor.allocate_resource('memory', 32)}")
    print(f"  Current memory: {monitor.current_usage['memory_mb']}MB")
    
    print(f"  Allocate 64MB memory: {monitor.allocate_resource('memory', 64)}")
    print(f"  Current memory: {monitor.current_usage['memory_mb']}MB")
    
    # Test CPU allocation
    print(f"  Allocate 500ms CPU: {monitor.allocate_resource('cpu', 500)}")
    print(f"  Current CPU time: {monitor.current_usage['cpu_time_ms']}ms")
    
    # Test thread allocation
    print(f"  Allocate 2 threads: {monitor.allocate_resource('threads', 2)}")
    print(f"  Current threads: {monitor.current_usage['threads']}")
    
    print(f"  Allocate 4 threads: {monitor.allocate_resource('threads', 4)}")
    print(f"  Current threads: {monitor.current_usage['threads']}")
    
    print()


def main():
    """Run all examples"""
    print("ION Intent Specification Examples")
    print("Demonstrating the 7 Impossibilities and Core Features")
    print("=" * 60)
    print()
    
    # Run all examples
    example_1_basic_api_intent()
    example_2_temporal_awareness()
    example_3_quantum_classical_fusion()
    example_4_neural_symbolic_continuum()
    example_5_antifragile_architecture()
    example_6_reality_first_spatial()
    example_7_entropy_reversal()
    example_8_full_compilation_workflow()
    example_9_security_policy_enforcement()
    example_10_resource_monitoring()
    
    print("All examples completed successfully!")
    print("ION platform demonstrates space-grade reliability through:")
    print("  ✓ Intent-deterministic development")
    print("  ✓ Formal verification by default")
    print("  ✓ The 7 Impossibilities implementation")
    print("  ✓ Multi-target artifact generation")
    print("  ✓ Comprehensive proof certificates")


if __name__ == "__main__":
    main()
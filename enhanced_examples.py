"""
ION Enhanced Examples
Comprehensive examples demonstrating all enhanced features including:
- Advanced type system
- Domain-specific modules (robotics, quantum, AI/ML, space, IoT, bio, XR)
- Memory model and ownership
- Capability-based security
- Formal verification
- Cross-domain integration

Based on ION Complete Language Specification (August 2026)

Developer: ADITYA KAMBLE
"""

from domain_modules import (
    Domain, RobotController, RobotControlMode, Pose3D, QuantumCircuit, QuantumGate,
    NeuralNetwork, NeuralLayer, Activation, Tensor, OrbitalMechanics, OrbitalElements,
    SensorReading, SensorType, DNASequence, Vector3, domain_registry
)
from memory_model import (
    OwnershipTracker, Mutability, Lifetime, Option, Result, SmartPointer,
    UniquePtr, SharedPtr, LinearType
)
from capability_security import (
    Capability, CapabilityType, Permission, SecurityContext, CapabilityEnforcer,
    CapabilitySpec, create_file_read_capability, create_network_capability
)
from formal_verification import (
    FormalVerifier, ProofObligation, VerificationStatus, VerifiedFunction,
    ModelCheckedFunction, TemporalOperator
)
from cross_domain_integration import (
    CrossDomainCoordinator, DataPacket, Interface, IntegrationPipeline,
    HybridSystem, TemporalSynchronizer, DataFusionEngine, setup_default_adapters
)
import asyncio


def example_1_advanced_type_system():
    """Example 1: Advanced type system features"""
    print("Example 1: Advanced Type System")
    print("=" * 50)
    
    # Option type for null safety
    print("\n1. OPTION TYPE (Null Safety)")
    some_value = Option.some(42)
    none_value = Option.none()
    
    print(f"   Some value: {some_value.unwrap()}")
    print(f"   Unwrap or default: {none_value.unwrap_or(0)}")
    print(f"   Map operation: {some_value.map(lambda x: x * 2).unwrap()}")
    
    # Result type for error handling
    print("\n2. RESULT TYPE (Error Handling)")
    ok_result = Result.ok(42)
    err_result = Result.err("Connection failed")
    
    print(f"   Ok result: {ok_result.unwrap()}")
    print(f"   Err unwrap or: {err_result.unwrap_or(0)}")
    print(f"   Chain operations: {ok_result.map(lambda x: x * 2).and_then(lambda x: Result.ok(x + 10)).unwrap()}")
    
    # Smart pointers
    print("\n3. SMART POINTERS")
    unique = UniquePtr("unique data")
    shared = SharedPtr("shared data")
    
    shared_clone = shared.clone()
    print(f"   Shared pointer ref count: {shared.ref_count}")
    print(f"   Clone ref count: {shared_clone.ref_count}")
    
    # Linear types
    print("\n4. LINEAR TYPES")
    linear = LinearType("linear data", "owner1")
    consumed = linear.consume("owner1")
    print(f"   Consumed linear value: {consumed}")
    print(f"   Linear valid after consumption: {linear.is_valid()}")


def example_2_robotics_module():
    """Example 2: Robotics domain module"""
    print("\nExample 2: Robotics Domain Module")
    print("=" * 50)
    
    # Robot controller
    print("\n1. ROBOT CONTROLLER")
    robot = RobotController(RobotControlMode.POSITION)
    target = Pose3D(1.0, 2.0, 3.0)
    
    control = robot.compute_control(target)
    print(f"   Target position: ({target.x}, {target.y}, {target.z})")
    print(f"   Control output: {control}")
    
    # Distance calculation
    start = Pose3D(0, 0, 0)
    end = Pose3D(3, 4, 0)
    distance = start.distance_to(end)
    print(f"   Distance from start to end: {distance:.2f}")


def example_3_quantum_module():
    """Example 3: Quantum domain module"""
    print("\nExample 3: Quantum Domain Module")
    print("=" * 50)
    
    # Quantum circuit
    print("\n1. QUANTUM CIRCUIT")
    circuit = QuantumCircuit(2, [])
    circuit.add_gate(QuantumGate.H, [0])
    circuit.add_gate(QuantumGate.CNOT, [0, 1])
    circuit.add_gate(QuantumGate.MEASURE, [0])
    
    print(f"   Circuit depth: {circuit.depth()}")
    print(f"   Number of qubits: {circuit.num_qubits}")
    print(f"   OpenQASM output:")
    print(circuit.to_openqasm())


def example_4_ai_ml_module():
    """Example 4: AI/ML domain module"""
    print("\nExample 4: AI/ML Domain Module")
    print("=" * 50)
    
    # Neural network
    print("\n1. NEURAL NETWORK")
    layer1 = NeuralLayer(3, 4, Activation.RELU)
    layer2 = NeuralLayer(4, 2, Activation.SIGMOID)
    
    network = NeuralNetwork([layer1, layer2])
    
    input_data = [1.0, 2.0, 3.0]
    output = network.predict(input_data)
    
    print(f"   Input: {input_data}")
    print(f"   Output: {output}")
    print(f"   Network layers: {len(network.layers)}")
    
    # Tensor operations
    print("\n2. TENSOR OPERATIONS")
    tensor = Tensor((2, 3), [1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    print(f"   Tensor shape: {tensor.shape}")
    print(f"   Tensor data: {tensor.data}")
    print(f"   Get element (0,1): {tensor.get((0, 1))}")


def example_5_space_module():
    """Example 5: Space domain module"""
    print("\nExample 5: Space Domain Module")
    print("=" * 50)
    
    # Orbital mechanics
    print("\n1. ORBITAL MECHANICS")
    orbit = OrbitalElements(
        semi_major_axis=7000,  # km
        eccentricity=0.01,
        inclination=0.5,      # rad
        raan=0.3,             # rad
        arg_periapsis=0.2,    # rad
        true_anomaly=0.1      # rad
    )
    
    period = OrbitalMechanics.orbital_period(orbit.semi_major_axis)
    velocity = OrbitalMechanics.orbital_velocity(orbit)
    
    print(f"   Orbital period: {period:.2f} seconds ({period/60:.2f} minutes)")
    print(f"   Orbital velocity: {velocity:.2f} km/s")
    
    # Attitude control
    print("\n2. ATTITUDE CONTROL")
    from domain_modules import Quaternion, AttitudeControl
    
    q = Quaternion(0.9, 0.1, 0.2, 0.3).normalize()
    roll, pitch, yaw = AttitudeControl.quaternion_to_euler(q)
    
    print(f"   Quaternion: ({q.w:.3f}, {q.x:.3f}, {q.y:.3f}, {q.z:.3f})")
    print(f"   Euler angles: roll={roll:.3f}, pitch={pitch:.3f}, yaw={yaw:.3f}")


def example_6_iot_module():
    """Example 6: IoT domain module"""
    print("\nExample 6: IoT Domain Module")
    print("=" * 50)
    
    # Sensor reading
    print("\n1. SENSOR READING")
    reading = SensorReading(
        sensor_id="temp_001",
        sensor_type=SensorType.TEMPERATURE,
        value=25.5,
        unit="C",
        timestamp=1234567890.0
    )
    
    print(f"   Sensor: {reading.sensor_id}")
    print(f"   Type: {reading.sensor_type.value}")
    print(f"   Value: {reading.value} {reading.unit}")
    
    # Sensor fusion
    print("\n2. SENSOR FUSION")
    from domain_modules import SensorFusion
    
    acc_data = [0.1, 0.2, 0.3]
    gyro_data = [0.05, 0.1, 0.15]
    
    fused = SensorFusion.complementary_filter(acc_data, gyro_data, alpha=0.98)
    print(f"   Accelerometer: {acc_data}")
    print(f"   Gyroscope: {gyro_data}")
    print(f"   Fused data: {fused}")


def example_7_bio_module():
    """Example 7: Bio domain module"""
    print("\nExample 7: Bio Domain Module")
    print("=" * 50)
    
    # DNA sequence
    print("\n1. DNA SEQUENCE")
    dna = DNASequence("ATCGATCGATCG")
    
    print(f"   Sequence: {dna.sequence}")
    print(f"   Complement: {dna.complement()}")
    print(f"   Transcribed: {dna.transcribe()}")
    print(f"   GC content: {dna.gc_content():.1f}%")
    
    # Protein structure
    print("\n2. PROTEIN STRUCTURE")
    from domain_modules import ProteinStructure
    
    sequence = "AILMV"
    hydrophobicity = ProteinStructure.hydrophobicity_index("A")
    structure = ProteinStructure.predict_secondary_structure(sequence)
    
    print(f"   Sequence: {sequence}")
    print(f"   Hydrophobicity of A: {hydrophobicity}")
    print(f"   Predicted structure: {structure}")


def example_8_xr_module():
    """Example 8: XR domain module"""
    print("\nExample 8: XR Domain Module")
    print("=" * 50)
    
    # Vector operations
    print("\n1. VECTOR OPERATIONS")
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(4, 5, 6)
    
    normalized = v1.normalize()
    dot_product = v1.dot(v2)
    cross_product = v1.cross(v2)
    
    print(f"   Vector 1: ({v1.x}, {v1.y}, {v1.z})")
    print(f"   Normalized: ({normalized.x:.3f}, {normalized.y:.3f}, {normalized.z:.3f})")
    print(f"   Dot product: {dot_product}")
    print(f"   Cross product: ({cross_product.x}, {cross_product.y}, {cross_product.z})")
    
    # Ray intersection
    print("\n2. RAY INTERSECTION")
    from domain_modules import XRInput
    
    ray_origin = Vector3(0, 0, 0)
    ray_direction = Vector3(1, 0, 0).normalize()
    triangle = (Vector3(2, -1, 0), Vector3(2, 1, 0), Vector3(2, 0, 1))
    
    intersection = XRInput.ray_intersection(ray_origin, ray_direction, triangle)
    print(f"   Ray intersection: {intersection if intersection else 'None'}")


def example_9_memory_model():
    """Example 9: Memory model and ownership"""
    print("\nExample 9: Memory Model & Ownership")
    print("=" * 50)
    
    # Ownership tracking
    print("\n1. OWNERSHIP TRACKING")
    tracker = OwnershipTracker()
    tracker.enter_scope()
    
    tracker.declare_variable("x", "int", Mutability.IMMUTABLE)
    tracker.declare_variable("y", "int", Mutability.MUTABLE)
    
    tracker.assign_variable("x", 42, size=4)
    tracker.assign_variable("y", 100, size=4)
    
    print(f"   Variables declared: x, y")
    print(f"   Memory usage: {tracker.memory_manager.get_memory_usage()}")
    
    # Borrowing
    print("\n2. BORROW CHECKING")
    tracker.borrow_variable("func1", "x", is_mutable=False)
    print(f"   Successfully borrowed x as immutable")
    
    # Ownership transfer
    print("\n3. OWNERSHIP TRANSFER")
    tracker.move_variable("x", "z")
    print(f"   Moved ownership from x to z")
    
    # Cleanup
    tracker.exit_scope()
    print(f"   Final memory usage: {tracker.memory_manager.get_memory_usage()}")


def example_10_capability_security():
    """Example 10: Capability-based security"""
    print("\nExample 10: Capability-Based Security")
    print("=" * 50)
    
    # Create enforcer
    enforcer = CapabilityEnforcer()
    
    # Create capabilities
    file_cap = create_file_read_capability(["/tmp", "/home/user"])
    network_cap = create_network_capability(["api.example.com"], [443])
    
    # Create security contexts
    user_context = enforcer.create_context("user", [file_cap])
    admin_context = enforcer.create_context("admin", [file_cap, network_cap])
    
    # Register function
    spec = CapabilitySpec(
        required_capabilities=["file_access"],
        required_permissions={CapabilityType.FILE_ACCESS: {Permission.READ}}
    )
    enforcer.register_function("read_file", spec)
    
    # Test access
    print(f"   User has file_access: {user_context.has_capability('file_access')}")
    print(f"   User can access /tmp/file: {enforcer.check_resource_access(user_context, CapabilityType.FILE_ACCESS, Permission.READ, '/tmp/file')}")
    print(f"   User can access /etc/passwd: {enforcer.check_resource_access(user_context, CapabilityType.FILE_ACCESS, Permission.READ, '/etc/passwd')}")
    
    # Audit log
    print(f"   Audit events: {len(enforcer.audit_log)}")


def example_11_formal_verification():
    """Example 11: Formal verification"""
    print("\nExample 11: Formal Verification")
    print("=" * 50)
    
    # Create verifier
    verifier = FormalVerifier()
    
    # Verify function
    result = verifier.verify_function(
        function_name="safe_divide",
        preconditions=["denominator != 0"],
        postconditions=["result == numerator / denominator"],
        variables={"numerator": "Int", "denominator": "Int", "result": "Int"}
    )
    
    print(f"   Function: {result.function_name}")
    print(f"   Status: {result.overall_status.value}")
    print(f"   Conditions: {len(result.conditions)}")
    print(f"   Proof generated: {result.proof_generated}")
    
    # Temporal property
    verifier.add_temporal_property(
        "system_safety",
        "always (temperature < 100)"
    )
    
    mc_result = verifier.model_check_property("system_safety")
    print(f"   Model checking: {mc_result.property_name}")
    print(f"   Satisfied: {mc_result.is_satisfied}")
    
    # Verification summary
    summary = verifier.get_verification_summary()
    print(f"   Summary: {summary}")


def example_12_cross_domain_integration():
    """Example 12: Cross-domain integration"""
    print("\nExample 12: Cross-Domain Integration")
    print("=" * 50)
    
    # Create coordinator
    coordinator = CrossDomainCoordinator()
    setup_default_adapters(coordinator)
    
    # Test conversion
    robot_data = {"joint_1": 45.0, "joint_2": 90.0}
    quantum_params = coordinator.convert_data(robot_data, Domain.ROBOTICS, Domain.QUANTUM)
    print(f"   Robotics -> Quantum: {quantum_params}")
    
    # Create pipeline
    pipeline = IntegrationPipeline(
        name="sensor_to_ai",
        stages=[
            coordinator.adapters[(Domain.IOT, Domain.XR)],
            coordinator.adapters[(Domain.XR, Domain.AI_ML)]
        ]
    )
    coordinator.register_pipeline(pipeline)
    print(f"   Pipeline: {pipeline.name}")
    
    # Temporal sync
    sync = TemporalSynchronizer()
    sync.register_domain_clock(Domain.ROBOTICS, 100.0)
    sync.register_domain_clock(Domain.AI_ML, 100.02)
    adjustments = sync.synchronize(Domain.ROBOTICS)
    print(f"   Sync adjustments: {adjustments}")
    
    # Data fusion
    fusion = DataFusionEngine()
    fusion.register_fusion_strategy("weighted_average", fusion.weighted_average_fusion)
    
    domain_data = {
        Domain.ROBOTICS: {"position": 1.0},
        Domain.AI_ML: {"position": 1.1}
    }
    fused = fusion.fuse_data(domain_data, "weighted_average")
    print(f"   Fused data: {fused}")


def example_13_hybrid_robotics_quantum_ai():
    """Example 13: Hybrid robotics-quantum-AI system"""
    print("\nExample 13: Hybrid Robotics-Quantum-AI System")
    print("=" * 50)
    
    # Create coordinator
    coordinator = CrossDomainCoordinator()
    setup_default_adapters(coordinator)
    
    # Create hybrid system
    hybrid = HybridSystem("quantum_enhanced_robot", coordinator)
    
    # Add components
    robot = RobotController(RobotControlMode.POSITION)
    quantum_circuit = QuantumCircuit(2, [])
    quantum_circuit.add_gate(QuantumGate.H, [0])
    quantum_circuit.add_gate(QuantumGate.CNOT, [0, 1])
    
    neural_layer = NeuralLayer(2, 3, Activation.RELU)
    neural_network = NeuralNetwork([neural_layer])
    
    hybrid.add_component(Domain.ROBOTICS, robot)
    hybrid.add_component(Domain.QUANTUM, quantum_circuit)
    hybrid.add_component(Domain.AI_ML, neural_network)
    
    print(f"   Hybrid system: {hybrid.name}")
    print(f"   Components: {[d.value for d in hybrid.components.keys()]}")
    
    # Simulate data flow
    robot_state = {"joint_1": 30.0, "joint_2": 45.0}
    print(f"   Robot state: {robot_state}")
    
    # Convert robotics to quantum
    quantum_params = coordinator.convert_data(robot_state, Domain.ROBOTICS, Domain.QUANTUM)
    print(f"   Quantum parameters: {quantum_params}")
    
    # Convert quantum to AI
    ai_input = coordinator.convert_data([complex(0.7, 0.7), complex(0.7, -0.7)], 
                                       Domain.QUANTUM, Domain.AI_ML)
    print(f"   AI input: {ai_input}")


def example_14_space_qualified_software():
    """Example 14: Space-qualified software verification"""
    print("\nExample 14: Space-Qualified Software Verification")
    print("=" * 50)
    
    # Create verifier with space-specific requirements
    verifier = FormalVerifier()
    
    # Verify orbital propagation function
    result = verifier.verify_function(
        function_name="propagate_orbit",
        preconditions=[
            "orbit.semi_major_axis > 6371",  # Above Earth's surface
            "orbit.eccentricity >= 0 and orbit.eccentricity < 1"
        ],
        postconditions=[
            "result.semi_major_axis == orbit.semi_major_axis",
            "result.eccentricity == orbit.eccentricity"
        ],
        variables={"orbit": "OrbitalElements", "result": "OrbitalElements", "dt": "Float"}
    )
    
    print(f"   Function: {result.function_name}")
    print(f"   Status: {result.overall_status.value}")
    
    # Add temporal property for attitude control
    verifier.add_temporal_property(
        "attitude_stability",
        "always (angular_velocity < max_angular_velocity)"
    )
    
    mc_result = verifier.model_check_property("attitude_stability")
    print(f"   Attitude stability: {mc_result.is_satisfied}")


def example_15_bio_computing_integration():
    """Example 15: Bio-computing with AI integration"""
    print("\nExample 15: Bio-Computing with AI Integration")
    print("=" * 50)
    
    # DNA sequence analysis
    dna = DNASequence("ATCGATCGATCGATCG")
    print(f"   DNA sequence: {dna.sequence}")
    print(f"   GC content: {dna.gc_content():.1f}%")
    
    # Convert to AI input
    coordinator = CrossDomainCoordinator()
    setup_default_adapters(coordinator)
    
    ai_input = coordinator.convert_data(dna, Domain.BIO, Domain.AI_ML)
    print(f"   AI input length: {len(ai_input)}")
    
    # Simple neural network processing
    layer = NeuralLayer(len(ai_input), 4, Activation.RELU)
    input_tensor = Tensor((len(ai_input),), ai_input)
    output = layer.forward(input_tensor)
    print(f"   Neural output: {output.data}")


def main():
    """Run all enhanced examples"""
    print("ION Enhanced Examples")
    print("Demonstrating Advanced Features from Complete Specification")
    print("=" * 60)
    
    # Run all examples
    example_1_advanced_type_system()
    example_2_robotics_module()
    example_3_quantum_module()
    example_4_ai_ml_module()
    example_5_space_module()
    example_6_iot_module()
    example_7_bio_module()
    example_8_xr_module()
    example_9_memory_model()
    example_10_capability_security()
    example_11_formal_verification()
    example_12_cross_domain_integration()
    example_13_hybrid_robotics_quantum_ai()
    example_14_space_qualified_software()
    example_15_bio_computing_integration()
    
    print("\n" + "=" * 60)
    print("All Enhanced Examples Completed Successfully!")
    print("=" * 60)
    print("\nION Platform now supports:")
    print("  ✓ Advanced type system (Option, Result, smart pointers, linear types)")
    print("  ✓ 7 domain modules (Robotics, Quantum, AI/ML, Space, IoT, Bio, XR)")
    print("  ✓ Memory model with ownership and borrow checking")
    print("  ✓ Capability-based security system")
    print("  ✓ Formal verification with SMT solving and model checking")
    print("  ✓ Cross-domain integration and data fusion")
    print("  ✓ Hybrid systems combining multiple domains")
    print("  ✓ Space-qualified software verification")
    print("  ✓ Bio-computing integration")


if __name__ == "__main__":
    main()
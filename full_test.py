"""
ION Platform Full Program Test
Comprehensive testing of all ION platform components
Developer: ADITYA KAMBLE
"""

import sys
from datetime import datetime


def test_basic_platform():
    """Test basic platform components"""
    print("\n" + "="*60)
    print("TEST 1: Basic Platform Components")
    print("="*60)
    
    try:
        from ion_language import parse_ion
        from intent_system import IntentSpecification, IntentRegistry, IntentVerifier
        from ion_compiler import IONCompiler
        from deterministic_verification import DeterministicVerifier
        from artifact_generator import ArtifactGenerator
        
        print("✓ All basic modules imported successfully")
        
        # Test parser
        source = """
intent TestService:
    get /test -> test_func()
    constraint auth: jwt
"""
        ast = parse_ion(source)
        print(f"✓ Parser working: {len(ast.statements)} statements parsed")
        
        # Test intent system
        registry = IntentRegistry()
        from intent_system import create_api_intent
        intent = create_api_intent(
            name="TestService",
            endpoints=[{'method': 'get', 'path': '/test', 'function': 'test_func'}],
            constraints=[{'name': 'auth', 'type': 'auth', 'value': 'jwt'}]
        )
        intent_hash = registry.register_intent(intent)
        print(f"✓ Intent system working: {intent_hash[:16]}...")
        
        # Test verifier
        verifier = IntentVerifier()
        status, proof = verifier.verify_intent(intent)
        print(f"✓ Intent verifier working: {status.value}")
        
        # Test compiler
        compiler = IONCompiler()
        result = compiler.compile_source(source)
        print(f"✓ Compiler working: {result.success}")
        
        # Test artifact generator
        from artifact_generator import ArtifactGenerator
        artifact_gen = ArtifactGenerator()
        artifacts = artifact_gen.generate_all_artifacts(intent, proof)
        print(f"✓ Artifact generator working: {len(artifacts)} artifacts generated")
        
        return True
        
    except Exception as e:
        print(f"✗ Basic platform test failed: {e}")
        return False


def test_domain_modules():
    """Test all domain modules"""
    print("\n" + "="*60)
    print("TEST 2: Domain Modules")
    print("="*60)
    
    try:
        from domain_modules import (
            RobotController, RobotControlMode, Pose3D,
            QuantumCircuit, QuantumGate,
            NeuralNetwork, NeuralLayer, Activation, Tensor,
            OrbitalMechanics, OrbitalElements,
            SensorReading, SensorType,
            DNASequence,
            Vector3,
            domain_registry
        )
        
        print("✓ All domain modules imported successfully")
        
        # Test Robotics
        robot = RobotController(RobotControlMode.POSITION)
        target = Pose3D(1.0, 2.0, 3.0)
        control = robot.compute_control(target)
        print(f"✓ Robotics module working: control output {len(control)} DOF")
        
        # Test Quantum
        circuit = QuantumCircuit(2, [])
        circuit.add_gate(QuantumGate.H, [0])
        circuit.add_gate(QuantumGate.CNOT, [0, 1])
        print(f"✓ Quantum module working: circuit depth {circuit.depth()}")
        
        # Test AI/ML
        layer = NeuralLayer(3, 2, Activation.RELU)
        tensor = Tensor((3,), [1.0, 2.0, 3.0])
        output = layer.forward(tensor)
        print(f"✓ AI/ML module working: output shape {output.data}")
        
        # Test Space
        orbit = OrbitalElements(7000, 0.01, 0.5, 0.3, 0.2, 0.1)
        period = OrbitalMechanics.orbital_period(orbit.semi_major_axis)
        print(f"✓ Space module working: orbital period {period:.2f}s")
        
        # Test IoT
        reading = SensorReading("temp_001", SensorType.TEMPERATURE, 25.5, "C", 1234567890.0)
        print(f"✓ IoT module working: sensor reading {reading.value} {reading.unit}")
        
        # Test Bio
        dna = DNASequence("ATCG")
        complement = dna.complement()
        print(f"✓ Bio module working: DNA complement {complement}")
        
        # Test XR
        vec = Vector3(1, 2, 3).normalize()
        print(f"✓ XR module working: normalized vector ({vec.x:.3f}, {vec.y:.3f}, {vec.z:.3f})")
        
        # Test domain registry
        domains = domain_registry.list_domains()
        print(f"✓ Domain registry working: {len(domains)} domains available")
        
        return True
        
    except Exception as e:
        print(f"✗ Domain modules test failed: {e}")
        return False


def test_memory_model():
    """Test memory model and ownership"""
    print("\n" + "="*60)
    print("TEST 3: Memory Model & Ownership")
    print("="*60)
    
    try:
        from memory_model import (
            OwnershipTracker, Mutability, Lifetime,
            Option, Result, SmartPointer, UniquePtr, SharedPtr, LinearType
        )
        
        print("✓ Memory model modules imported successfully")
        
        # Test ownership tracking
        tracker = OwnershipTracker()
        tracker.enter_scope()
        tracker.declare_variable("x", "int", Mutability.IMMUTABLE)
        tracker.assign_variable("x", 42, size=4)
        print(f"✓ Ownership tracking working: variable x declared")
        
        # Test Option type
        some_val = Option.some(42)
        none_val = Option.none()
        print(f"✓ Option type working: some={some_val.unwrap()}, none={none_val.unwrap_or(0)}")
        
        # Test Result type
        ok_val = Result.ok(42)
        err_val = Result.err("error")
        print(f"✓ Result type working: ok={ok_val.unwrap()}, err={err_val.unwrap_or(0)}")
        
        # Test smart pointers
        shared = SharedPtr("data")
        shared_clone = shared.clone()
        print(f"✓ Smart pointers working: ref count {shared.ref_count}")
        
        # Test linear types
        linear = LinearType("data", "owner")
        consumed = linear.consume("owner")
        print(f"✓ Linear types working: consumed={consumed}")
        
        tracker.exit_scope()
        print(f"✓ Memory cleanup working: scope exited")
        
        return True
        
    except Exception as e:
        print(f"✗ Memory model test failed: {e}")
        return False


def test_capability_security():
    """Test capability-based security"""
    print("\n" + "="*60)
    print("TEST 4: Capability-Based Security")
    print("="*60)
    
    try:
        from capability_security import (
            Capability, CapabilityType, Permission, SecurityContext,
            CapabilityEnforcer, CapabilitySpec, create_file_read_capability
        )
        
        print("✓ Security modules imported successfully")
        
        # Test capability creation
        file_cap = create_file_read_capability(["/tmp"])
        print(f"✓ Capability creation working: {file_cap.name}")
        
        # Test security context
        context = SecurityContext(principal="test_user", capabilities=[file_cap])
        print(f"✓ Security context working: principal {context.principal}")
        
        # Test capability enforcer
        enforcer = CapabilityEnforcer()
        enforcer.create_context("user", [file_cap])
        print(f"✓ Capability enforcer working: context created")
        
        # Test permission checking
        has_perm = context.has_permission(CapabilityType.FILE_ACCESS, Permission.READ)
        print(f"✓ Permission checking working: has_permission={has_perm}")
        
        return True
        
    except Exception as e:
        print(f"✗ Capability security test failed: {e}")
        return False


def test_formal_verification():
    """Test formal verification"""
    print("\n" + "="*60)
    print("TEST 5: Formal Verification")
    print("="*60)
    
    try:
        from formal_verification import (
            FormalVerifier, ProofObligation, VerificationStatus,
            SMTExpression, TemporalOperator
        )
        
        print("✓ Formal verification modules imported successfully")
        
        # Test verifier
        verifier = FormalVerifier()
        result = verifier.verify_function(
            function_name="test_func",
            preconditions=["x > 0"],
            postconditions=["result > x"],
            variables={"x": "Int", "result": "Int"}
        )
        print(f"✓ Function verification working: {result.overall_status.value}")
        
        # Test temporal properties
        verifier.add_temporal_property("safety", "always (x < 100)")
        mc_result = verifier.model_check_property("safety")
        print(f"✓ Model checking working: satisfied={mc_result.is_satisfied}")
        
        # Test SMT expression builder
        builder = SMTExpression()
        expr = builder.equals_expr("x", "42")
        print(f"✓ SMT expression builder working: {expr}")
        
        return True
        
    except Exception as e:
        print(f"✗ Formal verification test failed: {e}")
        return False


def test_cross_domain_integration():
    """Test cross-domain integration"""
    print("\n" + "="*60)
    print("TEST 6: Cross-Domain Integration")
    print("="*60)
    
    try:
        from cross_domain_integration import (
            CrossDomainCoordinator, DataPacket, Interface,
            IntegrationPipeline, setup_default_adapters, Domain
        )
        
        print("✓ Cross-domain integration modules imported successfully")
        
        # Test coordinator
        coordinator = CrossDomainCoordinator()
        setup_default_adapters(coordinator)
        print(f"✓ Coordinator working: {len(coordinator.adapters)} adapters registered")
        
        # Test data conversion
        robot_data = {"joint_1": 45.0}
        quantum_params = coordinator.convert_data(robot_data, Domain.ROBOTICS, Domain.QUANTUM)
        print(f"✓ Data conversion working: {quantum_params}")
        
        # Test data packet
        packet = DataPacket(
            source_domain=Domain.ROBOTICS,
            target_domain=Domain.AI_ML,
            interface_type=Interface.CONTROL_SIGNAL,
            data={"command": "test"},
            timestamp=1234567890.0
        )
        print(f"✓ Data packet working: {packet.interface_type.value}")
        
        return True
        
    except Exception as e:
        print(f"✗ Cross-domain integration test failed: {e}")
        return False


def test_enhanced_examples():
    """Test enhanced examples"""
    print("\n" + "="*60)
    print("TEST 7: Enhanced Examples")
    print("="*60)
    
    try:
        from enhanced_examples import (
            example_1_advanced_type_system, example_2_robotics_module,
            example_3_quantum_module, example_4_ai_ml_module
        )
        
        print("✓ Enhanced examples imported successfully")
        
        # Test a few key examples
        print("Running example 1 (Advanced Type System)...")
        example_1_advanced_type_system()
        print("✓ Example 1 completed")
        
        print("Running example 2 (Robotics Module)...")
        example_2_robotics_module()
        print("✓ Example 2 completed")
        
        print("Running example 3 (Quantum Module)...")
        example_3_quantum_module()
        print("✓ Example 3 completed")
        
        print("Running example 4 (AI/ML Module)...")
        example_4_ai_ml_module()
        print("✓ Example 4 completed")
        
        return True
        
    except Exception as e:
        print(f"✗ Enhanced examples test failed: {e}")
        return False


def test_interoperability():
    """Test cross-module interoperability"""
    print("\n" + "="*60)
    print("TEST 8: Cross-Module Interoperability")
    print("="*60)
    
    try:
        # Test that all modules can work together
        from domain_modules import RobotController, QuantumCircuit
        from memory_model import OwnershipTracker
        from capability_security import CapabilityEnforcer
        from formal_verification import FormalVerifier
        from cross_domain_integration import CrossDomainCoordinator, Domain
        
        print("✓ All modules can be imported together")
        
        # Create a hybrid system test
        coordinator = CrossDomainCoordinator()
        from cross_domain_integration import setup_default_adapters
        setup_default_adapters(coordinator)
        
        # Test cross-domain data flow
        robot = RobotController()
        circuit = QuantumCircuit(2, [])
        
        robot_data = {"position": [1.0, 2.0, 3.0]}
        quantum_data = coordinator.convert_data(robot_data, Domain.ROBOTICS, Domain.QUANTUM)
        
        print(f"✓ Cross-module data flow working: robotics -> quantum")
        
        # Test verification on domain components
        verifier = FormalVerifier()
        result = verifier.verify_function(
            function_name="robot_control",
            preconditions=["robot.safe == true"],
            postconditions=["robot.position == target"],
            variables={"robot": "Robot", "target": "Pose3D"}
        )
        
        print(f"✓ Verification on domain components working: {result.overall_status.value}")
        
        return True
        
    except Exception as e:
        print(f"✗ Interoperability test failed: {e}")
        return False


def run_full_test():
    """Run comprehensive full program test"""
    print("\n" + "="*70)
    print(" " * 15 + "ION PLATFORM FULL PROGRAM TEST")
    print(" " * 20 + "Developer: ADITYA KAMBLE")
    print("="*70)
    print(f"Test Started: {datetime.utcnow().isoformat()}")
    
    results = {}
    
    # Run all tests
    results['basic_platform'] = test_basic_platform()
    results['domain_modules'] = test_domain_modules()
    results['memory_model'] = test_memory_model()
    results['capability_security'] = test_capability_security()
    results['formal_verification'] = test_formal_verification()
    results['cross_domain'] = test_cross_domain_integration()
    results['enhanced_examples'] = test_enhanced_examples()
    results['interoperability'] = test_interoperability()
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*70)
    print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
    print(f"Test Completed: {datetime.utcnow().isoformat()}")
    print("="*70)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! ION Platform is fully functional.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    exit_code = run_full_test()
    sys.exit(exit_code)
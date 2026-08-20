"""
ION Platform Quick Test
Rapid component verification
Developer: ADITYA KAMBLE
"""

import sys


def test_imports():
    """Test all module imports"""
    print("Testing Module Imports...")
    print("-" * 40)
    
    try:
        # Basic platform
        from ion_language import parse_ion
        from intent_system import IntentSpecification, IntentRegistry, IntentVerifier
        from ion_compiler import IONCompiler
        from deterministic_verification import DeterministicVerifier
        from artifact_generator import ArtifactGenerator
        print("✓ Basic platform modules imported")
        
        # Enhanced modules
        from domain_modules import RobotController, QuantumCircuit
        from memory_model import OwnershipTracker, Option, Result
        from capability_security import CapabilityEnforcer, SecurityContext
        from formal_verification import FormalVerifier
        from cross_domain_integration import CrossDomainCoordinator
        from enhanced_examples import example_1_advanced_type_system
        from realtime_system import RealTimeScheduler, RealTimeExecutor
        print("✓ Enhanced modules imported")
        
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting Basic Functionality...")
    print("-" * 40)
    
    try:
        from ion_language import parse_ion
        from intent_system import create_api_intent, IntentVerifier
        
        # Parser test
        source = 'intent Test: get / -> test()'
        ast = parse_ion(source)
        print(f"✓ Parser: {len(ast.statements)} statements")
        
        # Intent verification test
        intent = create_api_intent('Test', [{'method': 'get', 'path': '/', 'function': 'test'}], [])
        verifier = IntentVerifier()
        status, proof = verifier.verify_intent(intent)
        print(f"✓ Intent verification: {status.value}")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality failed: {e}")
        return False


def test_domain_modules():
    """Test domain modules"""
    print("\nTesting Domain Modules...")
    print("-" * 40)
    
    try:
        from domain_modules import (
            RobotController, RobotControlMode, Pose3D,
            QuantumCircuit, QuantumGate,
            NeuralNetwork, NeuralLayer, Activation, Tensor,
            OrbitalMechanics, OrbitalElements,
            SensorReading, SensorType,
            DNASequence,
            Vector3
        )
        
        # Robotics
        robot = RobotController(RobotControlMode.POSITION)
        target = Pose3D(1, 2, 3)
        control = robot.compute_control(target)
        print(f"✓ Robotics: {len(control)} DOF control")
        
        # Quantum
        circuit = QuantumCircuit(2, [])
        circuit.add_gate(QuantumGate.H, [0])
        print(f"✓ Quantum: circuit depth {circuit.depth()}")
        
        # AI/ML
        layer = NeuralLayer(3, 2, Activation.RELU)
        tensor = Tensor((3,), [1.0, 2.0, 3.0])
        output = layer.forward(tensor)
        print(f"✓ AI/ML: layer output {len(output.data)} values")
        
        # Space
        orbit = OrbitalElements(7000, 0.01, 0.5, 0.3, 0.2, 0.1)
        period = OrbitalMechanics.orbital_period(orbit.semi_major_axis)
        print(f"✓ Space: orbital period {period:.2f}s")
        
        # IoT
        reading = SensorReading("temp_001", SensorType.TEMPERATURE, 25.5, "C", 1234567890.0)
        print(f"✓ IoT: sensor reading {reading.value} {reading.unit}")
        
        # Bio
        dna = DNASequence("ATCG")
        complement = dna.complement()
        print(f"✓ Bio: DNA complement {complement}")
        
        # XR
        vec = Vector3(1, 2, 3).normalize()
        print(f"✓ XR: normalized vector ({vec.x:.3f}, {vec.y:.3f}, {vec.z:.3f})")
        
        return True
    except Exception as e:
        print(f"✗ Domain modules failed: {e}")
        return False


def test_advanced_features():
    """Test advanced features"""
    print("\nTesting Advanced Features...")
    print("-" * 40)
    
    try:
        from memory_model import Option, Result, SharedPtr, LinearType
        from capability_security import CapabilityEnforcer
        from formal_verification import FormalVerifier
        from cross_domain_integration import CrossDomainCoordinator, Domain
        
        # Memory model
        opt = Option.some(42)
        res = Result.ok(100)
        shared = SharedPtr("data")
        linear = LinearType("data", "owner")
        print(f"✓ Memory model: Option={opt.unwrap()}, Result={res.unwrap()}, ref_count={shared.ref_count}")
        
        # Security
        enforcer = CapabilityEnforcer()
        print(f"✓ Security: Capability enforcer created")
        
        # Verification
        verifier = FormalVerifier()
        result = verifier.verify_function("test", ["x>0"], ["result>x"], {"x": "Int", "result": "Int"})
        print(f"✓ Verification: {result.overall_status.value}")
        
        # Integration
        coordinator = CrossDomainCoordinator()
        print(f"✓ Cross-domain: Coordinator created")
        
        return True
    except Exception as e:
        print(f"✗ Advanced features failed: {e}")
        return False


def test_examples():
    """Test example execution"""
    print("\nTesting Example Execution...")
    print("-" * 40)
    
    try:
        from enhanced_examples import example_1_advanced_type_system
        
        # Run one example to verify it works
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        example_1_advanced_type_system()
        
        sys.stdout = old_stdout
        print("✓ Example 1 (Advanced Type System) executed")
        
        return True
    except Exception as e:
        print(f"✗ Example execution failed: {e}")
        return False


def main():
    """Run quick test suite"""
    print("=" * 50)
    print("ION PLATFORM QUICK TEST")
    print("Developer: ADITYA KAMBLE")
    print("=" * 50)
    
    results = []
    
    results.append(("Module Imports", test_imports()))
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("Domain Modules", test_domain_modules()))
    results.append(("Advanced Features", test_advanced_features()))
    results.append(("Example Execution", test_examples()))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} tests passed ({passed*100//total}%)")
    print("=" * 50)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! ION Platform is fully functional.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
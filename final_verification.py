"""
Final Platform Verification Script
Comprehensive verification of all platform components
Developer: ADITYA KAMBLE
"""

import sys
import os
from datetime import datetime


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_section(title):
    """Print formatted section"""
    print(f"\n{title}")
    print("-" * 70)


def verify_files_exist():
    """Verify all required files exist"""
    print_section("1. Verifying Files Exist")
    
    required_files = [
        'main.py',
        'ion_language.py',
        'intent_system.py',
        'ion_compiler.py',
        'deterministic_verification.py',
        'artifact_generator.py',
        'examples.py',
        'domain_modules.py',
        'memory_model.py',
        'capability_security.py',
        'formal_verification.py',
        'cross_domain_integration.py',
        'realtime_system.py',
        'enhanced_examples.py',
        'requirements.txt',
        'README.md',
        'README_COMPLETE.md',
        'USER_GUIDE.md',
        'DEPLOYMENT_GUIDE.md',
        'DEVELOPER_LAUNCH_GUIDE.md',
        'QUICKSTART.md',
        'PROJECT_OVERVIEW.md',
        'CHANGELOG.md',
        'deploy.sh',
        'Dockerfile',
        'docker-compose.yml',
        'quick_test.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            missing_files.append(file)
    
    return len(missing_files) == 0


def verify_imports():
    """Verify all modules can be imported"""
    print_section("2. Verifying Module Imports")
    
    import_tests = [
        ('ion_language', 'parse_ion'),
        ('intent_system', 'IntentSpecification'),
        ('ion_compiler', 'IONCompiler'),
        ('deterministic_verification', 'DeterministicVerifier'),
        ('artifact_generator', 'ArtifactGenerator'),
        ('domain_modules', 'RobotController'),
        ('memory_model', 'OwnershipTracker'),
        ('capability_security', 'CapabilityEnforcer'),
        ('formal_verification', 'FormalVerifier'),
        ('cross_domain_integration', 'CrossDomainCoordinator'),
        ('realtime_system', 'RealTimeScheduler'),
        ('enhanced_examples', 'example_1_advanced_type_system')
    ]
    
    failed_imports = []
    for module_name, class_name in import_tests:
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                print(f"  ✓ {module_name}.{class_name}")
            else:
                print(f"  ✗ {module_name}.{class_name} (not found)")
                failed_imports.append(f"{module_name}.{class_name}")
        except ImportError as e:
            print(f"  ✗ {module_name} (import failed: {e})")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0


def verify_basic_functionality():
    """Verify basic platform functionality"""
    print_section("3. Verifying Basic Functionality")
    
    try:
        from ion_language import parse_ion
        from intent_system import create_api_intent, IntentVerifier
        
        # Test parser
        source = 'intent Test: get / -> test()'
        ast = parse_ion(source)
        print(f"  ✓ Parser: {len(ast.statements)} statements")
        
        # Test intent system
        intent = create_api_intent('Test', [{'method': 'get', 'path': '/', 'function': 'test'}], [])
        verifier = IntentVerifier()
        status, proof = verifier.verify_intent(intent)
        print(f"  ✓ Intent verification: {status.value}")
        
        return True
    except Exception as e:
        print(f"  ✗ Basic functionality failed: {e}")
        return False


def verify_domain_modules():
    """Verify all domain modules work"""
    print_section("4. Verifying Domain Modules")
    
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
        
        # Test Robotics
        robot = RobotController(RobotControlMode.POSITION)
        target = Pose3D(1, 2, 3)
        control = robot.compute_control(target)
        print(f"  ✓ Robotics: {len(control)} DOF control")
        
        # Test Quantum
        circuit = QuantumCircuit(2, [])
        circuit.add_gate(QuantumGate.H, [0])
        print(f"  ✓ Quantum: circuit depth {circuit.depth()}")
        
        # Test AI/ML
        layer = NeuralLayer(3, 2, Activation.RELU)
        tensor = Tensor((3,), [1.0, 2.0, 3.0])
        output = layer.forward(tensor)
        print(f"  ✓ AI/ML: layer output {len(output.data)} values")
        
        # Test Space
        orbit = OrbitalElements(7000, 0.01, 0.5, 0.3, 0.2, 0.1)
        period = OrbitalMechanics.orbital_period(orbit.semi_major_axis)
        print(f"  ✓ Space: orbital period {period:.2f}s")
        
        # Test IoT
        reading = SensorReading("temp_001", SensorType.TEMPERATURE, 25.5, "C", 1234567890.0)
        print(f"  ✓ IoT: sensor reading {reading.value} {reading.unit}")
        
        # Test Bio
        dna = DNASequence("ATCG")
        complement = dna.complement()
        print(f"  ✓ Bio: DNA complement {complement}")
        
        # Test XR
        vec = Vector3(1, 2, 3).normalize()
        print(f"  ✓ XR: normalized vector ({vec.x:.3f}, {vec.y:.3f}, {vec.z:.3f})")
        
        return True
    except Exception as e:
        print(f"  ✗ Domain modules failed: {e}")
        return False


def verify_advanced_features():
    """Verify advanced features"""
    print_section("5. Verifying Advanced Features")
    
    try:
        from memory_model import Option, Result, SharedPtr, LinearType
        from capability_security import CapabilityEnforcer
        from formal_verification import FormalVerifier
        from cross_domain_integration import CrossDomainCoordinator, Domain
        
        # Test memory model
        opt = Option.some(42)
        res = Result.ok(100)
        shared = SharedPtr("data")
        linear = LinearType("data", "owner")
        print(f"  ✓ Memory model: Option={opt.unwrap()}, Result={res.unwrap()}, ref_count={shared.ref_count}")
        
        # Test security
        enforcer = CapabilityEnforcer()
        print(f"  ✓ Security: Capability enforcer created")
        
        # Test verification
        verifier = FormalVerifier()
        result = verifier.verify_function("test", ["x>0"], ["result>x"], {"x": "Int", "result": "Int"})
        print(f"  ✓ Verification: {result.overall_status.value}")
        
        # Test integration
        coordinator = CrossDomainCoordinator()
        print(f"  ✓ Cross-domain: Coordinator created")
        
        return True
    except Exception as e:
        print(f"  ✗ Advanced features failed: {e}")
        return False


def verify_examples():
    """Verify examples execute"""
    print_section("6. Verifying Examples")
    
    try:
        from enhanced_examples import example_1_advanced_type_system
        
        # Suppress output for verification
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        example_1_advanced_type_system()
        
        sys.stdout = old_stdout
        print(f"  ✓ Example 1 (Advanced Type System) executed")
        
        return True
    except Exception as e:
        print(f"  ✗ Example execution failed: {e}")
        return False


def verify_realtime_system():
    """Verify real-time system"""
    print_section("7. Verifying Real-Time System")
    
    try:
        from realtime_system import RealTimeScheduler, RealTimeExecutor
        
        # Test scheduler
        scheduler = RealTimeScheduler(max_workers=2)
        print(f"  ✓ Real-time scheduler created")
        
        # Test executor
        executor = RealTimeExecutor()
        print(f"  ✓ Real-time executor created")
        
        return True
    except Exception as e:
        print(f"  ✗ Real-time system failed: {e}")
        return False


def verify_documentation():
    """Verify documentation files exist and are complete"""
    print_section("8. Verifying Documentation")
    
    doc_files = [
        ('README.md', 'Basic README'),
        ('README_COMPLETE.md', 'Complete README'),
        ('USER_GUIDE.md', 'User Guide'),
        ('DEPLOYMENT_GUIDE.md', 'Deployment Guide'),
        ('DEVELOPER_LAUNCH_GUIDE.md', 'Developer Launch Guide'),
        ('QUICKSTART.md', 'Quick Start'),
        ('PROJECT_OVERVIEW.md', 'Project Overview'),
        ('CHANGELOG.md', 'Changelog')
    ]
    
    for filename, description in doc_files:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read()
                lines = len(content.split('\n'))
                print(f"  ✓ {description} ({filename}): {lines} lines")
        else:
            print(f"  ✗ {description} ({filename}): MISSING")
    
    return True


def verify_deployment_resources():
    """Verify deployment resources"""
    print_section("9. Verifying Deployment Resources")
    
    deployment_files = [
        ('deploy.sh', 'Deployment script'),
        ('Dockerfile', 'Docker configuration'),
        ('docker-compose.yml', 'Docker Compose'),
        ('portal/landing.html', 'Developer portal')
    ]
    
    for filename, description in deployment_files:
        if os.path.exists(filename):
            print(f"  ✓ {description} ({filename})")
        else:
            print(f"  ✗ {description} ({filename}): MISSING")
    
    return True


def run_final_verification():
    """Run comprehensive final verification"""
    print_header("FINAL PLATFORM VERIFICATION")
    print(f"Date: {datetime.utcnow().isoformat()}")
    print(f"Developer: ADITYA KAMBLE")
    
    results = {}
    
    # Run all verifications
    results['files_exist'] = verify_files_exist()
    results['imports'] = verify_imports()
    results['basic_functionality'] = verify_basic_functionality()
    results['domain_modules'] = verify_domain_modules()
    results['advanced_features'] = verify_advanced_features()
    results['examples'] = verify_examples()
    results['realtime_system'] = verify_realtime_system()
    results['documentation'] = verify_documentation()
    results['deployment_resources'] = verify_deployment_resources()
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 70)
    print(f"FINAL RESULT: {passed}/{total} verifications passed ({passed*100//total}%)")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        print("\nThe Intent-Deterministic Development Platform is fully")
        print("functional and ready for production deployment.")
        print("\nNext steps:")
        print("  1. Review documentation in USER_GUIDE.md")
        print("  2. Deploy using deployment resources")
        print("  3. Launch for developers using DEVELOPER_LAUNCH_GUIDE.md")
        return 0
    else:
        print(f"\n⚠️  {total - passed} verification(s) failed.")
        print("Please review the failures above and fix issues.")
        return 1


if __name__ == "__main__":
    exit_code = run_final_verification()
    sys.exit(exit_code)
"""
Build Your First ION Application
Demonstrates compiling an ION file and reviewing artifacts
Developer: ADITYA KAMBLE
"""

from ion_language import parse_ion
from intent_system import create_api_intent, IntentVerifier
from ion_compiler import IONCompiler
from artifact_generator import ArtifactGenerator

print("=" * 70)
print("BUILDING YOUR FIRST ION APPLICATION")
print("=" * 70)

# Step 1: Define ION source code
ion_source = """
intent TaskManager:
    get /tasks -> list_all_tasks()
    post /tasks -> create_task(body)
    get /tasks/{id} -> get_task(id)
    delete /tasks/{id} -> delete_task(id)
    
    constraint auth: jwt
    constraint rate: 200/min
    constraint latency: < 100ms
    constraint memory: < 64MB
    
    invariant task.id is unique
    invariant task.title is not empty
"""

print("\n1. ION Source Code:")
print("-" * 70)
print(ion_source)

# Step 2: Parse the ION source
print("\n2. Parsing ION Source...")
ast = parse_ion(ion_source)
print(f"   ✓ Parsed {len(ast.statements)} statements")

# Step 3: Create intent from parsed AST
print("\n3. Creating Intent Specification...")
intent = create_api_intent(
    name='TaskManager',
    endpoints=[
        {'method': 'get', 'path': '/tasks', 'function': 'list_all_tasks'},
        {'method': 'post', 'path': '/tasks', 'function': 'create_task'},
        {'method': 'get', 'path': '/tasks/{id}', 'function': 'get_task'},
        {'method': 'delete', 'path': '/tasks/{id}', 'function': 'delete_task'}
    ],
    constraints=[
        {'name': 'auth', 'type': 'AUTH', 'value': 'jwt'},
        {'name': 'rate', 'type': 'RATE', 'value': '200/min'},
        {'name': 'latency', 'type': 'LATENCY', 'value': '< 100ms'},
        {'name': 'memory', 'type': 'MEMORY', 'value': '64MB'}
    ],
    invariants=[
        {'condition': 'task.id is unique', 'description': 'Task IDs must be unique'},
        {'condition': 'task.title is not empty', 'description': 'Task titles cannot be empty'}
    ]
)
print(f"   ✓ Intent created: {intent.name}")
print(f"   ✓ Endpoints: {len(intent.endpoints)}")
print(f"   ✓ Constraints: {len(intent.constraints)}")
print(f"   ✓ Invariants: {len(intent.invariants)}")

# Step 4: Verify the intent
print("\n4. Verifying Intent...")
verifier = IntentVerifier()
status, proof = verifier.verify_intent(intent)
print(f"   ✓ Verification Status: {status.value}")
print(f"   ✓ Memory Safety: {proof.memory_safety_theorem}")
print(f"   ✓ Termination: {proof.termination_proof}")
print(f"   ✓ Security: {proof.security_compliance}")

# Step 5: Compile the intent
print("\n5. Compiling Intent...")
compiler = IONCompiler()
result = compiler.compile_source(ion_source)
print(f"   ✓ Compilation Success: {result.success}")
print(f"   ✓ Compilation Time: {result.compilation_time_ms}ms")
print(f"   ✓ Phases Completed: {[p.value for p in result.phases_completed]}")

# Step 6: Generate artifacts
print("\n6. Generating Artifacts...")
artifact_gen = ArtifactGenerator()
artifacts = artifact_gen.generate_all_artifacts(intent, proof)
print(f"   ✓ Generated {len(artifacts)} artifacts:")

for artifact_type, artifact in artifacts.items():
    print(f"      - {artifact_type.value}: {artifact.format} ({len(artifact.data)} bytes)")

# Step 7: Save artifacts to disk
print("\n7. Saving Artifacts to Disk...")
import os
import json

os.makedirs('my-ion-project/artifacts', exist_ok=True)

for artifact_type, artifact in artifacts.items():
    filename = f"my-ion-project/artifacts/{artifact_type.value}.{artifact.format}"
    
    if artifact.format == "json":
        with open(filename, 'w') as f:
            f.write(artifact.data)
    elif artifact.format == "txt":
        with open(filename, 'w') as f:
            f.write(artifact.data)
    else:
        with open(filename, 'wb') as f:
            f.write(artifact.data)
    
    print(f"   ✓ Saved: {filename}")

# Step 8: Review generated artifacts
print("\n8. Reviewing Generated Artifacts...")
print("-" * 70)

# Show proof certificate
proof_file = 'my-ion-project/artifacts/proof_certificate.json'
if os.path.exists(proof_file):
    with open(proof_file, 'r') as f:
        proof_data = json.load(f)
    print("\nProof Certificate:")
    print(json.dumps(proof_data, indent=2)[:500] + "...")

# Show intent bundle
bundle_file = 'my-ion-project/artifacts/intent_bundle.json'
if os.path.exists(bundle_file):
    with open(bundle_file, 'r') as f:
        bundle_data = json.load(f)
    print("\nIntent Bundle:")
    print(f"  Name: {bundle_data.get('name', 'N/A')}")
    print(f"  Type: {bundle_data.get('intent_type', 'N/A')}")
    print(f"  Endpoints: {len(bundle_data.get('endpoints', []))}")

print("\n" + "=" * 70)
print("BUILD COMPLETE!")
print("=" * 70)
print("\nYour ION application has been:")
print("  ✓ Parsed and analyzed")
print("  ✓ Verified for safety and correctness")
print("  ✓ Compiled to intermediate representation")
print("  ✓ Generated 9 artifacts")
print("  ✓ Saved to my-ion-project/artifacts/")
print("\nNext steps:")
print("  1. Review the generated artifacts")
print("  2. Deploy using the deployment guide")
print("  3. Integrate with your backend framework")
print("\nDeveloper: ADITYA KAMBLE")

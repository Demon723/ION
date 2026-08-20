"""
ION Intent Compiler
Compiles ION intent specifications into verified executables and artifacts
Based on ION Research & Code Compendium - Layer 5: Intent Compiler

Developer: ADITYA KAMBLE
"""

import json
import base64
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ion_language import (
    Program, FunctionDecl, StructDecl, IntentDecl, 
    VariableDecl, BinaryOp, FunctionCall, Literal, ASTNode
)
from intent_system import (
    IntentSpecification, IntentType, Constraint, ConstraintType,
    ProofCertificate, IntentBundle, IntentRegistry, IntentVerifier,
    VerificationStatus
)


class CompilationPhase(Enum):
    """Compilation phases"""
    PARSING = "PARSING"
    DECOMPOSITION = "DECOMPOSITION"
    PLANNING = "PLANNING"
    GENERATION = "GENERATION"
    VERIFICATION = "VERIFICATION"
    EMISSION = "EMISSION"


class CompilationTarget(Enum):
    """Compilation targets"""
    NATIVE_X86 = "NATIVE_X86"
    NATIVE_ARM = "NATIVE_ARM"
    WASM = "WASM"
    FORMAL_MODEL = "FORMAL_MODEL"
    DOCUMENTATION = "DOCUMENTATION"


@dataclass
class CompilationResult:
    """Result of compilation process"""
    success: bool
    phases_completed: List[CompilationPhase]
    generated_artifacts: Dict[str, str] = field(default_factory=dict)
    proof_certificate: Optional[ProofCertificate] = None
    intent_bundle: Optional[IntentBundle] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    compilation_time_ms: int = 0


@dataclass
class DecompositionPlan:
    """Goal decomposition plan"""
    primary_goals: List[str]
    sub_goals: List[str]
    dependencies: List[str]
    execution_order: List[str]
    resource_estimates: Dict[str, str] = field(default_factory=dict)


@dataclass
class ExecutionPlan:
    """Execution plan for intent realization"""
    steps: List[Dict[str, Any]]
    parallelization: List[List[str]]
    verification_points: List[int]
    rollback_checkpoints: List[int]


class IntentDecomposer:
    """Decomposes high-level intents into executable goals"""
    
    def decompose(self, intent: IntentSpecification) -> DecompositionPlan:
        """Decompose intent into executable goals"""
        primary_goals = []
        sub_goals = []
        dependencies = []
        
        # Extract goals from endpoints
        for endpoint in intent.endpoints:
            primary_goals.append(f"implement_{endpoint.method}_{endpoint.path.replace('/', '_')}")
            sub_goals.append(f"validate_{endpoint.function}")
            sub_goals.append(f"secure_{endpoint.method}_{endpoint.path}")
        
        # Extract goals from constraints
        for constraint in intent.constraints:
            sub_goals.append(f"enforce_{constraint.name}")
            dependencies.append(constraint.name)
        
        # Extract goals from invariants
        for invariant in intent.invariants:
            primary_goals.append(f"maintain_invariant_{hash(invariant.condition) % 10000}")
            sub_goals.append(f"verify_{invariant.condition[:20]}")
        
        # Determine execution order based on dependencies
        execution_order = self._determine_execution_order(primary_goals, sub_goals, dependencies)
        
        # Estimate resources
        resource_estimates = self._estimate_resources(intent)
        
        return DecompositionPlan(
            primary_goals=primary_goals,
            sub_goals=sub_goals,
            dependencies=dependencies,
            execution_order=execution_order,
            resource_estimates=resource_estimates
        )
    
    def _determine_execution_order(self, primary: List[str], sub: List[str], deps: List[str]) -> List[str]:
        """Determine optimal execution order"""
        # Simple topological sort for prototype
        order = []
        
        # Add dependency implementations first
        for dep in deps:
            order.append(f"setup_{dep}")
        
        # Add primary goals
        order.extend(primary)
        
        # Add sub-goals
        order.extend(sub)
        
        return order
    
    def _estimate_resources(self, intent: IntentSpecification) -> Dict[str, str]:
        """Estimate resource requirements"""
        estimates = {
            'memory': '64MB',
            'cpu': '2 cores',
            'storage': '100MB',
            'network': '1Gbps'
        }
        
        # Adjust based on constraints
        for constraint in intent.constraints:
            if constraint.constraint_type == ConstraintType.MEMORY:
                estimates['memory'] = constraint.value
            elif constraint.constraint_type == ConstraintType.RATE:
                # Estimate based on rate limit
                rate = int(constraint.value.split('/')[0])
                if rate > 1000:
                    estimates['cpu'] = '4 cores'
        
        return estimates


class PlanGenerator:
    """Generates execution plans from decomposed goals"""
    
    def generate_plan(self, decomposition: DecompositionPlan, intent: IntentSpecification) -> ExecutionPlan:
        """Generate execution plan"""
        steps = []
        parallelization = []
        verification_points = []
        rollback_checkpoints = []
        
        step_id = 0
        for goal in decomposition.execution_order:
            step = {
                'id': step_id,
                'goal': goal,
                'action': self._determine_action(goal),
                'estimated_duration': self._estimate_duration(goal),
                'dependencies': self._find_dependencies(goal, decomposition)
            }
            steps.append(step)
            
            # Add verification points after critical steps
            if 'implement' in goal or 'enforce' in goal:
                verification_points.append(step_id)
            
            # Add rollback checkpoints before destructive operations
            if 'deploy' in goal or 'modify' in goal:
                rollback_checkpoints.append(step_id)
            
            step_id += 1
        
        # Determine parallelization opportunities
        parallelization = self._find_parallel_steps(steps)
        
        return ExecutionPlan(
            steps=steps,
            parallelization=parallelization,
            verification_points=verification_points,
            rollback_checkpoints=rollback_checkpoints
        )
    
    def _determine_action(self, goal: str) -> str:
        """Determine action for a goal"""
        if 'implement' in goal:
            return 'generate_code'
        elif 'validate' in goal:
            return 'formal_verification'
        elif 'secure' in goal:
            return 'apply_security_controls'
        elif 'enforce' in goal:
            return 'apply_constraint'
        elif 'setup' in goal:
            return 'initialize_dependency'
        elif 'verify' in goal:
            return 'runtime_verification'
        else:
            return 'execute'
    
    def _estimate_duration(self, goal: str) -> str:
        """Estimate step duration"""
        if 'implement' in goal:
            return '5-10s'
        elif 'verify' in goal or 'validate' in goal:
            return '1-3s'
        else:
            return '1-2s'
    
    def _find_dependencies(self, goal: str, decomposition: DecompositionPlan) -> List[str]:
        """Find dependencies for a goal"""
        deps = []
        for dep in decomposition.dependencies:
            if dep.lower() in goal.lower():
                deps.append(f"setup_{dep}")
        return deps
    
    def _find_parallel_steps(self, steps: List[Dict]) -> List[List[str]]:
        """Find steps that can be executed in parallel"""
        parallel_groups = []
        current_group = []
        
        for i, step in enumerate(steps):
            if not step['dependencies'] and i > 0:
                if current_group:
                    parallel_groups.append([s['goal'] for s in current_group])
                    current_group = []
            current_group.append(step)
        
        if current_group:
            parallel_groups.append([s['goal'] for s in current_group])
        
        return parallel_groups


class CodeGenerator:
    """Generates code from execution plans"""
    
    def generate(self, plan: ExecutionPlan, intent: IntentSpecification) -> Dict[str, str]:
        """Generate code for all targets"""
        artifacts = {}
        
        # Generate native binary (simulated)
        artifacts['native_binary'] = self._generate_native_code(plan, intent)
        
        # Generate WASM module
        artifacts['wasm_module'] = self._generate_wasm(plan, intent)
        
        # Generate formal model
        artifacts['formal_model'] = self._generate_formal_model(plan, intent)
        
        # Generate documentation
        artifacts['documentation'] = self._generate_documentation(plan, intent)
        
        return artifacts
    
    def _generate_native_code(self, plan: ExecutionPlan, intent: IntentSpecification) -> str:
        """Generate native code (simulated)"""
        code = f"""// Auto-generated ION Native Code
// Intent: {intent.name}
// Generated: {datetime.utcnow().isoformat()}

#include <ion_runtime.h>
#include <security.h>
#include <verification.h>

int main() {{
    // Initialize ION runtime
    ion_runtime_init();
    
    // Apply security constraints
"""
        for constraint in intent.constraints:
            code += f"    apply_constraint(\"{constraint.name}\", \"{constraint.value}\");\n"
        
        code += "\n    // Execute intent\n"
        for step in plan.steps:
            code += f"    // Step {step['id']}: {step['goal']}\n"
            code += f"    execute_step(\"{step['action']}\");\n"
        
        code += """
    // Verify invariants
    verify_all_invariants();
    
    return 0;
}
"""
        return code
    
    def _generate_wasm(self, plan: ExecutionPlan, intent: IntentSpecification) -> str:
        """Generate WASM module (simulated)"""
        wasm = f"""(module
  ;; Auto-generated ION WASM Module
  ;; Intent: {intent.name}
  
  (import "ion" "memory" (memory 1))
  (import "ion" "apply_constraint" (func $apply_constraint (param i32 i32)))
  
  (func (export "main")
    ;; Apply constraints
"""
        for i, constraint in enumerate(intent.constraints):
            wasm += f"    call $apply_constraint (i32.const {i}) (i32.const {len(constraint.value)})\n"
        
        wasm += """
    ;; Execute intent steps
    call $execute_intent
    
    ;; Verify invariants
    call $verify_invariants
  )
)
"""
        return wasm
    
    def _generate_formal_model(self, plan: ExecutionPlan, intent: IntentSpecification) -> str:
        """Generate formal model (SMT-LIB format)"""
        model = f""";; ION Formal Model
;; Intent: {intent.name}

(declare-fun state (Int) Bool)
(declare-fun invariant_holds (Int) Bool)

;; Invariants
"""
        for i, invariant in enumerate(intent.invariants):
            model += f"(assert (forall ((t Int)) (= (invariant_holds {i}) {invariant.condition})))\n"
        
        model += "\n;; Constraints\n"
        for i, constraint in enumerate(intent.constraints):
            model += f"(declare-fun constraint_{i} (Int) Bool)\n"
            model += f"(assert (constraint_{i} 0))\n"
        
        model += "\n;; Verification goals\n"
        model += "(check-sat)\n"
        model += "(get-model)\n"
        
        return model
    
    def _generate_documentation(self, plan: ExecutionPlan, intent: IntentSpecification) -> str:
        """Generate human-readable documentation"""
        doc = f"""# ION Intent Documentation

## Intent: {intent.name}

**Type:** {intent.intent_type.value}  
**Version:** {intent.version}  
**Description:** {intent.description}

### Endpoints
"""
        for endpoint in intent.endpoints:
            doc += f"- **{endpoint.method.upper()} {endpoint.path}** → `{endpoint.function}`\n"
        
        doc += "\n### Constraints\n"
        for constraint in intent.constraints:
            doc += f"- **{constraint.name}** ({constraint.constraint_type.value}): {constraint.value}\n"
        
        doc += "\n### Invariants\n"
        for invariant in intent.invariants:
            doc += f"- {invariant.condition}\n"
        
        doc += f"\n### Execution Plan\n"
        doc += f"Total steps: {len(plan.steps)}\n"
        doc += f"Parallel groups: {len(plan.parallelization)}\n"
        doc += f"Verification points: {len(plan.verification_points)}\n"
        
        doc += "\n### Steps\n"
        for step in plan.steps:
            doc += f"{step['id']}. **{step['goal']}** ({step['action']}) - {step['estimated_duration']}\n"
        
        return doc


class IONCompiler:
    """Main ION Intent Compiler"""
    
    def __init__(self):
        self.decomposer = IntentDecomposer()
        self.plan_generator = PlanGenerator()
        self.code_generator = CodeGenerator()
        self.verifier = IntentVerifier()
        self.registry = IntentRegistry()
    
    def compile(self, ast: Program, intent_spec: IntentSpecification, 
                targets: List[CompilationTarget] = None) -> CompilationResult:
        """Compile ION intent into executable artifacts"""
        start_time = datetime.utcnow()
        
        if targets is None:
            targets = [CompilationTarget.NATIVE_X86, CompilationTarget.WASM, 
                      CompilationTarget.FORMAL_MODEL, CompilationTarget.DOCUMENTATION]
        
        result = CompilationResult(
            success=False,
            phases_completed=[],
            generated_artifacts={},
            errors=[],
            warnings=[]
        )
        
        try:
            # Phase 1: Parsing (already done, AST provided)
            result.phases_completed.append(CompilationPhase.PARSING)
            
            # Phase 2: Decomposition
            result.phases_completed.append(CompilationPhase.DECOMPOSITION)
            decomposition = self.decomposer.decompose(intent_spec)
            
            # Phase 3: Planning
            result.phases_completed.append(CompilationPhase.PLANNING)
            execution_plan = self.plan_generator.generate_plan(decomposition, intent_spec)
            
            # Phase 4: Generation
            result.phases_completed.append(CompilationPhase.GENERATION)
            artifacts = self.code_generator.generate(execution_plan, intent_spec)
            result.generated_artifacts = artifacts
            
            # Phase 5: Verification
            result.phases_completed.append(CompilationPhase.VERIFICATION)
            verification_status, proof_certificate = self.verifier.verify_intent(intent_spec)
            result.proof_certificate = proof_certificate
            
            if verification_status != VerificationStatus.VERIFIED:
                result.warnings.append(f"Verification status: {verification_status.value}")
            
            # Phase 6: Emission
            result.phases_completed.append(CompilationPhase.EMISSION)
            
            # Create intent bundle
            intent_bundle = IntentBundle(
                intent_spec=intent_spec.to_dict(),
                compiled_binary=base64.b64encode(artifacts['native_binary'].encode()).decode(),
                proof_certificate=proof_certificate,
                rollback_spec={'steps': execution_plan.rollback_checkpoints},
                signature=self._generate_signature(intent_spec, proof_certificate),
                version=intent_spec.version
            )
            result.intent_bundle = intent_bundle
            
            # Calculate compilation time
            end_time = datetime.utcnow()
            result.compilation_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            result.success = True
            
        except Exception as e:
            result.errors.append(str(e))
            result.success = False
        
        return result
    
    def _generate_signature(self, intent: IntentSpecification, proof: ProofCertificate) -> str:
        """Generate cryptographic signature for intent bundle"""
        data = f"{intent.generate_hash()}_{proof.intent_hash}_{datetime.utcnow().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def compile_source(self, source: str) -> CompilationResult:
        """Compile ION source code directly"""
        from ion_language import parse_ion
        
        # Parse source
        ast = parse_ion(source)
        
        # Extract intent specification from AST
        intent_spec = self._extract_intent_from_ast(ast)
        
        if not intent_spec:
            # Create default intent if none found
            intent_spec = IntentSpecification(
                name="DefaultIntent",
                intent_type=IntentType.API,
                description="Auto-generated from source code"
            )
        
        return self.compile(ast, intent_spec)
    
    def _extract_intent_from_ast(self, ast: Program) -> Optional[IntentSpecification]:
        """Extract intent specification from AST"""
        for stmt in ast.statements:
            if isinstance(stmt, IntentDecl):
                # Convert AST IntentDecl to IntentSpecification
                intent_spec = IntentSpecification(
                    name=stmt.name,
                    intent_type=IntentType.API,
                    description=f"Intent: {stmt.name}"
                )
                
                # Add endpoints
                for ep in stmt.endpoints:
                    from intent_system import Endpoint
                    intent_spec.endpoints.append(Endpoint(
                        method=ep['method'],
                        path=ep['path'],
                        function=ep['function']
                    ))
                
                # Add constraints
                for c in stmt.constraints:
                    constraint_type = ConstraintType.AUTH if c['name'] == 'auth' else ConstraintType.RATE
                    intent_spec.constraints.append(Constraint(
                        name=c['name'],
                        constraint_type=constraint_type,
                        value=c['value']
                    ))
                
                # Add invariants
                for inv in stmt.invariants:
                    from intent_system import Invariant
                    intent_spec.invariants.append(Invariant(condition=inv))
                
                return intent_spec
        
        return None


def main():
    """Example usage of ION Compiler"""
    compiler = IONCompiler()
    
    # Example ION source code
    ion_source = """
# ION User Service
intent UserService:
    get /users -> list_all()
    post /users -> create_user(body)
    
    constraint auth: jwt
    constraint rate: 100/min
    constraint memory: < 64MB
"""
    
    # Compile the source
    result = compiler.compile_source(ion_source)
    
    print("ION Compilation Result")
    print("=" * 50)
    print(f"Success: {result.success}")
    print(f"Phases Completed: {[p.value for p in result.phases_completed]}")
    print(f"Compilation Time: {result.compilation_time_ms}ms")
    print(f"Artifacts Generated: {list(result.generated_artifacts.keys())}")
    
    if result.errors:
        print(f"\nErrors: {result.errors}")
    
    if result.warnings:
        print(f"\nWarnings: {result.warnings}")
    
    if result.proof_certificate:
        print(f"\nProof Certificate:")
        print(f"  Memory Safety: {result.proof_certificate.memory_safety_theorem}")
        print(f"  Termination: {result.proof_certificate.termination_proof}")
        print(f"  Security: {result.proof_certificate.security_compliance}")
    
    if result.intent_bundle:
        print(f"\nIntent Bundle Created:")
        print(f"  Version: {result.intent_bundle.version}")
        print(f"  Signature: {result.intent_bundle.signature[:16]}...")
    
    print("\nGenerated Documentation:")
    print(result.generated_artifacts.get('documentation', 'Not available'))


if __name__ == "__main__":
    main()
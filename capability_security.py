"""
ION Capability-Based Security System
Implementation of capability-based security and permission enforcement
Based on ION Complete Language Specification (August 2026)

Developer: ADITYA KAMBLE
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Callable
from enum import Enum
import hashlib
import json


class SecurityError(Exception):
    """Security-related errors"""
    pass


class PermissionDeniedError(SecurityError):
    """Permission denied errors"""
    pass


class CapabilityInvalidError(SecurityError):
    """Capability validation errors"""
    pass


class CapabilityType(Enum):
    """Types of capabilities"""
    FILE_ACCESS = "file_access"
    NETWORK_ACCESS = "network_access"
    HARDWARE_ACCESS = "hardware_access"
    PROCESS_CONTROL = "process_control"
    SYSTEM_CONFIG = "system_config"
    DATABASE_ACCESS = "database_access"
    CRYPTOGRAPHIC = "cryptographic"
    USER_DATA = "user_data"
    ADMIN = "admin"


class Permission(Enum):
    """Specific permissions within capabilities"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    CREATE = "create"
    MODIFY = "modify"
    CONNECT = "connect"
    BIND = "bind"
    LISTEN = "listen"


@dataclass
class Capability:
    """Security capability"""
    name: str
    capability_type: CapabilityType
    permissions: Set[Permission]
    constraints: Dict[str, Any] = field(default_factory=dict)
    is_revoked: bool = False
    expires_at: Optional[float] = None
    
    def __post_init__(self):
        self.id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique capability ID"""
        data = f"{self.name}{self.capability_type.value}{','.join(p.value for p in self.permissions)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if capability has specific permission"""
        return permission in self.permissions and not self.is_revoked
    
    def is_expired(self) -> bool:
        """Check if capability is expired"""
        if self.expires_at is None:
            return False
        import time
        return time.time() > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if capability is valid"""
        return not self.is_revoked and not self.is_expired()
    
    def revoke(self):
        """Revoke the capability"""
        self.is_revoked = True
    
    def check_constraint(self, constraint_name: str, value: Any) -> bool:
        """Check if a constraint is satisfied"""
        if constraint_name not in self.constraints:
            return False
        return self.constraints[constraint_name] == value


@dataclass
class SecurityContext:
    """Security context for execution"""
    capabilities: List[Capability] = field(default_factory=list)
    principal: str = "anonymous"
    is_trusted: bool = False
    security_level: int = 0  # 0-10, higher = more privileges
    
    def add_capability(self, capability: Capability):
        """Add a capability to the context"""
        if not capability.is_valid():
            raise CapabilityInvalidError(f"Cannot add invalid capability: {capability.name}")
        self.capabilities.append(capability)
    
    def has_capability(self, capability_name: str) -> bool:
        """Check if context has a specific capability"""
        return any(cap.name == capability_name and cap.is_valid() 
                  for cap in self.capabilities)
    
    def has_permission(self, capability_type: CapabilityType, 
                      permission: Permission) -> bool:
        """Check if context has specific permission"""
        return any(
            cap.capability_type == capability_type and 
            cap.has_permission(permission) and 
            cap.is_valid()
            for cap in self.capabilities
        )
    
    def get_capability(self, capability_name: str) -> Optional[Capability]:
        """Get a specific capability"""
        for cap in self.capabilities:
            if cap.name == capability_name:
                return cap
        return None
    
    def revoke_capability(self, capability_name: str):
        """Revoke a specific capability"""
        cap = self.get_capability(capability_name)
        if cap:
            cap.revoke()
    
    def clone(self) -> 'SecurityContext':
        """Clone the security context"""
        return SecurityContext(
            capabilities=list(self.capabilities),
            principal=self.principal,
            is_trusted=self.is_trusted,
            security_level=self.security_level
        )


@dataclass
class CapabilitySpec:
    """Capability specification for functions"""
    required_capabilities: List[str] = field(default_factory=list)
    required_permissions: Dict[CapabilityType, Set[Permission]] = field(default_factory=dict)
    restrictions: List[str] = field(default_factory=list)
    security_level_required: int = 0


class CapabilityEnforcer:
    """Enforce capability-based security policies"""
    
    def __init__(self):
        self.contexts: Dict[str, SecurityContext] = {}
        self.function_specs: Dict[str, CapabilitySpec] = {}
        self.audit_log: List[Dict[str, Any]] = []
    
    def create_context(self, principal: str, capabilities: List[Capability] = None) -> SecurityContext:
        """Create a new security context"""
        if capabilities is None:
            capabilities = []
        
        context = SecurityContext(
            capabilities=capabilities,
            principal=principal
        )
        
        self.contexts[principal] = context
        self._log_audit("context_created", {"principal": principal})
        return context
    
    def register_function(self, function_name: str, spec: CapabilitySpec):
        """Register a function with its capability requirements"""
        self.function_specs[function_name] = spec
        self._log_audit("function_registered", {"function": function_name, "spec": spec.__dict__})
    
    def check_function_access(self, context: SecurityContext, function_name: str) -> bool:
        """Check if context can access a function"""
        if function_name not in self.function_specs:
            return True  # No spec means no restrictions
        
        spec = self.function_specs[function_name]
        
        # Check security level
        if context.security_level < spec.security_level_required:
            self._log_audit("access_denied", {
                "function": function_name,
                "reason": "insufficient_security_level",
                "required": spec.security_level_required,
                "current": context.security_level
            })
            return False
        
        # Check required capabilities
        for cap_name in spec.required_capabilities:
            if not context.has_capability(cap_name):
                self._log_audit("access_denied", {
                    "function": function_name,
                    "reason": "missing_capability",
                    "required": cap_name
                })
                return False
        
        # Check required permissions
        for cap_type, permissions in spec.required_permissions.items():
            for perm in permissions:
                if not context.has_permission(cap_type, perm):
                    self._log_audit("access_denied", {
                        "function": function_name,
                        "reason": "missing_permission",
                        "capability_type": cap_type.value,
                        "permission": perm.value
                    })
                    return False
        
        self._log_audit("access_granted", {"function": function_name, "principal": context.principal})
        return True
    
    def enforce_function_access(self, context: SecurityContext, function_name: str):
        """Enforce function access, raise exception if denied"""
        if not self.check_function_access(context, function_name):
            raise PermissionDeniedError(
                f"Context '{context.principal}' does not have required capabilities for '{function_name}'"
            )
    
    def check_resource_access(self, context: SecurityContext, resource_type: CapabilityType,
                            permission: Permission, resource_path: str = "") -> bool:
        """Check if context can access a specific resource"""
        if not context.has_permission(resource_type, permission):
            self._log_audit("resource_access_denied", {
                "resource_type": resource_type.value,
                "permission": permission.value,
                "resource_path": resource_path,
                "principal": context.principal
            })
            return False
        
        # Check path constraints if specified
        if resource_path:
            for cap in context.capabilities:
                if cap.capability_type == resource_type and "allowed_paths" in cap.constraints:
                    allowed_paths = cap.constraints["allowed_paths"]
                    if not any(resource_path.startswith(path) for path in allowed_paths):
                        self._log_audit("resource_access_denied", {
                            "reason": "path_not_allowed",
                            "resource_path": resource_path,
                            "allowed_paths": allowed_paths
                        })
                        return False
        
        self._log_audit("resource_access_granted", {
            "resource_type": resource_type.value,
            "permission": permission.value,
            "resource_path": resource_path,
            "principal": context.principal
        })
        return True
    
    def _log_audit(self, event_type: str, details: Dict[str, Any]):
        """Log security audit event"""
        import time
        self.audit_log.append({
            "timestamp": time.time(),
            "event_type": event_type,
            "details": details
        })
    
    def get_audit_log(self, event_type: str = None) -> List[Dict[str, Any]]:
        """Get audit log, optionally filtered by event type"""
        if event_type is None:
            return self.audit_log
        return [entry for entry in self.audit_log if entry["event_type"] == event_type]


class FileAccessCapability(Capability):
    """File access capability"""
    
    def __init__(self, allowed_paths: List[str], permissions: Set[Permission]):
        super().__init__(
            name="file_access",
            capability_type=CapabilityType.FILE_ACCESS,
            permissions=permissions,
            constraints={"allowed_paths": allowed_paths}
        )
    
    def can_access_path(self, path: str, permission: Permission) -> bool:
        """Check if can access specific path with permission"""
        if not self.has_permission(permission):
            return False
        
        allowed_paths = self.constraints.get("allowed_paths", [])
        return any(path.startswith(allowed_path) for allowed_path in allowed_paths)


class NetworkAccessCapability(Capability):
    """Network access capability"""
    
    def __init__(self, allowed_hosts: List[str], allowed_ports: List[int], 
                 permissions: Set[Permission]):
        super().__init__(
            name="network_access",
            capability_type=CapabilityType.NETWORK_ACCESS,
            permissions=permissions,
            constraints={
                "allowed_hosts": allowed_hosts,
                "allowed_ports": allowed_ports
            }
        )
    
    def can_connect_to(self, host: str, port: int) -> bool:
        """Check if can connect to specific host:port"""
        if not self.has_permission(Permission.CONNECT):
            return False
        
        allowed_hosts = self.constraints.get("allowed_hosts", [])
        allowed_ports = self.constraints.get("allowed_ports", [])
        
        host_allowed = not allowed_hosts or any(host == allowed or host.endswith(allowed) 
                                            for allowed in allowed_hosts)
        port_allowed = not allowed_ports or port in allowed_ports
        
        return host_allowed and port_allowed


class CapabilityDecorator:
    """Decorator for enforcing capabilities on functions"""
    
    def __init__(self, enforcer: CapabilityEnforcer):
        self.enforcer = enforcer
    
    def __call__(self, required_capabilities: List[str] = None,
                required_permissions: Dict[CapabilityType, List[Permission]] = None,
                security_level: int = 0):
        """Create a decorator for capability enforcement"""
        
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Get security context from first argument if available
                context = None
                if args and isinstance(args[0], SecurityContext):
                    context = args[0]
                elif 'context' in kwargs:
                    context = kwargs['context']
                
                if context is None:
                    raise SecurityError("No security context provided")
                
                # Build capability spec
                spec = CapabilitySpec(
                    required_capabilities=required_capabilities or [],
                    required_permissions={
                        k: set(v) for k, v in (required_permissions or {}).items()
                    },
                    security_level_required=security_level
                )
                
                # Register function spec if not already registered
                func_name = func.__name__
                if func_name not in self.enforcer.function_specs:
                    self.enforcer.register_function(func_name, spec)
                
                # Enforce access
                self.enforcer.enforce_function_access(context, func_name)
                
                # Call the function
                return func(*args, **kwargs)
            
            return wrapper
        return decorator


# Predefined capabilities

def create_file_read_capability(allowed_paths: List[str]) -> FileAccessCapability:
    """Create a file read capability"""
    return FileAccessCapability(allowed_paths, {Permission.READ})


def create_file_write_capability(allowed_paths: List[str]) -> FileAccessCapability:
    """Create a file write capability"""
    return FileAccessCapability(allowed_paths, {Permission.READ, Permission.WRITE})


def create_network_capability(allowed_hosts: List[str], 
                            allowed_ports: List[int] = None) -> NetworkAccessCapability:
    """Create a network access capability"""
    if allowed_ports is None:
        allowed_ports = [80, 443]  # Default to HTTP/HTTPS
    return NetworkAccessCapability(allowed_hosts, allowed_ports, {Permission.CONNECT})


def create_admin_capability() -> Capability:
    """Create an admin capability with all permissions"""
    return Capability(
        name="admin",
        capability_type=CapabilityType.ADMIN,
        permissions=set(Permission),
        constraints={"all_access": True}
    )


def main():
    """Example usage of capability-based security system"""
    print("ION Capability-Based Security System Example")
    print("=" * 50)
    
    # Create enforcer
    enforcer = CapabilityEnforcer()
    
    # Create capabilities
    file_cap = create_file_read_capability(["/tmp", "/home/user"])
    network_cap = create_network_capability(["api.example.com"], [443])
    
    # Create security contexts
    user_context = enforcer.create_context("user", [file_cap])
    admin_context = enforcer.create_context("admin", [create_admin_capability()])
    
    # Register function with capability requirements
    def process_data(data: str, context: SecurityContext) -> str:
        """Function that requires file access"""
        return f"Processed: {data}"
    
    spec = CapabilitySpec(
        required_capabilities=["file_access"],
        required_permissions={CapabilityType.FILE_ACCESS: {Permission.READ}}
    )
    enforcer.register_function("process_data", spec)
    
    # Test access
    print("\n1. CAPABILITY CHECKING")
    print(f"   User has file_access: {user_context.has_capability('file_access')}")
    print(f"   User has network_access: {user_context.has_capability('network_access')}")
    print(f"   Admin has admin: {admin_context.has_capability('admin')}")
    
    # Test function access
    print("\n2. FUNCTION ACCESS CONTROL")
    try:
        enforcer.enforce_function_access(user_context, "process_data")
        print(f"   User can access process_data: True")
    except PermissionDeniedError as e:
        print(f"   User can access process_data: False ({e})")
    
    try:
        enforcer.enforce_function_access(user_context, "network_operation")
        print(f"   User can access network_operation: True")
    except PermissionDeniedError as e:
        print(f"   User can access network_operation: False (no restrictions)")
    
    # Test resource access
    print("\n3. RESOURCE ACCESS CONTROL")
    print(f"   User can read /tmp/file.txt: {enforcer.check_resource_access(user_context, CapabilityType.FILE_ACCESS, Permission.READ, '/tmp/file.txt')}")
    print(f"   User can read /etc/passwd: {enforcer.check_resource_access(user_context, CapabilityType.FILE_ACCESS, Permission.READ, '/etc/passwd')}")
    print(f"   User can connect to api.example.com:443: {enforcer.check_resource_access(user_context, CapabilityType.NETWORK_ACCESS, Permission.CONNECT, 'api.example.com')}")
    
    # Test capability revocation
    print("\n4. CAPABILITY REVOCATION")
    user_context.revoke_capability("file_access")
    print(f"   User has file_access after revocation: {user_context.has_capability('file_access')}")
    
    # Test audit log
    print("\n5. AUDIT LOG")
    print(f"   Total audit events: {len(enforcer.audit_log)}")
    print(f"   Access denied events: {len(enforcer.get_audit_log('access_denied'))}")
    print(f"   Access granted events: {len(enforcer.get_audit_log('access_granted'))}")
    
    # Test capability decorator
    print("\n6. CAPABILITY DECORATOR")
    decorator = CapabilityDecorator(enforcer)
    
    @decorator(required_capabilities=["file_access"])
    def secure_function(data: str, context: SecurityContext) -> str:
        return f"Securely processed: {data}"
    
    # Create new context with capabilities
    new_context = enforcer.create_context("new_user", [file_cap])
    
    try:
        result = secure_function("test data", new_context)
        print(f"   Decorated function executed: {result}")
    except PermissionDeniedError as e:
        print(f"   Decorated function denied: {e}")


if __name__ == "__main__":
    main()
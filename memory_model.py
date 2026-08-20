"""
ION Memory Model & Ownership System
Implementation of linear types, ownership tracking, and memory safety
Based on ION Complete Language Specification (August 2026)

Developer: ADITYA KAMBLE
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, TypeVar, Generic
from enum import Enum
import copy


class OwnershipError(Exception):
    """Ownership-related errors"""
    pass


class MemorySafetyError(Exception):
    """Memory safety violations"""
    pass


class BorrowError(Exception):
    """Borrow checker errors"""
    pass


class Mutability(Enum):
    """Mutability types"""
    IMMUTABLE = "immutable"
    MUTABLE = "mutable"
    CONST = "const"


class Lifetime(Enum):
    """Lifetime categories"""
    STATIC = "static"      # Lives for entire program
    AUTOMATIC = "automatic" # Stack-allocated, scoped
    DYNAMIC = "dynamic"     # Heap-allocated
    ANONYMOUS = "anonymous" # Temporary/rvalue


@dataclass
class MemoryRegion:
    """Memory region representation"""
    address: int
    size: int
    is_free: bool = True
    owner: Optional[str] = None  # Variable name that owns this region
    borrow_count: int = 0
    mutable_borrow: bool = False


@dataclass
class BorrowInfo:
    """Borrow tracking information"""
    borrower: str
    is_mutable: bool
    lifetime: str
    scope_start: int
    scope_end: int


@dataclass
class VariableInfo:
    """Variable information for ownership tracking"""
    name: str
    type_name: str
    mutability: Mutability
    lifetime: Lifetime
    is_owned: bool = True
    is_borrowed: bool = False
    borrows: List[BorrowInfo] = field(default_factory=list)
    current_borrower: Optional[str] = None


class MemoryManager:
    """Simple memory manager for tracking allocations"""
    
    def __init__(self, heap_size: int = 1024 * 1024):  # 1MB default
        self.heap_size = heap_size
        self.regions: List[MemoryRegion] = []
        self.next_address = 0
        self.initialize_heap()
    
    def initialize_heap(self):
        """Initialize heap as one free region"""
        self.regions.append(MemoryRegion(0, self.heap_size, True))
    
    def allocate(self, size: int, owner: str) -> int:
        """Allocate memory with ownership tracking"""
        # Find first free region that fits
        for i, region in enumerate(self.regions):
            if region.is_free and region.size >= size:
                # Split region if there's space left
                if region.size > size:
                    new_region = MemoryRegion(
                        region.address + size,
                        region.size - size,
                        True
                    )
                    self.regions.insert(i + 1, new_region)
                
                # Mark as allocated
                region.is_free = False
                region.owner = owner
                return region.address
        
        raise MemorySafetyError(f"Out of memory: cannot allocate {size} bytes")
    
    def free(self, address: int, expected_owner: str):
        """Free memory with ownership verification"""
        for region in self.regions:
            if region.address == address:
                if region.owner != expected_owner:
                    raise OwnershipError(
                        f"Ownership violation: {expected_owner} cannot free "
                        f"memory owned by {region.owner}"
                    )
                if region.borrow_count > 0:
                    raise BorrowError(
                        f"Cannot free memory with active borrows: {region.borrow_count}"
                    )
                region.is_free = True
                region.owner = None
                # Merge with adjacent free regions
                self.merge_free_regions()
                return
        
        raise MemorySafetyError(f"Invalid free address: {address}")
    
    def merge_free_regions(self):
        """Merge adjacent free regions"""
        i = 0
        while i < len(self.regions) - 1:
            if self.regions[i].is_free and self.regions[i + 1].is_free:
                # Merge regions
                self.regions[i].size += self.regions[i + 1].size
                self.regions.pop(i + 1)
            else:
                i += 1
    
    def get_memory_usage(self) -> Tuple[int, int]:
        """Get current memory usage (used, total)"""
        used = sum(region.size for region in self.regions if not region.is_free)
        return used, self.heap_size


class OwnershipTracker:
    """Track variable ownership and borrowing"""
    
    def __init__(self):
        self.variables: Dict[str, VariableInfo] = {}
        self.memory_manager = MemoryManager()
        self.scope_stack: List[Set[str]] = [set()]  # Stack of variable names per scope
    
    def enter_scope(self):
        """Enter a new scope"""
        self.scope_stack.append(set())
    
    def exit_scope(self):
        """Exit current scope and clean up variables"""
        current_scope = self.scope_stack.pop()
        for var_name in current_scope:
            self.drop_variable(var_name)
    
    def declare_variable(self, name: str, type_name: str, mutability: Mutability = Mutability.IMMUTABLE,
                         lifetime: Lifetime = Lifetime.AUTOMATIC) -> VariableInfo:
        """Declare a new variable with ownership"""
        if name in self.variables:
            raise OwnershipError(f"Variable '{name}' already declared")
        
        var_info = VariableInfo(
            name=name,
            type_name=type_name,
            mutability=mutability,
            lifetime=lifetime
        )
        
        self.variables[name] = var_info
        self.scope_stack[-1].add(name)
        
        return var_info
    
    def assign_variable(self, name: str, value: Any, size: int = 0):
        """Assign value to variable with memory allocation"""
        if name not in self.variables:
            raise OwnershipError(f"Variable '{name}' not declared")
        
        var_info = self.variables[name]
        
        if var_info.mutability == Mutability.CONST:
            raise OwnershipError(f"Cannot reassign const variable '{name}'")
        
        if var_info.mutability == Mutability.IMMUTABLE and var_info.is_owned:
            raise OwnershipError(f"Cannot reassign immutable variable '{name}'")
        
        # Free previous memory if owned
        if var_info.is_owned and hasattr(var_info, 'memory_address'):
            self.memory_manager.free(var_info.memory_address, name)
        
        # Allocate new memory if needed
        if size > 0:
            address = self.memory_manager.allocate(size, name)
            var_info.memory_address = address
        
        var_info.is_owned = True
    
    def borrow_variable(self, borrower: str, target: str, is_mutable: bool = False,
                      lifetime: str = "anonymous") -> BorrowInfo:
        """Borrow a variable with borrow checking rules"""
        if target not in self.variables:
            raise OwnershipError(f"Cannot borrow undeclared variable '{target}'")
        
        target_var = self.variables[target]
        
        # Check if variable is already borrowed
        if target_var.is_borrowed:
            if is_mutable or target_var.mutable_borrow:
                raise BorrowError(
                    f"Cannot borrow '{target}' as {'mutable' if is_mutable else 'immutable'} "
                    f"while it's already borrowed"
                )
        
        # Check mutability rules
        if is_mutable and target_var.mutability == Mutability.IMMUTABLE:
            raise BorrowError(
                f"Cannot borrow '{target}' as mutable - it's immutable"
            )
        
        # Create borrow info
        scope_level = len(self.scope_stack) - 1
        borrow_info = BorrowInfo(
            borrower=borrower,
            is_mutable=is_mutable,
            lifetime=lifetime,
            scope_start=scope_level,
            scope_end=scope_level  # Simplified - same scope for now
        )
        
        target_var.is_borrowed = True
        target_var.current_borrower = borrower
        target_var.mutable_borrow = is_mutable
        target_var.borrows.append(borrow_info)
        
        return borrow_info
    
    def return_borrow(self, borrower: str, target: str):
        """Return a borrowed variable"""
        if target not in self.variables:
            return
        
        target_var = self.variables[target]
        
        # Remove the borrow
        target_var.borrows = [b for b in target_var.borrows if b.borrower != borrower]
        
        if not target_var.borrows:
            target_var.is_borrowed = False
            target_var.current_borrower = None
            target_var.mutable_borrow = False
    
    def move_variable(self, source: str, destination: str):
        """Move ownership from source to destination"""
        if source not in self.variables:
            raise OwnershipError(f"Cannot move from undeclared variable '{source}'")
        
        source_var = self.variables[source]
        
        if not source_var.is_owned:
            raise OwnershipError(f"Cannot move from '{source}' - ownership already transferred")
        
        if source_var.is_borrowed:
            raise BorrowError(f"Cannot move '{source}' while it's borrowed")
        
        # Transfer ownership
        source_var.is_owned = False
        
        # Create destination variable
        dest_var = VariableInfo(
            name=destination,
            type_name=source_var.type_name,
            mutability=source_var.mutability,
            lifetime=source_var.lifetime,
            is_owned=True
        )
        
        if hasattr(source_var, 'memory_address'):
            dest_var.memory_address = source_var.memory_address
            # Update memory owner
            for region in self.memory_manager.regions:
                if region.address == dest_var.memory_address:
                    region.owner = destination
        
        self.variables[destination] = dest_var
        self.scope_stack[-1].add(destination)
    
    def drop_variable(self, name: str):
        """Drop a variable and free its memory"""
        if name not in self.variables:
            return
        
        var_info = self.variables[name]
        
        if var_info.is_owned and hasattr(var_info, 'memory_address'):
            try:
                self.memory_manager.free(var_info.memory_address, name)
            except (OwnershipError, BorrowError) as e:
                # Log but don't fail - this is cleanup
                pass
        
        del self.variables[name]
    
    def clone_variable(self, source: str, destination: str):
        """Clone a variable (deep copy)"""
        if source not in self.variables:
            raise OwnershipError(f"Cannot clone undeclared variable '{source}'")
        
        source_var = self.variables[source]
        
        # Create destination as a clone
        dest_var = VariableInfo(
            name=destination,
            type_name=source_var.type_name,
            mutability=source_var.mutability,
            lifetime=source_var.lifetime,
            is_owned=True
        )
        
        self.variables[destination] = dest_var
        self.scope_stack[-1].add(destination)
        
        return dest_var


class LinearType:
    """Linear type - must be used exactly once"""
    
    def __init__(self, value: Any, owner: str):
        self.value = value
        self.owner = owner
        self.is_consumed = False
    
    def consume(self, consumer: str) -> Any:
        """Consume the linear value"""
        if self.is_consumed:
            raise OwnershipError(
                f"Linear value already consumed by {self.owner}"
            )
        
        if consumer != self.owner:
            raise OwnershipError(
                f"Cannot consume linear value - wrong owner: {consumer} != {self.owner}"
            )
        
        self.is_consumed = True
        return self.value
    
    def is_valid(self) -> bool:
        """Check if linear value is still valid"""
        return not self.is_consumed


class Option:
    """Option type for null safety - enforces null handling"""
    
    def __init__(self, value: Any = None, is_some: bool = False):
        self.value = value
        self.is_some = is_some
    
    @staticmethod
    def some(value: Any) -> 'Option':
        """Create Some variant"""
        return Option(value, True)
    
    @staticmethod
    def none() -> 'Option':
        """Create None variant"""
        return Option(None, False)
    
    def is_some_value(self) -> bool:
        """Check if this is Some"""
        return self.is_some
    
    def is_none_value(self) -> bool:
        """Check if this is None"""
        return not self.is_some
    
    def unwrap(self) -> Any:
        """Unwrap the value, raise if None"""
        if self.is_none_value():
            raise MemorySafetyError("Attempted to unwrap None value")
        return self.value
    
    def unwrap_or(self, default: Any) -> Any:
        """Unwrap or return default"""
        return self.value if self.is_some else default
    
    def map(self, func) -> 'Option':
        """Apply function if Some"""
        if self.is_some:
            return Option.some(func(self.value))
        return Option.none()
    
    def and_then(self, func) -> 'Option':
        """Chain operations that return Options"""
        if self.is_some:
            return func(self.value)
        return Option.none()


class Result:
    """Result type for error handling without exceptions"""
    
    def __init__(self, value: Any = None, error: Any = None, is_ok: bool = True):
        self.value = value
        self.error = error
        self.is_ok = is_ok
    
    @staticmethod
    def ok(value: Any) -> 'Result':
        """Create Ok variant"""
        return Result(value, None, True)
    
    @staticmethod
    def err(error: Any) -> 'Result':
        """Create Err variant"""
        return Result(None, error, False)
    
    def is_ok_value(self) -> bool:
        """Check if this is Ok"""
        return self.is_ok
    
    def is_err_value(self) -> bool:
        """Check if this is Err"""
        return not self.is_ok
    
    def unwrap(self) -> Any:
        """Unwrap the value, raise if Err"""
        if self.is_err_value():
            raise MemorySafetyError(f"Attempted to unwrap Err: {self.error}")
        return self.value
    
    def unwrap_or(self, default: Any) -> Any:
        """Unwrap or return default"""
        return self.value if self.is_ok else default
    
    def map(self, func) -> 'Result':
        """Apply function if Ok"""
        if self.is_ok:
            return Result.ok(func(self.value))
        return Result.err(self.error)
    
    def map_err(self, func) -> 'Result':
        """Apply function to error if Err"""
        if self.is_err_value():
            return Result.err(func(self.error))
        return Result.ok(self.value)
    
    def and_then(self, func) -> 'Result':
        """Chain operations that return Results"""
        if self.is_ok:
            return func(self.value)
        return Result.err(self.error)


class SmartPointer:
    """Smart pointer base class"""
    
    def __init__(self, value: Any):
        self.value = value
    
    def deref(self) -> Any:
        """Dereference the pointer"""
        return self.value


class UniquePtr(SmartPointer):
    """Unique pointer - single ownership, no copying"""
    
    def __init__(self, value: Any):
        super().__init__(value)
        self.is_valid = True
    
    def move(self) -> 'UniquePtr':
        """Move ownership to new UniquePtr"""
        if not self.is_valid:
            raise OwnershipError("Cannot move from invalid UniquePtr")
        
        self.is_valid = False
        return UniquePtr(self.value)
    
    def deref(self) -> Any:
        """Dereference, check validity"""
        if not self.is_valid:
            raise MemorySafetyError("Attempted to dereference invalid UniquePtr")
        return super().deref()


class SharedPtr(SmartPointer):
    """Shared pointer - reference counted"""
    
    def __init__(self, value: Any):
        super().__init__(value)
        self.ref_count = 1
    
    def clone(self) -> 'SharedPtr':
        """Create new reference to same value"""
        self.ref_count += 1
        return SharedPtr(self.value)
    
    def drop(self):
        """Drop a reference"""
        self.ref_count -= 1
        if self.ref_count <= 0:
            # Value would be deallocated here
            pass
    
    def deref(self) -> Any:
        """Dereference"""
        return super().deref()


class BorrowChecker:
    """Borrow checker for enforcing Rust-like borrowing rules"""
    
    def __init__(self):
        self.active_borrows: Dict[str, List[BorrowInfo]] = {}
        self.ownership_map: Dict[str, str] = {}  # value -> owner
    
    def check_borrow_rules(self, borrower: str, target: str, is_mutable: bool) -> bool:
        """Check if borrow is allowed"""
        if target not in self.active_borrows:
            self.active_borrows[target] = []
        
        existing_borrows = self.active_borrows[target]
        
        # Rule 1: Can have multiple immutable borrows OR one mutable borrow
        if is_mutable:
            if existing_borrows:
                return False  # No other borrows allowed with mutable
        else:
            # Check for existing mutable borrow
            if any(b.is_mutable for b in existing_borrows):
                return False  # No immutable borrows if mutable exists
        
        return True
    
    def add_borrow(self, borrower: str, target: str, is_mutable: bool):
        """Add a borrow if rules allow"""
        if not self.check_borrow_rules(borrower, target, is_mutable):
            raise BorrowError(
                f"Borrow rules violated: {borrower} -> {target} "
                f"({'mutable' if is_mutable else 'immutable'})"
            )
        
        borrow_info = BorrowInfo(
            borrower=borrower,
            is_mutable=is_mutable,
            lifetime="current",
            scope_start=0,
            scope_end=0
        )
        
        self.active_borrows[target].append(borrow_info)
    
    def remove_borrow(self, borrower: str, target: str):
        """Remove a borrow"""
        if target in self.active_borrows:
            self.active_borrows[target] = [
                b for b in self.active_borrows[target] if b.borrower != borrower
            ]
    
    def transfer_ownership(self, from_owner: str, to_owner: str, value: str):
        """Transfer ownership of a value"""
        if value in self.ownership_map:
            current_owner = self.ownership_map[value]
            if current_owner != from_owner:
                raise OwnershipError(
                    f"Ownership transfer failed: {from_owner} does not own {value}"
                )
        
        self.ownership_map[value] = to_owner


def main():
    """Example usage of memory model and ownership system"""
    print("ION Memory Model & Ownership System Example")
    print("=" * 50)
    
    # Ownership tracking
    print("\n1. OWNERSHIP TRACKING")
    tracker = OwnershipTracker()
    tracker.enter_scope()
    
    # Declare variables
    tracker.declare_variable("x", "int", Mutability.IMMUTABLE)
    tracker.declare_variable("y", "int", Mutability.MUTABLE)
    
    # Assign values
    tracker.assign_variable("x", 42, size=4)
    tracker.assign_variable("y", 100, size=4)
    
    print(f"   Variables declared: x, y")
    print(f"   Memory usage: {tracker.memory_manager.get_memory_usage()}")
    
    # Borrowing
    print("\n2. BORROW CHECKING")
    tracker.borrow_variable("func1", "x", is_mutable=False)
    print(f"   Successfully borrowed x as immutable")
    
    try:
        tracker.borrow_variable("func2", "x", is_mutable=True)
        print(f"   ERROR: Should not reach here")
    except BorrowError as e:
        print(f"   Correctly prevented mutable borrow: {e}")
    
    # Ownership transfer
    print("\n3. OWNERSHIP TRANSFER")
    tracker.move_variable("x", "z")
    print(f"   Moved ownership from x to z")
    
    # Option type
    print("\n4. OPTION TYPE (Null Safety)")
    some_value = Option.some(42)
    none_value = Option.none()
    
    print(f"   Some value: {some_value.unwrap()}")
    print(f"   Unwrap or default: {none_value.unwrap_or(0)}")
    
    try:
        none_value.unwrap()
        print(f"   ERROR: Should not reach here")
    except MemorySafetyError as e:
        print(f"   Correctly prevented unwrap of None: {e}")
    
    # Result type
    print("\n5. RESULT TYPE (Error Handling)")
    ok_result = Result.ok(42)
    err_result = Result.err("Something went wrong")
    
    print(f"   Ok result: {ok_result.unwrap()}")
    print(f"   Err unwrap or: {err_result.unwrap_or(0)}")
    
    # Smart pointers
    print("\n6. SMART POINTERS")
    unique = UniquePtr("unique data")
    shared = SharedPtr("shared data")
    
    shared_clone = shared.clone()
    print(f"   Shared pointer ref count: {shared.ref_count}")
    
    # Linear types
    print("\n7. LINEAR TYPES")
    linear = LinearType("linear data", "owner1")
    consumed = linear.consume("owner1")
    print(f"   Consumed linear value: {consumed}")
    
    try:
        linear.consume("owner1")
        print(f"   ERROR: Should not reach here")
    except OwnershipError as e:
        print(f"   Correctly prevented double consumption: {e}")
    
    # Clean up
    tracker.exit_scope()
    print(f"\n8. CLEANUP")
    print(f"   Final memory usage: {tracker.memory_manager.get_memory_usage()}")


if __name__ == "__main__":
    main()
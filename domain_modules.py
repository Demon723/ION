"""
ION Domain-Specific Modules
Implementation of domain modules: Robotics, Quantum, AI/ML, Space, IoT, Bio, XR
Based on ION Complete Language Specification (August 2026)

Developer: ADITYA KAMBLE
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Tuple
from enum import Enum
import math


class Domain(Enum):
    """Domain types for ION modules"""
    ROBOTICS = "robotics"
    QUANTUM = "quantum"
    AI_ML = "ai"
    SPACE = "space"
    IOT = "iot"
    BIO = "bio"
    XR = "xr"


# ==================== ROBOTICS MODULE ====================

class RobotControlMode(Enum):
    """Robot control modes"""
    POSITION = "position"
    VELOCITY = "velocity"
    TORQUE = "torque"
    IMPEDANCE = "impedance"


@dataclass
class JointState:
    """Robot joint state"""
    positions: List[float]
    velocities: List[float]
    torques: List[float]
    timestamp: float = 0.0


@dataclass
class Pose3D:
    """3D pose with position and orientation"""
    x: float
    y: float
    z: float
    qw: float = 1.0  # Quaternion w
    qx: float = 0.0  # Quaternion x
    qy: float = 0.0  # Quaternion y
    qz: float = 0.0  # Quaternion z
    
    def distance_to(self, other: 'Pose3D') -> float:
        """Calculate Euclidean distance to another pose"""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)


@dataclass
class TrajectoryPoint:
    """Single trajectory point"""
    pose: Pose3D
    time: float
    velocity: Optional[List[float]] = None


class RobotKinematics:
    """Robot kinematics solver"""
    
    @staticmethod
    def forward_kinematics(joint_angles: List[float], dh_params: List[Tuple]) -> Pose3D:
        """Compute forward kinematics using DH parameters"""
        # Simplified FK computation
        x, y, z = 0.0, 0.0, 0.0
        for i, (theta, d, a, alpha) in enumerate(dh_params):
            angle = joint_angles[i] + theta
            x += a * math.cos(angle)
            y += a * math.sin(angle)
            z += d
        
        return Pose3D(x=x, y=y, z=z)
    
    @staticmethod
    def inverse_kinematics(target_pose: Pose3D, dh_params: List[Tuple]) -> List[float]:
        """Compute inverse kinematics (simplified)"""
        # Simplified IK computation
        joint_angles = []
        for i, (theta, d, a, alpha) in enumerate(dh_params):
            # Simplified analytical solution
            angle = math.atan2(target_pose.y, target_pose.x) + theta
            joint_angles.append(angle)
        
        return joint_angles


class RobotController:
    """Robot motion controller"""
    
    def __init__(self, control_mode: RobotControlMode = RobotControlMode.POSITION):
        self.control_mode = control_mode
        self.state = JointState([], [], [])
        self.current_pose = Pose3D(0, 0, 0)
    
    def compute_control(self, target: Pose3D, dt: float = 0.001) -> List[float]:
        """Compute control output"""
        if self.control_mode == RobotControlMode.POSITION:
            return self._position_control(target, dt)
        elif self.control_mode == RobotControlMode.VELOCITY:
            return self._velocity_control(target, dt)
        elif self.control_mode == RobotControlMode.TORQUE:
            return self._torque_control(target, dt)
        else:
            return self._impedance_control(target, dt)
    
    def _position_control(self, target: Pose3D, dt: float) -> List[float]:
        """Position control law"""
        kp = 100.0  # Proportional gain
        error_x = target.x - self.current_pose.x
        error_y = target.y - self.current_pose.y
        error_z = target.z - self.current_pose.z
        
        return [kp * error_x, kp * error_y, kp * error_z]
    
    def _velocity_control(self, target: Pose3D, dt: float) -> List[float]:
        """Velocity control law"""
        kv = 50.0  # Velocity gain
        return self._position_control(target, dt)  # Simplified
    
    def _torque_control(self, target: Pose3D, dt: float) -> List[float]:
        """Torque control law"""
        kt = 10.0  # Torque gain
        return self._position_control(target, dt)  # Simplified
    
    def _impedance_control(self, target: Pose3D, dt: float) -> List[float]:
        """Impedance control law"""
        k_imp = 20.0  # Impedance gain
        d_imp = 5.0   # Damping
        return self._position_control(target, dt)  # Simplified


# ==================== QUANTUM MODULE ====================

class QuantumGate(Enum):
    """Quantum gate types"""
    H = "H"          # Hadamard
    X = "X"          # Pauli-X
    Y = "Y"          # Pauli-Y
    Z = "Z"          # Pauli-Z
    S = "S"          # Phase gate
    T = "T"          # T gate
    CNOT = "CNOT"    # CNOT
    CZ = "CZ"        # Controlled-Z
    SWAP = "SWAP"    # SWAP
    MEASURE = "MEASURE"


@dataclass
class QuantumOperation:
    """Single quantum operation"""
    gate: QuantumGate
    qubits: List[int]
    params: List[float] = field(default_factory=list)


@dataclass
class QuantumCircuit:
    """Quantum circuit representation"""
    num_qubits: int
    operations: List[QuantumOperation]
    
    def add_gate(self, gate: QuantumGate, qubits: List[int], params: List[float] = None):
        """Add a gate to the circuit"""
        if params is None:
            params = []
        self.operations.append(QuantumOperation(gate, qubits, params))
    
    def depth(self) -> int:
        """Calculate circuit depth"""
        return len(self.operations)
    
    def to_openqasm(self) -> str:
        """Convert to OpenQASM format"""
        qasm = f"OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[{self.num_qubits}];\ncreg c[{self.num_qubits}];\n"
        
        for op in self.operations:
            if op.gate == QuantumGate.H:
                qasm += f"h q[{op.qubits[0]}];\n"
            elif op.gate == QuantumGate.X:
                qasm += f"x q[{op.qubits[0]}];\n"
            elif op.gate == QuantumGate.CNOT:
                qasm += f"cx q[{op.qubits[0]}], q[{op.qubits[1]}];\n"
            elif op.gate == QuantumGate.MEASURE:
                qasm += f"measure q[{op.qubits[0]}] -> c[{op.qubits[0]}];\n"
        
        return qasm


class QuantumSimulator:
    """Simple quantum circuit simulator"""
    
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.state = [complex(1.0, 0.0)] + [complex(0.0, 0.0)] * (2**num_qubits - 1)
    
    def apply_gate(self, gate: QuantumGate, qubits: List[int]):
        """Apply a quantum gate"""
        # Simplified gate application
        if gate == QuantumGate.H:
            self._apply_hadamard(qubits[0])
        elif gate == QuantumGate.X:
            self._apply_pauli_x(qubits[0])
        elif gate == QuantumGate.CNOT:
            self._apply_cnot(qubits[0], qubits[1])
    
    def _apply_hadamard(self, qubit: int):
        """Apply Hadamard gate"""
        # Simplified H gate application
        for i in range(len(self.state)):
            if (i >> qubit) & 1:
                j = i ^ (1 << qubit)
                self.state[i], self.state[j] = (self.state[i] + self.state[j]) / math.sqrt(2), (self.state[i] - self.state[j]) / math.sqrt(2)
    
    def _apply_pauli_x(self, qubit: int):
        """Apply Pauli-X gate"""
        for i in range(len(self.state)):
            if (i >> qubit) & 1:
                j = i ^ (1 << qubit)
                self.state[i], self.state[j] = self.state[j], self.state[i]
    
    def _apply_cnot(self, control: int, target: int):
        """Apply CNOT gate"""
        for i in range(len(self.state)):
            if (i >> control) & 1:
                j = i ^ (1 << target)
                self.state[i], self.state[j] = self.state[j], self.state[i]
    
    def measure(self, qubit: int) -> int:
        """Measure a qubit"""
        # Simplified measurement
        prob_0 = sum(abs(self.state[i])**2 for i in range(len(self.state)) if not ((i >> qubit) & 1))
        import random
        return 0 if random.random() < prob_0 else 1


# ==================== AI/ML MODULE ====================

class Activation(Enum):
    """Neural network activation functions"""
    RELU = "relu"
    SIGMOID = "sigmoid"
    TANH = "tanh"
    GELU = "gelu"
    SOFTMAX = "softmax"


@dataclass
class Tensor:
    """Multi-dimensional tensor"""
    shape: Tuple[int, ...]
    data: List[float]
    
    def __post_init__(self):
        expected_size = 1
        for dim in self.shape:
            expected_size *= dim
        if len(self.data) != expected_size:
            raise ValueError(f"Data size {len(self.data)} doesn't match shape {self.shape}")
    
    def get(self, indices: Tuple[int, ...]) -> float:
        """Get value at indices"""
        index = 0
        stride = 1
        for i in reversed(range(len(self.shape))):
            index += indices[i] * stride
            stride *= self.shape[i]
        return self.data[index]
    
    def set(self, indices: Tuple[int, ...], value: float):
        """Set value at indices"""
        index = 0
        stride = 1
        for i in reversed(range(len(self.shape))):
            index += indices[i] * stride
            stride *= self.shape[i]
        self.data[index] = value


@dataclass
class NeuralLayer:
    """Neural network layer"""
    input_size: int
    output_size: int
    activation: Activation
    weights: Optional[Tensor] = None
    biases: Optional[Tensor] = None
    
    def __post_init__(self):
        if self.weights is None:
            # Initialize weights randomly
            import random
            self.weights = Tensor((self.input_size, self.output_size),
                                 [random.uniform(-0.1, 0.1) for _ in range(self.input_size * self.output_size)])
        if self.biases is None:
            self.biases = Tensor((self.output_size,), [0.0] * self.output_size)
    
    def forward(self, x: Tensor) -> Tensor:
        """Forward pass through layer"""
        # Simplified matrix multiplication
        output_data = []
        for j in range(self.output_size):
            sum_val = 0.0
            for i in range(self.input_size):
                sum_val += x.get((i,)) * self.weights.get((i, j))
            sum_val += self.biases.get((j,))
            
            # Apply activation
            if self.activation == Activation.RELU:
                sum_val = max(0.0, sum_val)
            elif self.activation == Activation.SIGMOID:
                sum_val = 1.0 / (1.0 + math.exp(-sum_val))
            elif self.activation == Activation.TANH:
                sum_val = math.tanh(sum_val)
            
            output_data.append(sum_val)
        
        return Tensor((self.output_size,), output_data)


class NeuralNetwork:
    """Neural network model"""
    
    def __init__(self, layers: List[NeuralLayer]):
        self.layers = layers
    
    def forward(self, x: Tensor) -> Tensor:
        """Forward pass through network"""
        current = x
        for layer in self.layers:
            current = layer.forward(current)
        return current
    
    def predict(self, x: List[float]) -> List[float]:
        """Make prediction"""
        input_tensor = Tensor((len(x),), x)
        output = self.forward(input_tensor)
        return output.data


# ==================== SPACE MODULE ====================

@dataclass
class OrbitalElements:
    """Keplerian orbital elements"""
    semi_major_axis: float  # a (km)
    eccentricity: float     # e
    inclination: float      # i (rad)
    raan: float            # Ω (rad) - Right ascension of ascending node
    arg_periapsis: float    # ω (rad) - Argument of periapsis
    true_anomaly: float     # ν (rad) - True anomaly


@dataclass
class Quaternion:
    """Quaternion for attitude representation"""
    w: float
    x: float
    y: float
    z: float
    
    def normalize(self) -> 'Quaternion':
        """Normalize quaternion"""
        norm = math.sqrt(self.w**2 + self.x**2 + self.y**2 + self.z**2)
        return Quaternion(self.w/norm, self.x/norm, self.y/norm, self.z/norm)
    
    def multiply(self, other: 'Quaternion') -> 'Quaternion':
        """Quaternion multiplication"""
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)


class OrbitalMechanics:
    """Orbital mechanics calculations"""
    
    MU_EARTH = 398600.4418  # Earth's gravitational parameter (km³/s²)
    
    @staticmethod
    def orbital_period(semi_major_axis: float) -> float:
        """Calculate orbital period using Kepler's third law"""
        return 2 * math.pi * math.sqrt(semi_major_axis**3 / OrbitalMechanics.MU_EARTH)
    
    @staticmethod
    def orbital_velocity(orbit: OrbitalElements) -> float:
        """Calculate orbital velocity"""
        r = orbit.semi_major_axis * (1 - orbit.eccentricity**2) / (1 + orbit.eccentricity * math.cos(orbit.true_anomaly))
        return math.sqrt(OrbitalMechanics.MU_EARTH * (2/r - 1/orbit.semi_major_axis))
    
    @staticmethod
    def propagate_orbit(orbit: OrbitalElements, dt: float) -> OrbitalElements:
        """Propagate orbit forward in time (simplified)"""
        # Mean motion
        n = math.sqrt(OrbitalMechanics.MU_EARTH / orbit.semi_major_axis**3)
        
        # Update true anomaly (simplified)
        new_true_anomaly = orbit.true_anomaly + n * dt
        
        return OrbitalElements(
            semi_major_axis=orbit.semi_major_axis,
            eccentricity=orbit.eccentricity,
            inclination=orbit.inclination,
            raan=orbit.raan,
            arg_periapsis=orbit.arg_periapsis,
            true_anomaly=new_true_anomaly
        )


class AttitudeControl:
    """Spacecraft attitude control"""
    
    @staticmethod
    def quaternion_to_euler(q: Quaternion) -> Tuple[float, float, float]:
        """Convert quaternion to Euler angles"""
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (q.w * q.x + q.y * q.z)
        cosr_cosp = 1 - 2 * (q.x**2 + q.y**2)
        roll = math.atan2(sinr_cosp, cosr_cosp)
        
        # Pitch (y-axis rotation)
        sinp = 2 * (q.w * q.y - q.z * q.x)
        pitch = math.asin(sinp) if abs(sinp) <= 1 else math.copysign(math.pi/2, sinp)
        
        # Yaw (z-axis rotation)
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y**2 + q.z**2)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        return roll, pitch, yaw
    
    @staticmethod
    def euler_to_quaternion(roll: float, pitch: float, yaw: float) -> Quaternion:
        """Convert Euler angles to quaternion"""
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)
        
        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy
        
        return Quaternion(w, x, y, z)


# ==================== IOT MODULE ====================

class SensorType(Enum):
    """IoT sensor types"""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    ACCELEROMETER = "accelerometer"
    GYROSCOPE = "gyroscope"
    LIGHT = "light"
    PROXIMITY = "proximity"


@dataclass
class SensorReading:
    """Sensor reading with metadata"""
    sensor_id: str
    sensor_type: SensorType
    value: float
    unit: str
    timestamp: float
    quality: float = 1.0  # Signal quality (0-1)


class SensorFusion:
    """Sensor fusion algorithms"""
    
    @staticmethod
    def complementary_filter(acc_data: List[float], gyro_data: List[float], 
                           alpha: float = 0.98) -> List[float]:
        """Complementary filter for IMU data fusion"""
        # Simplified complementary filter
        fused = []
        for acc, gyro in zip(acc_data, gyro_data):
            fused.append(alpha * gyro + (1 - alpha) * acc)
        return fused
    
    @staticmethod
    def kalman_filter(measurement: float, prediction: float, 
                     measurement_uncertainty: float, estimation_uncertainty: float) -> Tuple[float, float]:
        """Simple Kalman filter"""
        # Kalman gain
        kalman_gain = estimation_uncertainty / (estimation_uncertainty + measurement_uncertainty)
        
        # Update estimate
        estimate = prediction + kalman_gain * (measurement - prediction)
        
        # Update uncertainty
        new_uncertainty = (1 - kalman_gain) * estimation_uncertainty
        
        return estimate, new_uncertainty


class IoTProtocol(Enum):
    """IoT communication protocols"""
    MQTT = "mqtt"
    COAP = "coap"
    LORAWAN = "lorawan"
    ZIGBEE = "zigbee"
    BLE = "ble"


@dataclass
class IoTMessage:
    """IoT message"""
    topic: str
    payload: str
    qos: int = 0
    retain: bool = False


# ==================== BIO MODULE ====================

class DNABase(Enum):
    """DNA nucleotide bases"""
    A = "A"  # Adenine
    T = "T"  # Thymine
    G = "G"  # Guanine
    C = "C"  # Cytosine


@dataclass
class DNASequence:
    """DNA sequence representation"""
    sequence: str
    
    def complement(self) -> str:
        """Get complementary DNA strand"""
        complement_map = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
        return ''.join(complement_map[base] for base in self.sequence)
    
    def transcribe(self) -> str:
        """Transcribe DNA to RNA"""
        return self.sequence.replace('T', 'U')
    
    def gc_content(self) -> float:
        """Calculate GC content percentage"""
        gc_count = self.sequence.count('G') + self.sequence.count('C')
        return (gc_count / len(self.sequence)) * 100 if self.sequence else 0.0


class ProteinStructure:
    """Protein structure analysis"""
    
    @staticmethod
    def hydrophobicity_index(amino_acid: str) -> float:
        """Get hydrophobicity index for amino acid"""
        # Simplified Kyte-Doolittle scale
        hydrophobicity = {
            'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
            'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
            'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
            'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
        }
        return hydrophobicity.get(amino_acid.upper(), 0.0)
    
    @staticmethod
    def predict_secondary_structure(sequence: str) -> str:
        """Simple secondary structure prediction"""
        # Very simplified prediction
        structure = ""
        for aa in sequence:
            if aa in ['A', 'V', 'I', 'L', 'M']:
                structure += 'H'  # Helix
            elif aa in ['E', 'D', 'K', 'R']:
                structure += 'E'  # Sheet
            else:
                structure += 'C'  # Coil
        return structure


# ==================== XR MODULE ====================

@dataclass
class Vector3:
    """3D vector for XR applications"""
    x: float
    y: float
    z: float
    
    def normalize(self) -> 'Vector3':
        """Normalize vector"""
        length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
        if length == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x/length, self.y/length, self.z/length)
    
    def dot(self, other: 'Vector3') -> float:
        """Dot product"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3') -> 'Vector3':
        """Cross product"""
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )


@dataclass
class XRAnchor:
    """Spatial anchor for XR"""
    id: str
    position: Vector3
    rotation: Quaternion
    timestamp: float


@dataclass
class SpatialMapping:
    """Spatial mapping data"""
    mesh_vertices: List[Vector3]
    mesh_indices: List[Tuple[int, int, int]]
    surface_type: str  # "floor", "wall", "ceiling", "table", etc.


class XRInput:
    """XR input handling"""
    
    @staticmethod
    def ray_intersection(ray_origin: Vector3, ray_direction: Vector3, 
                        triangle: Tuple[Vector3, Vector3, Vector3]) -> Optional[Vector3]:
        """Ray-triangle intersection for XR interaction"""
        # Simplified ray-triangle intersection
        v0, v1, v2 = triangle
        
        edge1 = Vector3(v1.x - v0.x, v1.y - v0.y, v1.z - v0.z)
        edge2 = Vector3(v2.x - v0.x, v2.y - v0.y, v2.z - v0.z)
        
        h = ray_direction.cross(edge2)
        a = edge1.dot(h)
        
        if abs(a) < 0.00001:
            return None
        
        f = 1.0 / a
        s = Vector3(ray_origin.x - v0.x, ray_origin.y - v0.y, ray_origin.z - v0.z)
        u = f * s.dot(h)
        
        if u < 0.0 or u > 1.0:
            return None
        
        q = s.cross(edge1)
        v = f * ray_direction.dot(q)
        
        if v < 0.0 or u + v > 1.0:
            return None
        
        t = f * edge2.dot(q)
        
        if t > 0.00001:
            return Vector3(
                ray_origin.x + ray_direction.x * t,
                ray_origin.y + ray_direction.y * t,
                ray_origin.z + ray_direction.z * t
            )
        
        return None


# ==================== DOMAIN MODULE REGISTRY ====================

class DomainModuleRegistry:
    """Registry for domain-specific modules"""
    
    def __init__(self):
        self.modules = {
            Domain.ROBOTICS: {
                'kinematics': RobotKinematics,
                'controller': RobotController,
                'types': {'JointState': JointState, 'Pose3D': Pose3D, 'TrajectoryPoint': TrajectoryPoint}
            },
            Domain.QUANTUM: {
                'circuit': QuantumCircuit,
                'simulator': QuantumSimulator,
                'gates': QuantumGate
            },
            Domain.AI_ML: {
                'tensor': Tensor,
                'layer': NeuralLayer,
                'network': NeuralNetwork,
                'activation': Activation
            },
            Domain.SPACE: {
                'orbital': OrbitalMechanics,
                'attitude': AttitudeControl,
                'types': {'OrbitalElements': OrbitalElements, 'Quaternion': Quaternion}
            },
            Domain.IOT: {
                'sensor': {'types': SensorType, 'reading': SensorReading},
                'fusion': SensorFusion,
                'protocol': IoTProtocol
            },
            Domain.BIO: {
                'dna': DNASequence,
                'protein': ProteinStructure
            },
            Domain.XR: {
                'vector': Vector3,
                'anchor': XRAnchor,
                'mapping': SpatialMapping,
                'input': XRInput
            }
        }
    
    def get_module(self, domain: Domain, module_name: str):
        """Get a specific module from a domain"""
        if domain in self.modules and module_name in self.modules[domain]:
            return self.modules[domain][module_name]
        return None
    
    def list_domains(self) -> List[str]:
        """List all available domains"""
        return [domain.value for domain in self.modules.keys()]
    
    def list_modules(self, domain: Domain) -> List[str]:
        """List modules in a domain"""
        if domain in self.modules:
            return list(self.modules[domain].keys())
        return []


# Global domain registry
domain_registry = DomainModuleRegistry()


def main():
    """Example usage of domain modules"""
    print("ION Domain Modules Example")
    print("=" * 50)
    
    # Robotics example
    print("\n1. ROBOTICS MODULE")
    robot = RobotController(RobotControlMode.POSITION)
    target = Pose3D(1.0, 2.0, 3.0)
    control = robot.compute_control(target)
    print(f"   Control output: {control}")
    
    # Quantum example
    print("\n2. QUANTUM MODULE")
    circuit = QuantumCircuit(2, [])
    circuit.add_gate(QuantumGate.H, [0])
    circuit.add_gate(QuantumGate.CNOT, [0, 1])
    print(f"   Circuit depth: {circuit.depth()}")
    print(f"   OpenQASM:\n{circuit.to_openqasm()}")
    
    # AI/ML example
    print("\n3. AI/ML MODULE")
    layer = NeuralLayer(3, 2, Activation.RELU)
    input_tensor = Tensor((3,), [1.0, 2.0, 3.0])
    output = layer.forward(input_tensor)
    print(f"   Layer output: {output.data}")
    
    # Space example
    print("\n4. SPACE MODULE")
    orbit = OrbitalElements(7000, 0.01, 0.5, 0.3, 0.2, 0.1)
    period = OrbitalMechanics.orbital_period(orbit.semi_major_axis)
    print(f"   Orbital period: {period:.2f} seconds")
    
    # IoT example
    print("\n5. IOT MODULE")
    reading = SensorReading("temp_001", SensorType.TEMPERATURE, 25.5, "C", 1234567890.0)
    print(f"   Sensor reading: {reading.value} {reading.unit}")
    
    # Bio example
    print("\n6. BIO MODULE")
    dna = DNASequence("ATCGATCG")
    print(f"   Complement: {dna.complement()}")
    print(f"   GC content: {dna.gc_content():.1f}%")
    
    # XR example
    print("\n7. XR MODULE")
    vec = Vector3(1, 2, 3).normalize()
    print(f"   Normalized vector: ({vec.x:.3f}, {vec.y:.3f}, {vec.z:.3f})")
    
    print("\nDomain Registry:")
    print(f"   Available domains: {domain_registry.list_domains()}")
    print(f"   Robotics modules: {domain_registry.list_modules(Domain.ROBOTICS)}")


if __name__ == "__main__":
    main()
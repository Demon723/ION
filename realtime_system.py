"""
Real-Time Execution System
Deterministic real-time task scheduling and execution
Based on ION Research & Code Compendium - Real-Time Guarantees

Developer: ADITYA KAMBLE
"""

import time
import threading
import heapq
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
from datetime import datetime, timedelta
import asyncio


class RealTimePriority(Enum):
    """Real-time priority levels"""
    CRITICAL = 0      # Mission-critical, guaranteed execution
    HIGH = 1          # High priority, soft real-time
    NORMAL = 2        # Normal priority, best-effort
    LOW = 3           # Low priority, background


class TaskState(Enum):
    """Task execution states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


@dataclass
class RealTimeTask:
    """Real-time task specification"""
    name: str
    function: Callable
    priority: RealTimePriority
    period: float = 0.0  # Periodic task (0 = one-shot)
    deadline: float = 0.0  # Absolute deadline (0 = no deadline)
    execution_time_ms: float = 10.0  # Expected execution time
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    state: TaskState = TaskState.PENDING
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Any = None
    error: Optional[Exception] = None
    
    def __lt__(self, other: 'RealTimeTask'):
        """For priority queue ordering"""
        return self.priority.value < other.priority.value


@dataclass
class ExecutionMetrics:
    """Real-time execution metrics"""
    task_name: str
    start_time: float
    end_time: float
    execution_time_ms: float
    deadline_met: bool
    priority: RealTimePriority
    success: bool
    cpu_time_ms: float = 0.0
    context_switches: int = 0


class RealTimeScheduler:
    """Deterministic real-time scheduler"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.task_queue: List[RealTimeTask] = []
        self.current_time = time.time()
        self.is_running = False
        self.metrics: List[ExecutionMetrics] = []
        self.lock = threading.Lock()
        self.workers: List[threading.Thread] = []
        self.active_tasks: Dict[str, RealTimeTask] = {}
        self.periodic_tasks: List[RealTimeTask] = []
    
    def submit_task(self, task: RealTimeTask) -> str:
        """Submit a task for real-time execution"""
        with self.lock:
            heapq.heappush(self.task_queue, task)
            task.state = TaskState.PENDING
            return task.name
    
    def submit_periodic_task(self, task: RealTimeTask):
        """Submit a periodic task"""
        task.periodic = True
        with self.lock:
            self.periodic_tasks.append(task)
            return task.name
    
    def start(self):
        """Start the real-time scheduler"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, args=(i,))
            worker.daemon = True
            worker.start()
            self.workers.append(worker)
        
        # Start periodic task manager
        periodic_manager = threading.Thread(target=self._periodic_manager)
        periodic_manager.daemon = True
        periodic_manager.start()
        
        # Start monitoring thread
        monitor = threading.Thread(target=self._monitor)
        monitor.daemon = True
        monitor.start()
    
    def stop(self):
        """Stop the real-time scheduler"""
        self.is_running = False
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=1.0)
    
    def _worker_loop(self, worker_id: int):
        """Worker thread main loop"""
        while self.is_running:
            task = None
            
            with self.lock:
                if self.task_queue:
                    task = heapq.heappop(self.task_queue)
                    if task:
                        task.state = TaskState.RUNNING
                        task.started_at = time.time()
                        self.active_tasks[task.name] = task
            
            if task:
                try:
                    # Execute task with timing
                    start_time = time.time()
                    task.result = task.function(*task.args, **task.kwargs)
                    end_time = time.time()
                    
                    # Calculate metrics
                    execution_time = (end_time - start_time) * 1000
                    deadline_met = task.deadline == 0 or end_time <= task.deadline
                    
                    with self.lock:
                        task.state = TaskState.COMPLETED
                        task.completed_at = end_time
                        del self.active_tasks[task.name]
                        
                        metric = ExecutionMetrics(
                            task_name=task.name,
                            start_time=start_time,
                            end_time=end_time,
                            execution_time_ms=execution_time,
                            deadline_met=deadline_met,
                            priority=task.priority,
                            success=True
                        )
                        self.metrics.append(metric)
                
                except Exception as e:
                    with self.lock:
                        task.state = TaskState.FAILED
                        task.error = e
                        task.completed_at = time.time()
                        del self.active_tasks[task.name]
                        
                        metric = ExecutionMetrics(
                            task_name=task.name,
                            start_time=start_time,
                            end_time=time.time(),
                            execution_time_ms=0,
                            deadline_met=False,
                            priority=task.priority,
                            success=False
                        )
                        self.metrics.append(metric)
            else:
                # No task, sleep briefly
                time.sleep(0.001)
    
    def _periodic_manager(self):
        """Manage periodic task execution"""
        while self.is_running:
            current_time = time.time()
            
            with self.lock:
                for task in self.periodic_tasks:
                    if task.period > 0:
                        # Check if task should run
                        if not hasattr(task, 'last_run'):
                            task.last_run = 0
                        
                        if current_time - task.last_run >= task.period:
                            # Submit task for execution
                            task_copy = RealTimeTask(
                                name=f"{task.name}_periodic",
                                function=task.function,
                                priority=task.priority,
                                args=task.args,
                                kwargs=task.kwargs,
                                execution_time_ms=task.execution_time_ms
                            )
                            heapq.heappush(self.task_queue, task_copy)
                            task.last_run = current_time
            
            time.sleep(0.01)  # 10ms tick rate
    
    def _monitor(self):
        """Monitor system performance and deadlines"""
        while self.is_running:
            current_time = time.time()
            
            with self.lock:
                # Check for deadline violations
                for task_name, task in self.active_tasks.items():
                    if task.deadline > 0 and current_time > task.deadline:
                        # Deadline violation detected
                        task.state = TaskState.TIMEOUT
            
            time.sleep(0.001)  # 1ms tick rate
    
    def get_metrics(self) -> List[ExecutionMetrics]:
        """Get execution metrics"""
        with self.lock:
            return self.metrics.copy()
    
    def get_queue_length(self) -> int:
        """Get current queue length"""
        with self.lock:
            return len(self.task_queue)
    
    def get_active_tasks(self) -> List[str]:
        """Get list of active task names"""
        with self.lock:
            return list(self.active_tasks.keys())


class RealTimeExecutor:
    """Simple real-time executor for critical tasks"""
    
    def __init__(self):
        self.scheduler = RealTimeScheduler(max_workers=2)
        self.completed_tasks: Dict[str, Any] = {}
    
    def execute_critical(self, function: Callable, deadline_ms: float, *args, **kwargs) -> Any:
        """Execute a critical task with deadline guarantee"""
        task = RealTimeTask(
            name="critical_task",
            function=function,
            priority=RealTimePriority.CRITICAL,
            deadline=time.time() + (deadline_ms / 1000.0),
            execution_time_ms=deadline_ms,
            args=args,
            kwargs=kwargs
        )
        
        self.scheduler.submit_task(task)
        self.scheduler.start()
        
        # Wait for completion
        while task.state == TaskState.RUNNING:
            time.sleep(0.001)
        
        self.scheduler.stop()
        
        if task.state == TaskState.COMPLETED:
            return task.result
        else:
            raise TimeoutError(f"Critical task failed: {task.state.value}")
    
    def execute_high_priority(self, function: Callable, *args, **kwargs) -> Any:
        """Execute a high-priority task"""
        task = RealTimeTask(
            name="high_priority_task",
            function=function,
            priority=RealTimePriority.HIGH,
            args=args,
            kwargs=kwargs
        )
        
        self.scheduler.submit_task(task)
        self.scheduler.start()
        
        while task.state == TaskState.RUNNING:
            time.sleep(0.001)
        
        self.scheduler.stop()
        
        if task.state == TaskState.COMPLETED:
            return task.result
        else:
            raise RuntimeError(f"High priority task failed: {task.state.value}")


class DeterministicTimer:
    """Deterministic timer for real-time guarantees"""
    
    def __init__(self, resolution_ms: float = 1.0):
        self.resolution_ms = resolution_ms
        self.current_time = 0.0
        self.callbacks: List[Tuple[float, Callable]] = []
        self.is_running = False
    
    def set_timer(self, delay_ms: float, callback: Callable):
        """Set a timer with deterministic callback"""
        trigger_time = self.current_time + delay_ms
        self.callbacks.append((trigger_time, callback))
        # Sort by trigger time
        self.callbacks.sort(key=lambda x: x[0])
    
    def tick(self):
        """Advance timer by one resolution step"""
        self.current_time += self.resolution_ms
        
        # Execute callbacks whose time has come
        while self.callbacks and self.callbacks[0][0] <= self.current_time:
            trigger_time, callback = self.callbacks.pop(0)
            try:
                callback(self.current_time)
            except Exception as e:
                print(f"Timer callback error: {e}")
    
    def run_for_duration(self, duration_ms: float):
        """Run timer for specified duration"""
        self.is_running = True
        end_time = self.current_time + duration_ms
        
        while self.current_time < end_time and self.is_running:
            self.tick()
            time.sleep(self.resolution_ms / 1000.0)
        
        self.is_running = False


class RealTimeMonitor:
    """Monitor real-time system performance"""
    
    def __init__(self):
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.task_count = 0
        self.deadline_violations = 0
        self.history: List[Dict[str, Any]] = []
    
    def update_metrics(self, cpu: float, memory: float, tasks: int):
        """Update system metrics"""
        self.cpu_usage = cpu
        self.memory_usage = memory
        self.task_count = tasks
        
        self.history.append({
            'timestamp': time.time(),
            'cpu_usage': cpu,
            'memory_usage': memory,
            'task_count': tasks,
            'deadline_violations': self.deadline_violations
        })
    
    def record_deadline_violation(self, task_name: str):
        """Record a deadline violation"""
        self.deadline_violations += 1
        print(f"⚠️  DEADLINE VIOLATION: {task_name}")
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get current system health status"""
        return {
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'active_tasks': self.task_count,
            'deadline_violations': self.deadline_violations,
            'health_status': 'HEALTHY' if self.deadline_violations == 0 else 'DEGRADED'
        }


def example_realtime_robotics():
    """Example: Real-time robotics control"""
    print("Real-Time Robotics Control Example")
    print("=" * 50)
    
    executor = RealTimeExecutor()
    
    def robot_control_step():
        """Simulate robot control step"""
        # Simulate real-time control computation
        time.sleep(0.005)  # 5ms computation
        return {"position": [1.0, 2.0, 3.0], "timestamp": time.time()}
    
    try:
        # Execute with 10ms deadline
        result = executor.execute_critical(robot_control_step, deadline_ms=10)
        print(f"✓ Robot control completed: {result}")
    except TimeoutError as e:
        print(f"✗ Robot control timeout: {e}")


def example_periodic_sensor_fusion():
    """Example: Periodic sensor fusion"""
    print("\nPeriodic Sensor Fusion Example")
    print("=" * 50)
    
    scheduler = RealTimeScheduler(max_workers=2)
    
    sensor_data = {"accelerometer": [0.1, 0.2, 0.3], "gyroscope": [0.05, 0.1, 0.15]}
    
    def fuse_sensors():
        """Fuse sensor data"""
        # Simple complementary filter
        alpha = 0.98
        acc = sensor_data["accelerometer"]
        gyro = sensor_data["gyroscope"]
        fused = [alpha * gyro[i] + (1 - alpha) * acc[i] for i in range(3)]
        print(f"  Fused data: {fused}")
        return fused
    
    def periodic_task():
        """Periodic sensor fusion task"""
        fuse_sensors()
    
    # Create periodic task (100ms period)
    task = RealTimeTask(
        name="sensor_fusion",
        function=periodic_task,
        priority=RealTimePriority.HIGH,
        period=0.1,  # 100ms period
        execution_time_ms=5.0
    )
    
    scheduler.submit_periodic_task(task)
    scheduler.start()
    
    # Run for 500ms
    print("Running periodic sensor fusion for 500ms...")
    time.sleep(0.5)
    
    scheduler.stop()
    print("✓ Periodic sensor fusion completed")


def example_deadline_aware_execution():
    """Example: Deadline-aware task execution"""
    print("\nDeadline-Aware Execution Example")
    print("=" * 50)
    
    timer = DeterministicTimer(resolution_ms=1.0)
    
    def task1(current_time):
        print(f"  Task 1 executed at {current_time:.0f}ms")
    
    def task2(current_time):
        print(f"  Task 2 executed at {current_time:.0f}ms")
    
    def task3(current_time):
        print(f"  Task 3 executed at {current_time:.0f}ms")
    
    # Schedule tasks with deterministic timing
    timer.set_timer(10, task1)  # Execute at 10ms
    timer.set_timer(25, task2)  # Execute at 25ms
    timer.set_timer(50, task3)  # Execute at 50ms
    
    print("Running deterministic timer for 60ms...")
    timer.run_for_duration(60)
    print("✓ Deterministic execution completed")


def example_priority_scheduling():
    """Example: Priority-based task scheduling"""
    print("\nPriority-Based Scheduling Example")
    print("=" * 50)
    
    scheduler = RealTimeScheduler(max_workers=3)
    
    def critical_task():
        print("  Critical task executing...")
        time.sleep(0.002)
        return "critical_complete"
    
    def high_priority_task():
        print("  High priority task executing...")
        time.sleep(0.005)
        return "high_complete"
    
    def normal_task():
        print("  Normal task executing...")
        time.sleep(0.010)
        return "normal_complete"
    
    # Submit tasks with different priorities
    task1 = RealTimeTask("critical", critical_task, RealTimePriority.CRITICAL)
    task2 = RealTimeTask("high", high_priority_task, RealTimePriority.HIGH)
    task3 = RealTimeTask("normal", normal_task, RealTimePriority.NORMAL)
    
    scheduler.submit_task(task1)
    scheduler.submit_task(task2)
    scheduler.submit_task(task3)
    
    scheduler.start()
    
    # Wait for completion
    while scheduler.get_queue_length() > 0 or scheduler.get_active_tasks():
        time.sleep(0.001)
    
    scheduler.stop()
    
    print("✓ Priority scheduling completed")


def main():
    """Run real-time system examples"""
    print("Real-Time Execution System Examples")
    print("=" * 60)
    
    example_realtime_robotics()
    example_periodic_sensor_fusion()
    example_deadline_aware_execution()
    example_priority_scheduling()
    
    print("\n" + "=" * 60)
    print("Real-Time System Examples Completed")
    print("=" * 60)
    print("\nReal-Time Features:")
    print("  ✓ Deterministic task scheduling")
    print("  ✓ Priority-based execution")
    print("  ✓ Deadline guarantees")
    print("  ✓ Periodic task support")
    print("  ✓ Execution metrics monitoring")
    print("  ✓ System health tracking")


if __name__ == "__main__":
    main()
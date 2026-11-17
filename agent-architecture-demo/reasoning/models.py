"""
models.py
---------
Shared data structures and models for CoT, ToT, and ReAct reasoning frameworks.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional
from tools.travel_tools import ActionResult


class TaskStatus(str, Enum):
    """Enumeration of possible task states in the execution pipeline."""
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REPLANNED = "REPLANNED"


@dataclass
class TravelGoal:
    """Represents the parsed user travel goal and associated constraints."""
    raw_goal: str
    destination: str
    duration_days: int
    num_people: int
    budget_limit: float
    categories: List[str] = field(default_factory=lambda: [
        "transportation", "accommodation", "food", "sightseeing"
    ])

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Task:
    """Represents an atomic subtask within the execution plan."""
    task_id: str
    name: str
    action: str
    params: Dict[str, Any] = field(default_factory=dict)
    status: TaskStatus = TaskStatus.PENDING
    cost: float = 0.0
    result: Optional[ActionResult] = None
    is_replanned: bool = False
    original_task_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class ExecutionStep:
    """Represents a single step in the ReAct (Thought -> Action -> Observation) trace."""
    step_number: int
    thought: str
    action: str
    action_input: Dict[str, Any]
    observation: str
    status: str
    cost: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CandidatePlan:
    """
    Represents an alternative candidate plan generated and evaluated
    during the Tree-of-Thought (ToT) exploration phase.
    """
    plan_id: str                  # e.g., "Plan A", "Plan B", "Plan C"
    name: str                     # e.g., "Budget-Focused Travel", "Balanced Travel", etc.
    transport_choice: str
    accommodation_choice: str
    food_tier: str
    sightseeing_tier: str
    cost_breakdown: Dict[str, float]
    total_cost: float
    is_feasible: bool
    cost_efficiency_score: float
    experience_rating: float
    feasibility_score: float
    final_score: float
    description: str
    pros: List[str]
    cons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReasoningSummary:
    """User-facing structured reasoning summary produced during CoT decomposition."""
    goal_summary: str
    constraints: List[str]
    subtasks: List[Dict[str, str]]
    total_budget_limit: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TravelPlan:
    """Encapsulates the end-to-end plan, execution history, and final financial state."""
    goal: TravelGoal
    reasoning_summary: Optional[ReasoningSummary] = None
    candidate_plans: List[CandidatePlan] = field(default_factory=list)
    selected_candidate: Optional[CandidatePlan] = None
    initial_tasks: List[Task] = field(default_factory=list)
    current_tasks: List[Task] = field(default_factory=list)
    execution_trace: List[ExecutionStep] = field(default_factory=list)
    cost_breakdown: Dict[str, float] = field(default_factory=dict)
    total_cost: float = 0.0
    remaining_budget: float = 0.0
    is_approved: bool = False
    replanning_occurred: bool = False
    failed_task: Optional[Task] = None
    replanned_task: Optional[Task] = None
    replanning_reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal.to_dict(),
            "reasoning_summary": self.reasoning_summary.to_dict() if self.reasoning_summary else None,
            "selected_candidate": self.selected_candidate.to_dict() if self.selected_candidate else None,
            "cost_breakdown": self.cost_breakdown,
            "total_cost": self.total_cost,
            "remaining_budget": self.remaining_budget,
            "is_approved": self.is_approved,
            "replanning_occurred": self.replanning_occurred,
            "replanning_reason": self.replanning_reason,
            "execution_steps_count": len(self.execution_trace),
            "trace": [s.to_dict() for s in self.execution_trace]
        }


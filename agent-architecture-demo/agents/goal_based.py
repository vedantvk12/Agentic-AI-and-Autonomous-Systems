"""
goal_based.py
-------------
Architecture C: Goal-Based Agent

Operates using explicit goals and search/planning:
    Percept -> [Update State] -> [Goal Evaluation & Search/Planning] -> Action
Key Characteristics:
- Goal-Directed: Evaluates future states by whether they achieve an explicit objective.
- Goal Formulation: "Plan a 2-day Goa trip for 2 people within ₹10,000".
- Hierarchical Goal Decomposition:
    Goal -> Subgoal 1 (Transit) + Subgoal 2 (Lodging) + Subgoal 3 (Meals) + Subgoal 4 (Activities) + Subgoal 5 (Budget Verification).
- Selects actions systematically that bring the current world state closer to the goal state.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class GoalSpecification:
    """Explicit goal representation."""
    destination: str = "Goa"
    duration_days: int = 2
    num_people: int = 2
    budget_limit: float = 10000.0
    required_dimensions: List[str] = field(default_factory=lambda: [
        "transportation", "accommodation", "food", "sightseeing"
    ])


@dataclass
class GoalSubtask:
    """Subgoal within the goal-directed plan."""
    subgoal_id: str
    dimension: str
    target_action: str
    estimated_cost: float
    is_satisfied: bool = False
    chosen_option: Optional[str] = None


class GoalBasedAgent:
    """
    Demonstrates a Goal-Based Agent.
    Combines state evaluation with goal criteria to select an action sequence
    that transitions the environment into the defined goal state.
    """

    def __init__(self, goal: Optional[GoalSpecification] = None):
        self.architecture_name = "Goal-Based Agent"
        self.goal = goal or GoalSpecification()
        self.plan_subgoals: List[GoalSubtask] = []
        self.current_expenditure: float = 0.0

    def decompose_goal(self) -> List[GoalSubtask]:
        """
        Decomposes the high-level trip goal into structured, verifiable subgoals.
        """
        self.plan_subgoals = [
            GoalSubtask("SG-1", "transportation", "calculate_transport", 2000.0),
            GoalSubtask("SG-2", "accommodation", "search_accommodation", 2000.0),
            GoalSubtask("SG-3", "food", "estimate_food_cost", 3000.0),
            GoalSubtask("SG-4", "sightseeing", "select_sightseeing", 1200.0)
        ]
        return self.plan_subgoals

    def is_goal_achieved(self) -> bool:
        """
        Evaluates whether the agent has satisfied all criteria of the goal state:
        1. All dimensions satisfied.
        2. Total budget expenditure <= budget limit.
        """
        all_dimensions_met = all(sg.is_satisfied for sg in self.plan_subgoals)
        within_budget = self.current_expenditure <= self.goal.budget_limit
        return all_dimensions_met and within_budget

    def select_action_for_next_subgoal(self) -> Optional[Dict[str, Any]]:
        """
        Goal-directed action selection: identifies the first unsatisfied subgoal
        and emits the action required to transition towards goal achievement.
        """
        for sg in self.plan_subgoals:
            if not sg.is_satisfied:
                projected_total = self.current_expenditure + sg.estimated_cost
                if projected_total > self.goal.budget_limit:
                    return {
                        "action": "PRUNE_OR_REVISE_SUBGOAL",
                        "subgoal": sg.subgoal_id,
                        "reason": f"Projected total ₹{projected_total:,.0f} breaches goal budget ₹{self.goal.budget_limit:,.0f}."
                    }
                return {
                    "action": f"EXECUTE_{sg.target_action.upper()}",
                    "subgoal": sg.subgoal_id,
                    "dimension": sg.dimension,
                    "target_tool": sg.target_action,
                    "projected_cost": sg.estimated_cost,
                    "reason": f"Required to satisfy subgoal '{sg.dimension}' of the Goa travel goal."
                }
        return None

    def mark_subgoal_complete(self, subgoal_id: str, chosen_option: str, actual_cost: float) -> None:
        """Updates subgoal state and tracks budget progress toward goal."""
        for sg in self.plan_subgoals:
            if sg.subgoal_id == subgoal_id:
                sg.is_satisfied = True
                sg.chosen_option = chosen_option
                self.current_expenditure += actual_cost
                break

    def run_demonstration(self) -> Dict[str, Any]:
        """
        Runs an end-to-end demonstration of goal formulation, decomposition,
        step-by-step goal advancement, and goal-achievement verification.
        """
        self.decompose_goal()
        execution_log = []

        sample_execution_data = [
            ("SG-1", "Konkan Express AC Sleeper", 2000.0),
            ("SG-2", "Palm Breeze Budget Guesthouse", 2000.0),
            ("SG-3", "Local Beach Shacks & Thalis", 3000.0),
            ("SG-4", "North Goa Forts & Scooter Rental", 1200.0)
        ]

        for sg_id, option, cost in sample_execution_data:
            next_action = self.select_action_for_next_subgoal()
            self.mark_subgoal_complete(sg_id, option, cost)
            execution_log.append({
                "subgoal_advanced": sg_id,
                "action_selected": next_action["action"] if next_action else "DONE",
                "option_locked": option,
                "cost": cost,
                "cumulative_cost": self.current_expenditure,
                "remaining_budget": self.goal.budget_limit - self.current_expenditure
            })

        goal_achieved = self.is_goal_achieved()

        return {
            "agent_type": self.architecture_name,
            "goal_specification": {
                "destination": self.goal.destination,
                "duration_days": self.goal.duration_days,
                "num_people": self.goal.num_people,
                "budget_ceiling": self.goal.budget_limit
            },
            "subgoals_formulated": [
                {"id": sg.subgoal_id, "dimension": sg.dimension, "action": sg.target_action}
                for sg in self.plan_subgoals
            ],
            "execution_steps": execution_log,
            "final_status": {
                "total_cost": self.current_expenditure,
                "goal_achieved": goal_achieved,
                "savings": self.goal.budget_limit - self.current_expenditure
            },
            "key_distinction": (
                "Goal-based agents focus on WHETHER the objective is achieved. "
                "However, if multiple paths achieve the goal, it does not naturally quantify WHICH path is 'best' or 'most desirable' "
                "(that requires a Utility-Based Agent)."
            )
        }


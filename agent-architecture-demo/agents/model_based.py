"""
model_based.py
--------------
Architecture B: Model-Based Reflex Agent

Operates using internal state representation + transition model:
    Percept -> [Update State(Percept, Current State, How World Works)] -> [Condition-Action Rules with State] -> Action
Key Characteristics:
- State-Tracking: Maintains an internal model of the world (unobserved aspects).
- Tracks:
    * Total budget, spent budget, and remaining balance.
    * Hotel availability history and attempted reservations.
    * Completed subtasks (e.g., transport booked, hotel booked, etc.).
- Can handle partial observability and avoids circular re-executions.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class WorldState:
    """Internal representation of the travel planning environment."""
    total_budget: float = 10000.0
    spent_budget: float = 0.0
    remaining_budget: float = 10000.0
    completed_tasks: List[str] = field(default_factory=list)
    failed_attempts: List[Dict[str, Any]] = field(default_factory=list)
    confirmed_bookings: Dict[str, Any] = field(default_factory=dict)
    known_hotel_status: Dict[str, bool] = field(default_factory=dict)
    last_action: Optional[str] = None


class ModelBasedReflexAgent:
    """
    Demonstrates a Model-Based Reflex Agent.
    Maintains an explicit internal state of the environment to guide decisions
    even when aspects of the environment are partially observable or require historical context.
    """

    def __init__(self, initial_budget: float = 10000.0):
        self.architecture_name = "Model-Based Reflex Agent"
        self.state = WorldState(
            total_budget=initial_budget,
            remaining_budget=initial_budget
        )

    def update_internal_model(self, percept: Dict[str, Any]) -> None:
        """
        Updates the internal representation of the environment based on new percept
        and domain physics / transition rules.
        """
        percept_type = percept.get("type")

        if percept_type == "hotel_observation":
            hotel = percept.get("hotel_name")
            avail = percept.get("available", False)
            cost = percept.get("cost", 0.0)
            self.state.known_hotel_status[hotel] = avail

            if not avail:
                self.state.failed_attempts.append({
                    "component": "accommodation",
                    "target": hotel,
                    "reason": percept.get("reason", "Unavailable")
                })
            else:
                self.state.confirmed_bookings["accommodation"] = {
                    "hotel": hotel,
                    "cost": cost
                }
                self.state.spent_budget += cost
                self.state.remaining_budget = self.state.total_budget - self.state.spent_budget
                if "accommodation" not in self.state.completed_tasks:
                    self.state.completed_tasks.append("accommodation")

        elif percept_type == "transport_observation":
            cost = percept.get("cost", 0.0)
            mode = percept.get("mode", "train")
            self.state.confirmed_bookings["transportation"] = {
                "mode": mode,
                "cost": cost
            }
            self.state.spent_budget += cost
            self.state.remaining_budget = self.state.total_budget - self.state.spent_budget
            if "transportation" not in self.state.completed_tasks:
                self.state.completed_tasks.append("transportation")

    def decide_action(self, current_intent: str, candidate_options: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Selects next action using the internal state model.
        Crucially distinguishes between first-time booking and recovery after a known failure.
        """
        if current_intent == "book_hotel":
            # If transport is not completed yet, the internal state knows we need transport first
            if "transportation" not in self.state.completed_tasks:
                return {
                    "action": "DEFER_ACCOMMODATION",
                    "reason": "Internal model indicates transportation is not yet confirmed. Prerequisites unfulfilled.",
                    "state_summary": self.get_state_summary()
                }

            # Check candidate options against known state
            candidate_options = candidate_options or [
                {"name": "Sunset Beach Resort", "cost": 3000.0},
                {"name": "Palm Breeze Budget Guesthouse", "cost": 2000.0}
            ]

            for cand in candidate_options:
                h_name = cand["name"]
                h_cost = cand["cost"]

                # Has this hotel already failed in our internal model?
                if self.state.known_hotel_status.get(h_name) is False:
                    continue  # Skip known unavailable hotel based on internal state!

                # Does it fit within the remaining budget?
                if h_cost <= self.state.remaining_budget:
                    return {
                        "action": "ATTEMPT_HOTEL_BOOKING",
                        "selected_hotel": h_name,
                        "cost": h_cost,
                        "reason": f"Selected '{h_name}' (Cost: ₹{h_cost:,.0f}) which fits remaining budget ₹{self.state.remaining_budget:,.0f} and has not failed previously.",
                        "state_summary": self.get_state_summary()
                    }

            return {
                "action": "NO_FEASIBLE_HOTEL",
                "reason": "All available candidate hotels either previously failed or exceed the remaining budget.",
                "state_summary": self.get_state_summary()
            }

        return {
            "action": "PROCEED_NEXT",
            "state_summary": self.get_state_summary()
        }

    def get_state_summary(self) -> Dict[str, Any]:
        """Returns structured dictionary of internal model state."""
        return {
            "total_budget": self.state.total_budget,
            "spent_budget": self.state.spent_budget,
            "remaining_budget": self.state.remaining_budget,
            "completed_tasks": list(self.state.completed_tasks),
            "failed_attempts_count": len(self.state.failed_attempts),
            "known_hotel_status": dict(self.state.known_hotel_status)
        }

    def run_demonstration(self) -> Dict[str, Any]:
        """
        Executes a 2-step simulation demonstrating stateful decision-making:
        Step 1: Transport is booked -> updates internal state.
        Step 2: Tries Sunset Beach Resort -> observes failure -> updates model.
        Step 3: Queries decision engine -> internal state skips Sunset Beach Resort and picks Palm Breeze!
        """
        history = []

        # 1. Transport percept arrives
        p1 = {"type": "transport_observation", "mode": "Konkan Express (AC 3-Tier)", "cost": 2000.0}
        self.update_internal_model(p1)
        history.append({
            "step": 1,
            "event": "Transport Percept Received",
            "percept": p1,
            "state_after": self.get_state_summary()
        })

        # 2. Sunset Beach Resort tested & fails
        p2 = {"type": "hotel_observation", "hotel_name": "Sunset Beach Resort", "available": False, "reason": "Fully booked", "cost": 3000.0}
        self.update_internal_model(p2)
        history.append({
            "step": 2,
            "event": "Hotel Availability Failure Observed",
            "percept": p2,
            "state_after": self.get_state_summary()
        })

        # 3. Decision engine called
        decision = self.decide_action("book_hotel")
        history.append({
            "step": 3,
            "event": "Decision Engine Invocation",
            "decision": decision
        })

        return {
            "agent_type": self.architecture_name,
            "has_memory": True,
            "tracks_state": ["Budget balance", "Completed subtasks", "Known room availability history"],
            "simulation_steps": history,
            "key_advantage": (
                "Unlike the simple reflex agent, the model-based agent remembers that 'Sunset Beach Resort' is unavailable "
                "and that ₹2,000 was already spent on transport. It uses this internal state to pick 'Palm Breeze Budget Guesthouse' directly."
            )
        }


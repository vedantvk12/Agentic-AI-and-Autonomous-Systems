"""
simple_reflex.py
----------------
Architecture A: Simple Reflex Agent

Operates strictly on condition-action rules:
    Percept -> [Condition-Action Rules] -> Action
Key Characteristics:
- Stateless: Maintains zero internal historical memory of past percepts or actions.
- Operates only on current sensory input (percept).
- Vulnerable to infinite loops and partial observability.
- Sample Rule Demonstrated:
    IF (hotel == "Sunset Beach Resort" AND status == "UNAVAILABLE") -> REJECT_HOTEL
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ReflexPercept:
    """Represents current instantaneous sensory input to the reflex agent."""
    component: str           # e.g., 'hotel', 'transport', 'budget'
    target_name: str         # e.g., 'Sunset Beach Resort'
    observed_status: str     # e.g., 'AVAILABLE', 'UNAVAILABLE', 'EXCEEDED'
    cost: float = 0.0


@dataclass
class ReflexAction:
    """Action emitted by the simple reflex condition-action rule engine."""
    action_type: str
    target: str
    description: str
    rule_matched: str


class SimpleReflexAgent:
    """
    Demonstrates a classic Simple Reflex Agent.
    Evaluates current percept against a hard-coded condition-action table.
    Lacks internal memory or state representation.
    """

    def __init__(self):
        self.architecture_name = "Simple Reflex Agent"
        # Predefined Condition-Action Rules (Stimulus -> Response)
        self.rules = [
            {
                "condition": lambda p: p.component == "hotel" and p.observed_status == "UNAVAILABLE",
                "action": "REJECT_HOTEL",
                "rule_name": "RULE-01: If hotel is unavailable, reject hotel immediately",
                "desc": "Hotel booking rejected due to room unavailability percept."
            },
            {
                "condition": lambda p: p.component == "hotel" and p.observed_status == "AVAILABLE",
                "action": "BOOK_HOTEL",
                "rule_name": "RULE-02: If hotel is available, proceed with booking",
                "desc": "Hotel booking accepted."
            },
            {
                "condition": lambda p: p.component == "budget" and p.observed_status == "EXCEEDED",
                "action": "HALT_PLANNING",
                "rule_name": "RULE-03: If budget is exceeded, halt immediately",
                "desc": "Execution terminated because budget ceiling was breached."
            },
            {
                "condition": lambda p: p.component == "transport" and p.observed_status == "AVAILABLE",
                "action": "RESERVE_TRANSPORT",
                "rule_name": "RULE-04: If transport is available, reserve seats",
                "desc": "Transportation booked."
            }
        ]

    def perceive_and_act(self, percept: ReflexPercept) -> ReflexAction:
        """
        Receives an instantaneous percept, matches condition-action rules,
        and returns an action without consulting or updating any internal state.
        """
        for r in self.rules:
            if r["condition"](percept):
                return ReflexAction(
                    action_type=r["action"],
                    target=percept.target_name,
                    description=r["desc"],
                    rule_matched=r["rule_name"]
                )
        
        return ReflexAction(
            action_type="DEFAULT_NOOP",
            target=percept.target_name,
            description="No condition-action rule matched current percept.",
            rule_matched="NONE"
        )

    def run_demonstration(self, hotel_name: str = "Sunset Beach Resort", is_available: bool = False) -> Dict[str, Any]:
        """
        Runs a standardized demonstration of the Simple Reflex Agent handling hotel availability.
        """
        status_str = "AVAILABLE" if is_available else "UNAVAILABLE"
        percept = ReflexPercept(
            component="hotel",
            target_name=hotel_name,
            observed_status=status_str,
            cost=3000.0 if is_available else 0.0
        )
        action = self.perceive_and_act(percept)

        return {
            "agent_type": self.architecture_name,
            "has_memory": False,
            "internal_state": "None (Stateless - strictly stimulus-response)",
            "percept_received": {
                "component": percept.component,
                "target": percept.target_name,
                "status": percept.observed_status
            },
            "rule_fired": action.rule_matched,
            "action_emitted": action.action_type,
            "outcome_description": action.description,
            "behavioral_limitation": (
                "Cannot formulate a recovery plan or remember previous attempts because it has no internal state. "
                "If prompted again with the same hotel, it will blindly repeat the exact same rejection."
            )
        }


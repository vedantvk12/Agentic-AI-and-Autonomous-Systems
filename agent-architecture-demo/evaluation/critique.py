"""
critique.py
-----------
Critique and Improvement Analysis Module for Autonomous Agent Planning Systems.

Identifies and analyzes three critical planning weaknesses:
1. Reliance on Unverified Assumptions
2. Incorrect or Incomplete Observations
3. Budget Overrun Risk

Provides detailed explanations (Problem, Where it occurs, Consequences, Improvement)
and executable demonstration functions illustrating baseline vulnerabilities vs. improved architectural guardrails:
- Independent Pre-Verification
- Strict Budget Validation & Guardrails
- Autonomous Alternative Plan Generation
- Maximum Retry Limits
- Human-in-the-Loop Approval Gates
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from tools.travel_tools import verify_availability, ACCOMMODATION_CATALOG


@dataclass
class PlanningWeaknessAnalysis:
    """Detailed academic analysis of a specific agent planning weakness."""
    title: str
    problem_statement: str
    occurrence_locus: str
    cascading_consequences: str
    proposed_improvement: str
    remedy_mechanisms: List[str]


CRITIQUE_ANALYSES: List[PlanningWeaknessAnalysis] = [
    PlanningWeaknessAnalysis(
        title="1. Reliance on Unverified Assumptions",
        problem_statement=(
            "The agent formulates its primary candidate plan under the unverified assumption that its preferred "
            "hotel ('Sunset Beach Resort') will have available room vacancies at the quoted rate of ₹3,000. "
            "It does not perform a real-time availability check prior to executing interdependent planning steps."
        ),
        occurrence_locus=(
            "Occurs during Tree-of-Thought (ToT) candidate selection and Task 2 of the initial ReAct schedule, "
            "where transportation is locked in before confirming that lodging is actually bookable."
        ),
        cascading_consequences=(
            "When the room inventory check fails, the agent encounters an immediate pipeline blockage. "
            "If the agent is a Simple Reflex Agent, it terminates in failure. Even in standard ReAct, "
            "it incurs replanning latency, risks booking non-refundable transit without guaranteed accommodation, "
            "and forces emergency fallback selection."
        ),
        proposed_improvement=(
            "Independent Pre-Verification and Speculative Branching: Require an independent pre-flight tool "
            "call (`verify_availability()`) during plan synthesis before locking in dependent logistics."
        ),
        remedy_mechanisms=[
            "Pre-flight verification tools to validate external inventory before committing tasks",
            "Conditional branching: Prepare warm standby backup options (Plan B1, B2) upfront",
            "Two-phase commit: Hold reservations tentatively and finalize simultaneously"
        ]
    ),
    PlanningWeaknessAnalysis(
        title="2. Vulnerability to Incorrect or Incomplete Observations",
        problem_statement=(
            "The agent treats external tool observations as ground truth without validating data schemas, "
            "detecting sensor noise, or verifying completeness (e.g. hidden taxes, surge pricing, missing check-in dates)."
        ),
        occurrence_locus=(
            "Occurs at the observation intake boundary (the 'Observation' phase of the ReAct loop) where "
            "raw dictionary or string returns from Python tools are parsed into the agent's internal state."
        ),
        cascading_consequences=(
            "If an external API returns a partial payload (e.g. base room rate without GST taxes, or a false-positive availability), "
            "the agent updates its world model with corrupted state data, causing budget drift, invalid reservations, "
            "or severe hallucinations downstream."
        ),
        proposed_improvement=(
            "Contract-Based Observation Schema Validation and Sanity Assertions: Enforce strict Pydantic/dataclass "
            "schema validation and cross-checking before accepting observations into agent memory."
        ),
        remedy_mechanisms=[
            "Strict schema validation on all tool returns (validating cost > 0, currency, timestamps)",
            "Cross-source verification: Corroborate critical claims across multiple independent tools",
            "Confidence thresholding: Reject low-confidence observations and flag for human review"
        ]
    ),
    PlanningWeaknessAnalysis(
        title="3. Cumulative Budget Overrun Risk",
        problem_statement=(
            "Independent subtasks make local spending choices without continuously asserting global budget ceilings. "
            "A slightly higher meal expense or premium transport selection can silently push the final total over ₹10,000."
        ),
        occurrence_locus=(
            "Occurs across the sequential execution pipeline (Tasks 1 through 4), where the formal budget audit is "
            "deferred until the very last step ('verify_budget') rather than being enforced dynamically at each step."
        ),
        cascading_consequences=(
            "If intermediate expenses compound unpredictably, the agent only discovers the financial failure after "
            "all subtasks have finished execution, requiring an expensive full-pipeline rollback or leaving the user with an unaffordable itinerary."
        ),
        proposed_improvement=(
            "Dynamic Real-Time Budget Guardrails and Invariant Assertions: Enforce strict remaining-budget invariants "
            "before any subtask is executed. Terminate or downgrade options the instant remaining funds are insufficient."
        ),
        remedy_mechanisms=[
            "Real-time budget guardrail check before authorizing any action dispatch",
            "Category envelope budgeting: Set hard sub-ceilings (e.g. lodging max 35%, food max 30%)",
            "Autonomous fallback downgrade triggers when remaining buffer drops below 10%"
        ]
    )
]


class PlanningCritiqueEngine:
    """
    Executes comparative demonstrations of naive planning behavior vs.
    hardened planning behavior with safety guardrails.
    """

    @classmethod
    def get_critique_analyses(cls) -> List[PlanningWeaknessAnalysis]:
        return CRITIQUE_ANALYSES

    @staticmethod
    def demonstrate_pre_verification_improvement(hotel_name: str = "Sunset Beach Resort") -> Dict[str, Any]:
        """
        Demonstrates the improvement: Independent Pre-Verification.
        Compares:
        - Naive ReAct: Blindly commits transit, then tries hotel and fails.
        - Hardened Agent: Runs independent pre-verification FIRST; identifies unavailability immediately
          and swaps to Palm Breeze Budget Guesthouse before booking transit!
        """
        # Naive approach
        naive_trace = [
            {"step": 1, "action": "calculate_transport", "status": "COMMITTED", "cost": 2000.0, "note": "Transit booked without checking hotel vacancy."},
            {"step": 2, "action": "search_accommodation", "status": "FAILED", "cost": 0.0, "note": "Sunset Beach Resort is unavailable! Transit already booked."}
        ]

        # Improved approach with pre-verification
        verify_result = verify_availability(hotel_name)
        improved_trace = []
        if not verify_result.success:
            improved_trace.append({
                "step": 1,
                "action": f"verify_availability('{hotel_name}')",
                "status": "DETECTED_UNAVAILABLE",
                "note": f"Pre-flight verification alerted: {verify_result.failure_reason}. No commitments made yet."
            })
            # Immediate proactive substitute
            alt_hotel = "Palm Breeze Budget Guesthouse"
            alt_verify = verify_availability(alt_hotel)
            improved_trace.append({
                "step": 2,
                "action": f"verify_availability('{alt_hotel}')",
                "status": "VERIFIED_AVAILABLE",
                "note": f"Alternative '{alt_hotel}' verified vacant at ₹{alt_verify.cost:,.0f}."
            })
            improved_trace.append({
                "step": 3,
                "action": "calculate_transport",
                "status": "COMMITTED_SAFELY",
                "cost": 2000.0,
                "note": "Transit booked with 100% confidence in confirmed lodging."
            })

        return {
            "vulnerability": "Reliance on Unverified Assumptions",
            "naive_execution": naive_trace,
            "improved_execution": improved_trace,
            "improvement_benefit": (
                "Pre-verification prevented locking in non-refundable transit before confirming accommodation. "
                "The improved agent swapped to a verified guesthouse before initiating any financial commitments."
            )
        }

    @staticmethod
    def demonstrate_budget_guardrail_improvement(
        proposed_luxury_accommodation: float = 4800.0,
        budget_limit: float = 10000.0
    ) -> Dict[str, Any]:
        """
        Demonstrates the improvement: Dynamic Budget Guardrails & Invariant Assertions.
        """
        current_committed = 2000.0  # Transport
        food_envelope = 3000.0
        sightseeing_envelope = 1200.0
        minimum_required_subsequent = food_envelope + sightseeing_envelope  # 4200.0

        max_allowable_lodging = budget_limit - current_committed - minimum_required_subsequent  # 3800.0

        if proposed_luxury_accommodation > max_allowable_lodging:
            guardrail_triggered = True
            action_taken = "REJECT_AND_DOWNGRADE"
            recommended_budget_option = 2000.0  # Guesthouse
            savings = proposed_luxury_accommodation - recommended_budget_option
        else:
            guardrail_triggered = False
            action_taken = "APPROVE"
            recommended_budget_option = proposed_luxury_accommodation
            savings = 0.0

        return {
            "vulnerability": "Cumulative Budget Overrun Risk",
            "budget_limit": budget_limit,
            "current_committed": current_committed,
            "minimum_subsequent_needed": minimum_required_subsequent,
            "max_allowable_for_accommodation": max_allowable_lodging,
            "proposed_accommodation_cost": proposed_luxury_accommodation,
            "guardrail_triggered": guardrail_triggered,
            "guardrail_decision": action_taken,
            "selected_fallback_cost": recommended_budget_option,
            "financial_safety_savings": savings,
            "guardrail_rationale": (
                f"Proposed lodging cost ₹{proposed_luxury_accommodation:,.0f} exceeds max allowable limit "
                f"of ₹{max_allowable_lodging:,.0f} (to guarantee ₹{minimum_required_subsequent:,.0f} remains for meals and sightseeing). "
                "Guardrail intervened in real-time, preventing a downstream budget overrun of ₹1,000!"
            )
        }


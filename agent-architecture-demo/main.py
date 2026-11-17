"""
main.py
-------
Command-line Execution Runner for the Agent Architecture Comparison and ReAct-Based Reasoning Demonstrator.

Executes all core components:
1. Five Agent Architecture Demonstrations (Simple Reflex, Model-Based, Goal-Based, Utility-Based, Learning)
2. Chain-of-Thought (CoT) Goal Decomposition
3. Tree-of-Thought (ToT) Multi-Branch Alternative Exploration & Scoring
4. Live ReAct Execution Loop with Controlled Failure & Autonomous Dynamic Replanning
5. Critique and Improvement Demonstrations (Pre-Verification and Budget Guardrails)
6. Serializes authentic execution traces and evaluation metrics into outputs/

Student: Vedant Sattejkumar Kirange (Roll No: 55, PRN: ADT23SOCB1294)
MIT ADT University - Units I & II: CO I & CO II
"""

import os
import sys
import json

# Ensure UTF-8 output encoding for console in Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure local directories are in Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from agents import (
    SimpleReflexAgent,
    ModelBasedReflexAgent,
    GoalBasedAgent,
    UtilityBasedAgent,
    LearningAgent
)
from reasoning import (
    ChainOfThoughtPlanner,
    TreeOfThoughtPlanner,
    ReActAgent,
    TravelGoal
)
from evaluation import (
    AgentArchitectureComparator,
    PlanningCritiqueEngine,
    DebateContentManager
)


def run_all_demonstrations():
    print("=" * 80)
    print("MIT ADT UNIVERSITY - UNITS I & II: AGENTIC AI & AUTONOMOUS SYSTEMS")
    print("Agent Architecture Comparison and ReAct-Based Reasoning Demonstrator")
    print("Student: Vedant Sattejkumar Kirange | Roll No: 55 | PRN: ADT23SOCB1294")
    print("=" * 80)
    print("")

    # =========================================================================
    # PART 1: FIVE AGENT ARCHITECTURES DEMONSTRATION
    # =========================================================================
    print("[+] PART 1: DEMONSTRATING FIVE AGENT ARCHITECTURES...")
    
    # 1. Simple Reflex Agent
    print("\n  --- A. Simple Reflex Agent ---")
    sra = SimpleReflexAgent()
    sra_demo = sra.run_demonstration(hotel_name="Sunset Beach Resort", is_available=False)
    print(f"  • Agent: {sra_demo['agent_type']}")
    print(f"  • Percept Received: {sra_demo['percept_received']}")
    print(f"  • Rule Fired: {sra_demo['rule_fired']}")
    print(f"  • Action: {sra_demo['action_emitted']}")
    print(f"  • Limitation: {sra_demo['behavioral_limitation']}")

    # 2. Model-Based Reflex Agent
    print("\n  --- B. Model-Based Reflex Agent ---")
    mba = ModelBasedReflexAgent(initial_budget=10000.0)
    mba_demo = mba.run_demonstration()
    print(f"  • Agent: {mba_demo['agent_type']}")
    print(f"  • State Tracked: {mba_demo['tracks_state']}")
    print(f"  • Advantage: {mba_demo['key_advantage']}")

    # 3. Goal-Based Agent
    print("\n  --- C. Goal-Based Agent ---")
    gba = GoalBasedAgent()
    gba_demo = gba.run_demonstration()
    print(f"  • Agent: {gba_demo['agent_type']}")
    print(f"  • Goal Target: {gba_demo['goal_specification']['destination']} trip within ₹{gba_demo['goal_specification']['budget_ceiling']:,.0f}")
    print(f"  • Subgoals Generated: {len(gba_demo['subgoals_formulated'])}")
    print(f"  • Final Achieved Status: Goal Achieved = {gba_demo['final_status']['goal_achieved']}")

    # 4. Utility-Based Agent
    print("\n  --- D. Utility-Based Agent ---")
    uba = UtilityBasedAgent(budget_limit=10000.0)
    uba_demo = uba.run_demonstration()
    print(f"  • Agent: {uba_demo['agent_type']}")
    print(f"  • Selected Optimal Plan: {uba_demo['selected_optimal_plan']['plan_id']} ({uba_demo['selected_optimal_plan']['plan_name']})")
    print(f"  • Utility Score: {uba_demo['selected_optimal_plan']['final_utility_score']} / 100")
    print(f"  • Selection Rationale: {uba_demo['selection_rationale']}")

    # 5. Learning Agent
    print("\n  --- E. Learning Agent ---")
    la = LearningAgent()
    la_demo = la.run_demonstration()
    print(f"  • Agent: {la_demo['agent_type']}")
    print(f"  • Episode 1 (Untrained): Selected {la_demo['episodes'][0]['hotel_chosen']} -> {la_demo['episodes'][0]['environment_observation']}")
    print(f"  • Episode 2 (Trained): Selected {la_demo['episodes'][1]['hotel_chosen']} -> {la_demo['episodes'][1]['environment_observation']}")
    print(f"  • Takeaway: {la_demo['core_takeaway']}")

    # =========================================================================
    # PART 2: CoT & ToT REASONING FRAMEWORKS
    # =========================================================================
    print("\n" + "=" * 80)
    print("[+] PART 2: CHAIN-OF-THOUGHT (CoT) & TREE-OF-THOUGHT (ToT)...")
    
    shared_goal_text = "Plan a 2-day Goa trip for 2 people within ₹10,000, including transportation, accommodation, food and sightseeing."
    parsed_goal = ChainOfThoughtPlanner.parse_goal(shared_goal_text)
    cot_summary = ChainOfThoughtPlanner.decompose_goal(parsed_goal)

    print(f"\n  • Parsed Goal: Destination={parsed_goal.destination}, Days={parsed_goal.duration_days}, People={parsed_goal.num_people}, Budget=₹{parsed_goal.budget_limit:,.0f}")
    print(f"  • CoT Subtasks ({len(cot_summary.subtasks)} tasks generated):")
    for st in cot_summary.subtasks:
        print(f"    - Step {st['step']}: {st['task_name']} ({st['tool_action']}) -> {st['dependency']}")

    # Tree-of-Thought (ToT) exploration
    candidate_plans = TreeOfThoughtPlanner.generate_candidate_plans(parsed_goal)
    best_candidate, tot_justification = TreeOfThoughtPlanner.select_best_candidate(candidate_plans)

    print(f"\n  • ToT Candidate Exploration ({len(candidate_plans)} branches):")
    for c in candidate_plans:
        status_flag = "[FEASIBLE]" if c.is_feasible else "[INFEASIBLE]"
        print(f"    - {c.plan_id}: {c.name:28s} | Cost: ₹{c.total_cost:,.0f} {status_flag} | Score: {c.final_score:.2f}")

    print(f"\n  • Winning ToT Plan Selected: {best_candidate.plan_id} ({best_candidate.name})")

    # =========================================================================
    # PART 3: LIVE REACT DEMONSTRATION WITH CONTROLLED FAILURE
    # =========================================================================
    print("\n" + "=" * 80)
    print("[+] PART 3: LIVE REACT EXECUTION LOOP (THOUGHT -> ACTION -> OBSERVATION)...")
    
    react_agent = ReActAgent(
        goal=parsed_goal,
        selected_candidate=best_candidate,
        reasoning_summary=cot_summary,
        candidate_plans=candidate_plans
    )
    executed_plan = react_agent.run()
    trace_text = react_agent.get_formatted_trace()

    print(f"\n  • Total ReAct Steps Executed: {len(executed_plan.execution_trace)}")
    print(f"  • Controlled Failure Intercepted: Replanning Occurred = {executed_plan.replanning_occurred}")
    print(f"  • Replanning Details: {executed_plan.replanning_reason}")
    print(f"  • Final Budget Total: ₹{executed_plan.total_cost:,.0f} (Remaining Buffer: ₹{executed_plan.remaining_budget:,.0f})")
    print(f"  • Plan Financial Feasibility Approval: {executed_plan.is_approved}")

    # =========================================================================
    # PART 4: CRITIQUE & IMPROVEMENTS DEMONSTRATION
    # =========================================================================
    print("\n" + "=" * 80)
    print("[+] PART 4: PLANNING CRITIQUE & IMPROVEMENT DEMONSTRATIONS...")
    
    pre_verify_demo = PlanningCritiqueEngine.demonstrate_pre_verification_improvement()
    guardrail_demo = PlanningCritiqueEngine.demonstrate_budget_guardrail_improvement(proposed_luxury_accommodation=4800.0)

    print(f"\n  • Improvement 1 (Independent Pre-Verification): {pre_verify_demo['improvement_benefit']}")
    print(f"  • Improvement 2 (Dynamic Budget Guardrail): {guardrail_demo['guardrail_rationale']}")

    # =========================================================================
    # PART 5: SERIALIZE OUTPUTS
    # =========================================================================
    outputs_dir = os.path.join(current_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)

    trace_file = os.path.join(outputs_dir, "execution_trace.txt")
    with open(trace_file, "w", encoding="utf-8") as f:
        f.write(trace_text)
    print(f"\n[+] Saved live execution trace to: {trace_file}")

    candidates_file = os.path.join(outputs_dir, "candidate_plans.json")
    with open(candidates_file, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in candidate_plans], f, indent=2)
    print(f"[+] Saved candidate plans to: {candidates_file}")

    eval_results = {
        "student_details": {
            "name": "Vedant Sattejkumar Kirange",
            "roll_no": 55,
            "prn": "ADT23SOCB1294",
            "university": "MIT ADT University",
            "activity": "Group Debate and Live Demonstration – Agent Architectures and ReAct-Based Reasoning in Practice",
            "mapped_cos": ["CO I", "CO II"]
        },
        "agent_architecture_comparison": AgentArchitectureComparator.get_comparison_table(),
        "architectures_demonstrations": {
            "simple_reflex": sra_demo,
            "model_based": mba_demo,
            "goal_based": gba_demo,
            "utility_based": uba_demo,
            "learning_agent": la_demo
        },
        "cot_summary": cot_summary.to_dict(),
        "selected_plan": best_candidate.to_dict(),
        "executed_final_plan": executed_plan.to_dict(),
        "critique_improvements": {
            "pre_verification": pre_verify_demo,
            "budget_guardrail": guardrail_demo
        }
    }

    eval_file = os.path.join(outputs_dir, "evaluation_results.json")
    with open(eval_file, "w", encoding="utf-8") as f:
        json.dump(eval_results, f, indent=2)
    print(f"[+] Saved evaluation results to: {eval_file}")

    print("\n" + "=" * 80)
    print("[SUCCESS] All agent architectures, reasoning loops, and live ReAct tests passed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    run_all_demonstrations()

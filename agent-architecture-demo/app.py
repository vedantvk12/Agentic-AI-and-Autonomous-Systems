"""
app.py
------
Interactive Streamlit Academic Demonstration System.
MIT ADT University - Units I & II: Introduction to Agentic AI and Autonomous Systems;
Reasoning, Planning and Decision-Making (CO I & CO II).

Activity: Group Debate and Live Demonstration – Agent Architectures and ReAct-Based Reasoning in Practice.
Student: Vedant Sattejkumar Kirange | Roll No: 55 | PRN: ADT23SOCB1294

Includes 5 Dedicated Interactive Tabs:
1. Agent Architectures (5 Agents comparison & live scenario simulator)
2. CoT and ToT (Goal decomposition, 3 candidate plans, dynamic multi-attribute scoring)
3. ReAct Live Demo (Interactive execution loop, controlled failure, dynamic replanning trace)
4. Critique & Improvement (Failure root cause, before/after comparison, architectural guardrails)
5. Group Debate (10 Debate topics with balanced arguments, model answers, and student group note recorder)
"""

import os
import sys
import json
import streamlit as st
import pandas as pd

# Path setup
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

# Page configuration
st.set_page_config(
    page_title="Agent Architectures & ReAct Reasoning | MIT ADT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (MIT ADT Navy & Technical Theme)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1B365D 0%, #0969DA 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 10px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        color: white !important;
        font-size: 26px;
        margin-bottom: 6px;
        font-weight: 700;
    }
    .main-header p {
        color: #EBF3FA !important;
        font-size: 14px;
        margin: 0;
    }
    .student-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 13px;
        margin-top: 8px;
        font-weight: 500;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .trace-step-success {
        border-left: 5px solid #1A7F37;
        background-color: #F6FFF8;
        padding: 12px 18px;
        margin-bottom: 12px;
        border-radius: 4px;
    }
    .trace-step-failure {
        border-left: 5px solid #CF222E;
        background-color: #FFF5F5;
        padding: 12px 18px;
        margin-bottom: 12px;
        border-radius: 4px;
    }
    .trace-step-replan {
        border-left: 5px solid #BF8700;
        background-color: #FFFDF5;
        padding: 12px 18px;
        margin-bottom: 12px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Main Banner Header
st.markdown("""
<div class="main-header">
    <h1>Agent Architecture Comparison & ReAct-Based Reasoning Demonstrator</h1>
    <p>Units I & II: Introduction to Agentic AI and Autonomous Systems; Reasoning, Planning and Decision-Making (CO I & CO II)</p>
    <div class="student-badge">
        👨‍🎓 <b>Student:</b> Vedant Sattejkumar Kirange &nbsp;|&nbsp;
        <b>Roll No:</b> 55 &nbsp;|&nbsp;
        <b>PRN:</b> ADT23SOCB1294 &nbsp;|&nbsp;
        <b>University:</b> MIT ADT University
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Information & Navigation Controls
with st.sidebar:
    st.subheader("🎯 Academic Context")
    st.info(
        "**Activity Name:** Group Debate and Live Demonstration – Agent Architectures and ReAct-Based Reasoning in Practice\n\n"
        "**Mapped Outcomes:**\n"
        "- **CO I:** Understand and evaluate autonomous agent architectures.\n"
        "- **CO II:** Design, analyze, and inspect reasoning frameworks (CoT, ToT, ReAct)."
    )

    st.subheader("📋 Shared Travel Goal")
    st.markdown(
        "> *'Plan a 2-day Goa trip for 2 people within ₹10,000, including transportation, accommodation, food and sightseeing.'*"
    )

    st.divider()
    st.caption("Developed for MIT ADT University Academic Submission.")

# Define 5 Tabs
tabs = st.tabs([
    "🏛️ Tab 1: Agent Architectures",
    "🌳 Tab 2: CoT & ToT Reasoning",
    "⚡ Tab 3: ReAct Live Demo",
    "🔍 Tab 4: Critique & Improvement",
    "🗣️ Tab 5: Group Debate"
])

# =============================================================================
# TAB 1: AGENT ARCHITECTURES
# =============================================================================
with tabs[0]:
    st.header("Comparative Analysis of Five Agent Architectures")
    st.markdown(
        "Evaluate how distinct internal agent structures (from stateless condition-action reflex systems to adaptive learning agents) "
        "handle decision-making, state tracking, and failure events in travel planning."
    )

    st.subheader("📊 Architectural Comparison Matrix")
    df_comparison = pd.DataFrame(AgentArchitectureComparator.get_comparison_table())
    df_display = df_comparison.rename(columns={
        "agent_type": "Agent Architecture",
        "internal_architecture": "Internal Structure",
        "decision_making_method": "Decision Method",
        "advantages": "Key Advantages",
        "limitations": "Critical Limitations",
        "suitable_applications": "Real-World Applications"
    })
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("🎮 Interactive Agent Simulator")
    st.markdown("Select an agent architecture and test its behavioral response to a live environmental percept.")

    c1, c2 = st.columns([1, 2])
    with c1:
        selected_agent = st.selectbox(
            "Select Agent Architecture to Test:",
            [
                "A. Simple Reflex Agent",
                "B. Model-Based Reflex Agent",
                "C. Goal-Based Agent",
                "D. Utility-Based Agent",
                "E. Learning Agent"
            ]
        )

        hotel_available_input = st.toggle("Simulate Hotel Available", value=False)
        user_budget_input = st.number_input("Budget Ceiling (₹)", value=10000, step=1000)

        run_sim = st.button("Run Architecture Simulation", type="primary", use_container_width=True)

    with c2:
        if run_sim or "sim_result" not in st.session_state:
            if "Simple Reflex" in selected_agent:
                agent = SimpleReflexAgent()
                res = agent.run_demonstration(is_available=hotel_available_input)
                st.session_state["sim_result"] = {
                    "type": "Simple Reflex Agent",
                    "state": res["internal_state"],
                    "rule": res["rule_fired"],
                    "action": res["action_emitted"],
                    "desc": res["outcome_description"],
                    "limitation": res["behavioral_limitation"]
                }
            elif "Model-Based" in selected_agent:
                agent = ModelBasedReflexAgent(initial_budget=user_budget_input)
                res = agent.run_demonstration()
                st.session_state["sim_result"] = {
                    "type": "Model-Based Reflex Agent",
                    "state": f"Tracks: {res['tracks_state']}",
                    "steps": res["simulation_steps"],
                    "advantage": res["key_advantage"]
                }
            elif "Goal-Based" in selected_agent:
                agent = GoalBasedAgent()
                agent.goal.budget_limit = user_budget_input
                res = agent.run_demonstration()
                st.session_state["sim_result"] = {
                    "type": "Goal-Based Agent",
                    "goal": f"Target: {res['goal_specification']['destination']} trip within ₹{res['goal_specification']['budget_ceiling']:,.0f}",
                    "subgoals": res["subgoals_formulated"],
                    "steps": res["execution_steps"],
                    "achieved": res["final_status"]["goal_achieved"],
                    "note": res["key_distinction"]
                }
            elif "Utility-Based" in selected_agent:
                agent = UtilityBasedAgent(budget_limit=user_budget_input)
                res = agent.run_demonstration()
                st.session_state["sim_result"] = {
                    "type": "Utility-Based Agent",
                    "best": res["selected_optimal_plan"],
                    "rationale": res["selection_rationale"],
                    "all": res["all_evaluated_plans"]
                }
            elif "Learning Agent" in selected_agent:
                agent = LearningAgent()
                res = agent.run_demonstration()
                st.session_state["sim_result"] = {
                    "type": "Learning Agent",
                    "components": res["learning_components"],
                    "episodes": res["episodes"],
                    "kb": res["knowledge_base_state"],
                    "takeaway": res["core_takeaway"]
                }

        # Render Simulation Output
        sim = st.session_state.get("sim_result", {})
        st.markdown(f"### Results for **{sim.get('type', '')}**")

        if sim.get("type") == "Simple Reflex Agent":
            st.error(f"**Action Fired:** `{sim.get('action')}`")
            st.write(f"**Matched Rule:** {sim.get('rule')}")
            st.write(f"**Internal State:** {sim.get('state')}")
            st.warning(f"**Limitation:** {sim.get('limitation')}")

        elif sim.get("type") == "Model-Based Reflex Agent":
            st.success(f"**State Tracked:** {sim.get('state')}")
            st.write(f"**Key Advantage:** {sim.get('advantage')}")
            for step in sim.get("steps", []):
                st.markdown(f"- **Step {step.get('step')}:** {step.get('event')}")

        elif sim.get("type") == "Goal-Based Agent":
            st.info(f"**Goal Formulation:** {sim.get('goal')}")
            st.write(f"**Final Goal Achieved:** `{sim.get('achieved')}`")
            st.caption(f"**Pedagogical Note:** {sim.get('note')}")

        elif sim.get("type") == "Utility-Based Agent":
            best = sim.get("best", {})
            st.success(f"**Winning Plan:** {best.get('plan_name')} (Score: {best.get('final_utility_score')}/100)")
            st.write(f"**Selection Rationale:** {sim.get('rationale')}")
            st.caption(f"Evaluated across Cost Efficiency, Accommodation Comfort, and Activity Experience.")

        elif sim.get("type") == "Learning Agent":
            st.success("2-Episode Learning Simulation Complete:")
            for ep in sim.get("episodes", []):
                st.markdown(
                    f"- **Episode {ep['episode']} ({ep['state_of_knowledge']}):** "
                    f"Selected `{ep['hotel_chosen']}` → Result: `{ep['environment_observation']}` (Reward: {ep['critic_reward']}). "
                    f"*{ep['adaptation_note']}*"
                )
            st.info(f"**Takeaway:** {sim.get('takeaway')}")

# =============================================================================
# TAB 2: CoT AND ToT REASONING
# =============================================================================
with tabs[1]:
    st.header("Reasoning Frameworks: Chain-of-Thought & Tree-of-Thought")
    st.markdown(
        "Inspect how Chain-of-Thought (CoT) structures task decomposition and dependencies, while "
        "Tree-of-Thought (ToT) explores multiple candidate travel branches and scores trade-offs."
    )

    goal_text = "Plan a 2-day Goa trip for 2 people within ₹10,000, including transportation, accommodation, food and sightseeing."
    parsed_goal = ChainOfThoughtPlanner.parse_goal(goal_text)
    cot_summary = ChainOfThoughtPlanner.decompose_goal(parsed_goal)

    c1, c2 = st.columns([1, 1])

    with c1:
        st.subheader("🔗 Chain-of-Thought (CoT) Decomposition")
        st.write(f"**User Goal:** {parsed_goal.raw_goal}")
        st.write(f"**Constraints Identified:**")
        for c in cot_summary.constraints:
            st.markdown(f"- {c}")

        st.markdown("#### Ordered Subtask Pipeline")
        for st_item in cot_summary.subtasks:
            with st.expander(f"Step {st_item['step']}: {st_item['task_name']} (`{st_item['tool_action']}`)", expanded=(st_item['step'] in ["1", "2"])):
                st.write(f"**Prerequisite Dependency:** {st_item['dependency']}")
                st.write(f"**Academic Justification:** {st_item['justification']}")

    with c2:
        st.subheader("🌳 Tree-of-Thought (ToT) Candidate Exploration")
        st.markdown("Dynamic Multi-Attribute Evaluation across 3 distinct travel branches:")

        # Sliders for interactive utility weights
        st.markdown("**Tune Preference Weights:**")
        w_cols = st.columns(3)
        with w_cols[0]:
            w_cost = st.slider("Cost Efficiency", 0.0, 1.0, 0.30, 0.05)
        with w_cols[1]:
            w_exp = st.slider("Experience Quality", 0.0, 1.0, 0.50, 0.05)
        with w_cols[2]:
            w_feas = st.slider("Feasibility", 0.0, 1.0, 0.20, 0.05)

        candidates = TreeOfThoughtPlanner.generate_candidate_plans(parsed_goal)

        # Re-score candidates based on sliders for interactive demonstration
        scored_candidates = []
        for c in candidates:
            if c.is_feasible:
                dyn_score = round((w_cost * c.cost_efficiency_score) + (w_exp * c.experience_rating) + (w_feas * c.feasibility_score), 2)
            else:
                deficit = c.total_cost - parsed_goal.budget_limit
                dyn_score = round(max(0.0, (w_exp * 0.20 * c.experience_rating) - (deficit * 0.01)), 2)
            scored_candidates.append({
                "Plan": c.plan_id,
                "Name": c.name,
                "Total Cost": f"₹{c.total_cost:,.0f}",
                "Lodging": c.accommodation_choice,
                "Feasible": "✅ Yes" if c.is_feasible else "❌ Exceeded",
                "Exp. Rating": f"{c.experience_rating}/100",
                "Calculated Score": dyn_score
            })

        df_tot = pd.DataFrame(scored_candidates)
        st.dataframe(df_tot, use_container_width=True, hide_index=True)

        # Highlight Winner
        winner_row = max(scored_candidates, key=lambda x: x["Calculated Score"])
        st.success(
            f"🏆 **Top-Ranked Candidate Plan:** **{winner_row['Plan']}: {winner_row['Name']}** "
            f"(Score: {winner_row['Calculated Score']} / 100)\n\n"
            f"Provides balanced comfort with AC transit and beachfront resort lodging while adhering to the ₹10,000 budget ceiling."
        )

# =============================================================================
# TAB 3: REACT LIVE DEMO
# =============================================================================
with tabs[2]:
    st.header("⚡ Live ReAct (Reasoning + Acting) Demonstration")
    st.markdown(
        "Execute the live ReAct agent loop connecting high-level thoughts with low-level Python tool dispatches. "
        "Observe the controlled failure (Sunset Beach Resort unavailable) and autonomous dynamic replanning in real time."
    )

    start_col, summary_col = st.columns([1, 2])
    with start_col:
        run_react_btn = st.button("🚀 Start Live ReAct Execution", type="primary", use_container_width=True)

    if run_react_btn or "react_executed" not in st.session_state:
        # Execute ReAct
        candidates = TreeOfThoughtPlanner.generate_candidate_plans(parsed_goal)
        best_cand, _ = TreeOfThoughtPlanner.select_best_candidate(candidates)
        react_agent = ReActAgent(
            goal=parsed_goal,
            selected_candidate=best_cand,
            reasoning_summary=cot_summary,
            candidate_plans=candidates
        )
        plan_result = react_agent.run()
        st.session_state["react_executed"] = plan_result
        st.session_state["react_agent"] = react_agent

    plan_result = st.session_state["react_executed"]

    with summary_col:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Cost", f"₹{plan_result.total_cost:,.0f}")
        m2.metric("Remaining Buffer", f"₹{plan_result.remaining_budget:,.0f}")
        m3.metric("Replanning Triggered", "YES (Step 3-4)" if plan_result.replanning_occurred else "NO")
        m4.metric("Approval Status", "APPROVED ✅" if plan_result.is_approved else "REJECTED ❌")

    st.subheader("📜 Actual Execution Trace (Thought → Action → Observation)")

    for step in plan_result.execution_trace:
        is_failure = (step.status == "FAILED")
        is_replan = ("replan" in step.action or "verify_availability" in step.action)

        if is_failure:
            css_class = "trace-step-failure"
            badge = "❌ FAILED (CONTROLLED FAILURE INTERCEPTED)"
        elif is_replan:
            css_class = "trace-step-replan"
            badge = "🔄 DYNAMIC REPLANNING"
        else:
            css_class = "trace-step-success"
            badge = "✅ SUCCESS"

        st.markdown(f"""
        <div class="{css_class}">
            <b>STEP {step.step_number}: {badge}</b><br>
            <b>💭 Thought:</b> {step.thought}<br>
            <b>⚡ Action:</b> <code>{step.action}</code> &nbsp;|&nbsp; <b>Input:</b> <code>{step.action_input}</code><br>
            <b>👁️ Observation:</b> {step.observation}<br>
            <b>💰 Cost Impact:</b> ₹{step.cost:,.0f}
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📊 Final Itemized Trip Budget")
    b_cols = st.columns(4)
    b_cols[0].info(f"**🚆 Transportation**\n\n₹{plan_result.cost_breakdown.get('transportation', 0):,.0f}")
    b_cols[1].info(f"**🏨 Lodging (Guesthouse)**\n\n₹{plan_result.cost_breakdown.get('accommodation', 0):,.0f}")
    b_cols[2].info(f"**🍽️ Meals & Dining**\n\n₹{plan_result.cost_breakdown.get('food', 0):,.0f}")
    b_cols[3].info(f"**🛵 Sightseeing & Scooter**\n\n₹{plan_result.cost_breakdown.get('sightseeing', 0):,.0f}")

# =============================================================================
# TAB 4: CRITIQUE AND IMPROVEMENT
# =============================================================================
with tabs[3]:
    st.header("🔍 Critique, Planning Errors & Architectural Improvements")
    st.markdown(
        "Critical analysis of autonomous agent planning vulnerabilities identified in the Goa case study, "
        "and empirical demonstration of safety guardrails."
    )

    st.subheader("⚠️ Three Identified Planning Weaknesses")
    critiques = PlanningCritiqueEngine.get_critique_analyses()

    for crit in critiques:
        with st.expander(f"🚨 {crit.title}", expanded=True):
            st.markdown(f"**Problem Statement:** {crit.problem_statement}")
            st.markdown(f"**Where it Occurs:** {crit.occurrence_locus}")
            st.markdown(f"**Cascading Consequences:** {crit.cascading_consequences}")
            st.markdown(f"**Proposed Improvement:** {crit.proposed_improvement}")
            st.markdown("**Architectural Remedy Mechanisms:**")
            for mech in crit.remedy_mechanisms:
                st.markdown(f"- {mech}")

    st.divider()
    st.subheader("🛠️ Before vs. After Improvement Demonstrations")

    demo_choice = st.radio(
        "Select Improvement Mechanism to Inspect:",
        [
            "1. Independent Pre-Verification (Prevents Sunk Cost Fallacy)",
            "2. Dynamic Real-Time Budget Guardrails (Prevents Budget Creep)"
        ],
        horizontal=True
    )

    if "Pre-Verification" in demo_choice:
        demo_data = PlanningCritiqueEngine.demonstrate_pre_verification_improvement()
        col1, col2 = st.columns(2)
        with col1:
            st.error("❌ **Naive ReAct Approach (Vulnerable)**")
            st.markdown(
                "1. Books non-refundable transit tickets for ₹2,000.\n"
                "2. Checks Sunset Beach Resort -> **FAILED (Unavailable)**.\n"
                "3. *Consequence:* Transit money is committed before knowing if rooms exist!"
            )
        with col2:
            st.success("✅ **Hardened Approach (With Pre-Verification)**")
            st.markdown(
                "1. Calls `verify_availability('Sunset Beach Resort')` -> Unavailable detected!\n"
                "2. Calls `verify_availability('Palm Breeze')` -> Available confirmed!\n"
                "3. Locks in transit tickets for ₹2,000 with 100% certainty of lodging.\n"
                "4. *Benefit:* Zero stranded financial risk!"
            )

    else:
        demo_data = PlanningCritiqueEngine.demonstrate_budget_guardrail_improvement(proposed_luxury_accommodation=4800.0)
        col1, col2 = st.columns(2)
        with col1:
            st.error("❌ **Without Budget Guardrail**")
            st.markdown(
                "1. Agent attempts luxury villa at ₹4,800.\n"
                "2. Transit: ₹2,000 + Lodging: ₹4,800 + Food: ₹3,000 + Sightseeing: ₹1,200 = **₹11,000**.\n"
                "3. Discovers budget failure only at step 6 (`verify_budget`). Must scrap entire plan."
            )
        with col2:
            st.success("✅ **With Dynamic Budget Guardrail**")
            st.markdown(
                f"1. Maximum allowable lodging envelope calculated: **₹{demo_data['max_allowable_for_accommodation']:,.0f}**.\n"
                f"2. Proposed villa (₹{demo_data['proposed_accommodation_cost']:,.0f}) breaches envelope.\n"
                f"3. Guardrail automatically intervenes: **{demo_data['guardrail_decision']}** to budget guesthouse (₹{demo_data['selected_fallback_cost']:,.0f}).\n"
                f"4. Prevents an overrun of ₹{demo_data['financial_safety_savings']:,.0f} in real time!"
            )

# =============================================================================
# TAB 5: GROUP DEBATE
# =============================================================================
with tabs[4]:
    st.header("🗣️ Academic Group Debate & Discussion Preparation")
    st.markdown(
        "Structured debate topics exploring the fundamental trade-offs between Agent Architectures, "
        "Reasoning Paradigms, and Autonomous Recovery Boundaries."
    )

    topics = DebateContentManager.get_all_topics()
    selected_topic_num = st.selectbox(
        "Select Debate Question to Prepare / Debate:",
        [f"Question {t.question_number}: {t.question}" for t in topics]
    )

    t_num = int(selected_topic_num.split(":")[0].replace("Question", "").strip())
    topic = DebateContentManager.get_topic_by_number(t_num)

    st.subheader(f"Q{topic.question_number}: {topic.question}")
    st.caption(f"**Curriculum Mapping:** {topic.concept_mapping}")

    p_col, c_col = st.columns(2)
    with p_col:
        st.markdown("#### 🟢 Arguments In Favor / Supporting")
        for arg in topic.arguments_supporting:
            st.markdown(f"- {arg}")

    with c_col:
        st.markdown("#### 🔴 Arguments Opposing / Counterarguments")
        for arg in topic.arguments_opposing:
            st.markdown(f"- {arg}")

    st.markdown("#### 💡 Sample Student-Level Model Answer")
    st.info(topic.sample_student_answer)
    st.caption(f"**Core Takeaway:** {topic.key_takeaway}")

    st.divider()
    st.subheader("📝 Record Group Conclusions")
    st.markdown("Enter your student debate group's consensus conclusions below:")

    g_group_name = st.text_input("Group Name / Number:", value="Group 5 - Autonomous Systems")
    g_conclusion = st.text_area(
        "Group Consensus Notes & Synthesis:",
        value=(
            "Our group concluded that while pure ReAct effectively catches runtime tool errors, "
            "it must be paired with Tree-of-Thought for upfront exploration and a Model-Based memory "
            "to prevent repeating failed inquiries."
        )
    )

    if st.button("Save & Download Debate Conclusions"):
        download_payload = {
            "group": g_group_name,
            "topic_debated": f"Q{topic.question_number}: {topic.question}",
            "student": "Vedant Sattejkumar Kirange (Roll No: 55, PRN: ADT23SOCB1294)",
            "consensus": g_conclusion
        }
        st.download_button(
            "📥 Download Group Notes JSON",
            data=json.dumps(download_payload, indent=2),
            file_name=f"debate_conclusions_q{topic.question_number}.json",
            mime="application/json"
        )
        st.success("Debate notes recorded successfully!")


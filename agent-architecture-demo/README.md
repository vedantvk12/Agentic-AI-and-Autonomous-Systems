# Agent Architecture Comparison and ReAct-Based Reasoning Demonstrator

**MIT ADT UNIVERSITY, PUNE | SCHOOL OF COMPUTING**  
**Department of Artificial Intelligence & Data Science**  
**Units I & II:** Introduction to Agentic AI & Autonomous Systems; Reasoning, Planning and Decision-Making  
**Course Outcomes:** CO I & CO II  
**Activity Name:** Group Debate and Live Demonstration – Agent Architectures and ReAct-Based Reasoning in Practice  

---

## 👨‍🎓 Student Details
- **Student Name:** Vedant Sattejkumar Kirange
- **Roll Number:** 55
- **PRN:** ADT23SOCB1294
- **Academic Year:** 2025–2026

---

## 🎯 Project Overview
This project provides an interactive academic demonstration and research system that allows university students and educators to:
1. **Compare Five Agent Architectures:** Implement and empirically evaluate Simple Reflex, Model-Based Reflex, Goal-Based, Utility-Based, and Learning Agents side-by-side.
2. **Implement Advanced Reasoning Frameworks:** Contrast linear Chain-of-Thought (CoT) decomposition, multi-branch Tree-of-Thought (ToT) alternative exploration, and grounded ReAct (Reasoning + Acting) execution.
3. **Execute a Live ReAct Loop with Controlled Failure:** Ground high-level planning into real Python tool functions (`calculate_transport`, `search_accommodation`, `verify_availability`, `estimate_food_cost`, `select_sightseeing`, `calculate_total_budget`, `verify_budget`). Intercept a realistic room unavailability event for Sunset Beach Resort and trigger autonomous dynamic replanning in-flight to Palm Breeze Budget Guesthouse.
4. **Critique Systemic Planning Errors:** Formally analyze three core vulnerabilities (unverified assumptions, incomplete observations, and budget overrun risk) and demonstrate hardened architectural guardrails.
5. **Interactive Classroom Debate Platform:** Deliver an interactive 5-tab Streamlit dashboard and complete debate preparation notes for 10 foundational topics with balanced PRO/CON arguments and sample student model answers.

---

## 🏛️ 1. Five Agent Architectures

| Agent Architecture | Internal Structure | Decision-Making Method | Advantages | Limitations | Real-World Application |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Simple Reflex Agent** | Sensors $\rightarrow$ Condition-Action Rules $\rightarrow$ Actuators. Completely stateless. | Instantaneous lookup in condition-action table. Matches current percept only. | $O(1)$ Ultra-fast, minimal memory, deterministic. | Infinite loops, zero memory, cannot plan or adapt. | Thermostats, ABS brakes, simple packet firewalls. |
| **Model-Based Reflex Agent** | Sensors $\rightarrow$ State Tracker $\rightarrow$ Internal World Model $\rightarrow$ Rules with State $\rightarrow$ Actuators. | Evaluates condition-action rules using percept AND historical internal state. | Handles partial observability, avoids repetitive cyclic errors, tracks budget. | Model drift if environment diverges, lacks goal optimization. | Robotic vacuum room mapping, automotive cruise control. |
| **Goal-Based Agent** | Sensors $\rightarrow$ State $\rightarrow$ Goal Specification $\rightarrow$ Planning Engine $\rightarrow$ Actuators. | Forward search or hierarchical goal reduction toward goal state. | Highly flexible; re-targets easily without changing rule tables. | Binary success only; cannot quantify plan quality or comfort. | GPS route navigation, warehouse pick-and-pack planners. |
| **Utility-Based Agent** | Sensors $\rightarrow$ State $\rightarrow$ Utility Function $U(s)$ $\rightarrow$ Optimization Engine $\rightarrow$ Actuators. | Maximizes Expected Utility over competing candidate paths. | Balances conflicting trade-offs (cost vs comfort vs activities). | Designing weights is complex; combinatorial compute cost. | Algorithmic trading, personalized travel recommendation. |
| **Learning Agent** | Critic $\rightarrow$ Learning Element $\rightarrow$ Performance Element $\rightarrow$ Problem Generator. | Reinforcement / Bayesian updates based on empirical feedback signals. | Self-improving; autonomously learns supplier unreliability. | Exploration carries real-world failure risk; needs episodes. | Autonomous driving, adaptive recommendation systems. |

---

## 🧠 2. Reasoning Frameworks (CoT, ToT, ReAct)

### A. Chain-of-Thought (CoT) Goal Decomposition
- **Goal:** *"Plan a 2-day Goa trip for 2 people within ₹10,000, including transportation, accommodation, food and sightseeing."*
- **Entities & Constraints:** Destination: Goa | Duration: 2 Days | Travelers: 2 People | Budget Limit: ₹10,000.
- **Ordered Subtask Pipeline:**
  1. `calculate_transport()`: Round-trip tickets lock in dates and arrival logistics.
  2. `search_accommodation()`: Verifies room inventory to anchor overnight stay.
  3. `estimate_food_cost()`: Allocates daily meal allowance for 2 travelers.
  4. `select_sightseeing()`: Books scooter mobility and cultural fort visits.
  5. `calculate_total_budget()`: Aggregates itemized component costs.
  6. `verify_budget()`: Formally audits sum against the ₹10,000 ceiling.

### B. Tree-of-Thought (ToT) Multi-Branch Evaluation
- **Plan A (Budget-Focused):** Non-AC Train (₹1,600) + Hostel Pod (₹1,500) + Dhabas (₹2,000) + Walks (₹800) = **₹5,900** [Feasible] | Score: **59.80/100**
- **Plan B (Balanced) [WINNER]:** AC 3-Tier Train (₹2,000) + Beach Resort (₹3,000) + Shack Thalis (₹3,000) + Scooter (₹1,200) = **₹9,200** [Feasible] | Score: **66.40/100**
- **Plan C (Luxury):** Volvo Bus (₹2,800) + Luxury Villa (₹4,800) + Fine Dining (₹4,000) + Scuba/Cab (₹2,500) = **₹14,100** [Infeasible] | Score: **0.00/100 (Pruned)**

### C. ReAct Closed-Loop Execution & Controlled Failure
```
[Plan B Selected]
       |
       v
Thought: Need transportation before accommodation.
Action: calculate_transport() -> ₹2,000
       |
       v
Thought: Check accommodation availability.
Action: search_accommodation('Sunset Beach Resort')
Observation: FAILED (Fully booked due to peak rush!)
       |
       v
[CONTROLLED FAILURE INTERCEPTED]
       |
       +---> 1. Detect failed assumption
       +---> 2. Record failure observation
       +---> 3. Explain planning error
       +---> 4. Generate candidate guesthouses
       +---> 5. verify_availability('Palm Breeze Budget Guesthouse') -> Verified Available!
       +---> 6. replan_accommodation() -> Booked for ₹2,000 (Saved ₹1,000!)
       |
       v
Continue: estimate_food_cost() -> ₹3,000
Continue: select_sightseeing() -> ₹1,200
Sum: calculate_total_budget() -> ₹8,200
Audit: verify_budget() -> PASSED (₹1,800 Buffer Remaining)
```

---

## 📁 Project Directory Structure
```
agent-architecture-demo/
│
├── main.py                              # CLI runner executing all 5 agents, reasoning loops & tests
├── app.py                               # 5-Tab Interactive Streamlit Academic Dashboard
├── create_diagrams.py                   # High-resolution (300 DPI) publication diagram generator
├── generate_assignment_report.py        # Professional Word (DOCX) & PDF report builder
├── debate_preparation_notes.md          # 10 Academic Debate Topics with PRO/CON & Model Answers
├── requirements.txt                     # Pinned project dependencies
│
├── agents/                              # Core Agent Architecture Classes
│   ├── __init__.py
│   ├── simple_reflex.py                 # Architecture A: Condition-Action Rules (Stateless)
│   ├── model_based.py                   # Architecture B: Internal World Model & State Tracker
│   ├── goal_based.py                    # Architecture C: Explicit Goal & Hierarchical Reduction
│   ├── utility_based.py                 # Architecture D: Multi-Attribute Utility Function U(s)
│   └── learning_agent.py                # Architecture E: 4-Component Adaptive Learning Agent
│
├── reasoning/                           # Reasoning Frameworks
│   ├── __init__.py
│   ├── models.py                        # Shared dataclasses (Goal, Task, Trace, Plan)
│   ├── cot_planner.py                   # Chain-of-Thought Goal Decomposition
│   ├── tot_planner.py                   # Tree-of-Thought Multi-Branch Exploration & Scoring
│   └── react_agent.py                   # ReAct Thought->Action->Observation Engine with Replanning
│
├── tools/                               # Action Executor Tools
│   ├── __init__.py
│   └── travel_tools.py                  # Python tool functions & local inventory catalogs
│
├── evaluation/                          # Critique & Evaluation Modules
│   ├── __init__.py
│   ├── comparison.py                    # Side-by-side 6-column agent benchmark matrix
│   ├── critique.py                      # Planning weaknesses analysis & guardrails demo
│   └── debate_topics.py                 # 10 Structured academic debate questions & model answers
│
└── outputs/                             # Verified Runtime Execution Artifacts
    ├── execution_trace.txt              # Actual Thought/Action/Observation execution trace
    ├── candidate_plans.json             # ToT candidate exploration and scoring results
    ├── evaluation_results.json          # Complete benchmark and critique simulation data
    ├── system_architecture.png          # High-resolution (300 DPI) system architecture diagram
    └── agent_architectures_comparison.png# High-resolution (300 DPI) agent comparison diagram
```

---

## 🚀 Setup and Execution Instructions

### 1. Environment Setup
Ensure Python 3.10+ is installed:
```bash
pip install -r requirements.txt
```

### 2. Run Command-Line Benchmark & Verification
To execute the complete demonstration pipeline (all five agent classes, CoT decomposition, ToT branch scoring, live ReAct trace with failure interception, critique improvements, and artifact export):
```bash
python main.py
```

### 3. Launch Interactive Streamlit Dashboard
To launch the interactive academic dashboard:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser to explore:
- **Tab 1: Agent Architectures:** Compare agent structures and run live percept scenarios.
- **Tab 2: CoT & ToT:** Inspect task dependencies and interactively tune utility weight sliders.
- **Tab 3: ReAct Live Demo:** Trigger the ReAct engine, watch the accommodation failure, and observe dynamic replanning.
- **Tab 4: Critique & Improvement:** Analyze systemic failure modes and toggle pre-verification and budget guardrails.
- **Tab 5: Group Debate:** Review 10 debate questions with arguments and record your group's consensus notes.

### 4. Generate Academic Report & Diagrams
To re-generate the high-resolution architecture diagrams and the formal university submission documents:
```bash
python create_diagrams.py
python generate_assignment_report.py
```

---

## 📊 Final Verified Budget Summary
- **Transportation:** ₹2,000 (Konkan Express AC 3-Tier Sleeper Round-Trip for 2)
- **Accommodation (Replanned):** ₹2,000 (Palm Breeze Budget Guesthouse AC Room)
- **Food & Dining:** ₹3,000 (Local Beach Shacks & Authentic Thalis across 2 days)
- **Sightseeing & Commute:** ₹1,200 (Fort Aguada, Churches & 2-Day Scooter Rental)
- **Total Expenditure:** **₹8,200**
- **Remaining Safety Buffer:** **₹1,800**
- **Approval Status:** **APPROVED (Within ₹10,000 Budget Ceiling)**

---

## 📜 Academic Deliverables Included
1. `Units_I_II_Agent_Architecture_Debate_Assignment.pdf`: Formal 15-page university assignment report adhering to strict MIT ADT layout guidelines.
2. `Units_I_II_Agent_Architecture_Debate_Assignment.docx`: Fully styled Microsoft Word report with native formatting, callouts, and XML-anchored tables.
3. `agent-architecture-demo-source-code.zip`: Standalone redistributable archive containing complete project code and assets.
4. `README.md`: This comprehensive technical guide.
5. `execution_trace.txt`: Actual, un-fabricated execution trace.
6. `system_architecture.png` & `agent_architectures_comparison.png`: 300 DPI publication-quality diagrams.
7. `debate_preparation_notes.md`: Exhaustive debate preparation notes.


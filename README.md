# Physics-Informed Generative Agent for Autonomous Aerial Delivery System Design

A multi-agent drone design system that takes a mission specification and generates, screens, validates, and ranks novel aerial delivery drone configurations using LangGraph, Gemini-based specialist agents, physics-inspired models, machine-learning screening, and active learning.

## Project idea

The assignment asks for a system that does not search existing drone designs. Instead, it should invent plausible drone configurations from first principles such as aerodynamics, propulsion, structures, control, energy use, and cost.

This project follows that idea by splitting the mission into specialist engineering roles and combining their outputs into candidate drone designs.

## Mission used

The system is designed around this delivery mission:

* Payload: 5 kg
* Range: 10 km
* Environment: Dense urban area
* Crosswind: 15 m/s
* GPS: unavailable
* Platform: single drone
* Budget: $5000

## What the system does

1. Reads the mission specification.
2. Runs 4 specialist agents:

   * Aerodynamics
   * Propulsion
   * Structures
   * Control
3. Uses a supervisor to combine agent outputs into complete drone proposals.
4. Generates a large pool of candidate configurations.
5. Screens candidates using a fast ML model.
6. Validates the best candidates with physics-based checks.
7. Runs a 3-round active learning loop.
8. Outputs the top 3 designs with performance estimates and test protocol.

## Core workflow

```text
Mission specification
        ↓
LangGraph workflow
        ↓
Aerodynamics / Propulsion / Structures / Control agents
        ↓
Supervisor
        ↓
200+ complete drone designs
        ↓
RandomForest low-fidelity screening
        ↓
Physics validation
        ↓
Active learning loop (3 rounds)
        ↓
Top 3 designs
        ↓
JSON report
```

## Agent roles

### Aerodynamics Agent

Focuses on wing area, drag coefficient, propeller diameter, and fuselage design.

### Propulsion Agent

Focuses on battery capacity, motor KV, motor type, and voltage.

### Structures Agent

Focuses on material choice, estimated weight, safety factor, and cost.

### Control Agent

Focuses on PID gains, wind tolerance, and navigation method for GPS-denied operation.

### Supervisor

Combines the agent proposal pools into complete drone configurations.

### Judge

Ranks the final candidates using performance, cost, wind tolerance, and physics-based reasoning.

## Physics-informed models

The project uses simplified but explicit engineering models for:

* Lift
* Drag
* Flight time
* Energy consumption
* Structural stress
* Control stability
* Cost

These models are intentionally lightweight so the full system can run as a prototype during an internship assessment.

## Machine learning screener

The low-fidelity screening stage uses a RandomForestRegressor model. It acts as a fast first-pass selector before higher-fidelity physics validation.

This gives the pipeline a multi-fidelity structure:

* Fast screening for large candidate pools
* Physics-based validation for top designs
* Final ranking for submission output

## Active learning

The system runs 3 rounds of active learning:

1. Generate candidates
2. Screen and validate
3. Keep the best design
4. Mutate around the best design
5. Repeat

This helps the design improve over multiple rounds rather than relying on a single pass.

## Files in the project

```text
drone_design_ai/
│
├── core/
│   ├── agents.py
│   ├── supervisor.py
│   ├── physics.py
│   ├── generator.py
│   ├── ml_screener.py
│   ├── ranker.py
│   ├── active_learning.py
│   ├── report_generator.py
│   └── langgraph_workflow.py
│
│
├── README.md
├── requirements.txt
└── .gitignore
```

## How to run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Do not commit the `.env` file to GitHub.

### 3. Run the main pipeline

```bash
python core/langgraph_workflow.py
```

or, if you are using the top-level runner:

```bash
python run_drone_design.py
```

### 4. Run the test scripts

```bash
python core/test_pipeline.py
python core/test_report_generator.py
python core/test_active_learning.py
```

## Expected outputs

The project produces these files:

* `ranked_designs.json`
* `designs.json`
* `top_design_reports.json`
* `output_report.pdf`
## Final takeaway

This project shows how a LangGraph-based multi-agent system can explore drone design space using engineering reasoning, physics, machine learning, and iterative refinement.

It is a prototype, but it follows the structure of a real design workflow rather than a single prompt response.

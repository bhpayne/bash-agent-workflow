# workflow.py

import json
import os

STAGES = {
    1: {
        "name": "Goal Specification",
        "instructions": "Prompt the user to define the overall goal if it is not yet clear. Do not proceed until the goal is established. The goal doesn't have to be something you can accomplish immediately as the next step will be to decompose the task. Once the goal has been set, write the file `GOAL.md`",
        "file_dependencies": ["GOAL.md"],
    },
    2: {
        "name": "Requirements Formulation",
        "instructions": "Work with the user to iteratively draft specific, verifiable requirements. Write these to `REQUIREMENTS.md`.",
        "file_dependencies": ["REQUIREMENTS.md"],
    },
    3: {
        "name": "Completion Definitions",
        "instructions": "Append explicit 'Definition of Done' / success criteria to respective entries in `REQUIREMENTS.md`. Identify edge cases and propose quantitative boundary conditions.",
        "file_dependencies": ["REQUIREMENTS.md"],
    },
    4: {
        "name": "Use Cases",
        "instructions": "Propose use cases describing the intended workflow. Write these to `USE_CASES.md`.",
        "file_dependencies": ["USE_CASES.md"],
    },
    5: {
        "name": "High-Level Planning & Task Sequence",
        "instructions": "Based on REQUIREMENTS.md, design an implementation task sequence and write it to PLAN.md.",
        "file_dependencies": ["PLAN.md"],
    },
    6: {
        "name": "Design Evaluation & Recommendations",
        "instructions": "Identify design options, document them in `DESIGN.md`, recommend one with trade-offs, and note the selections once accepted.",
        "file_dependencies": ["DESIGN.md"],
    },
    7: {
        "name": "Interface Definition",
        "instructions": "Define interfaces, API boundaries, or data contracts between components. Document them in `INTERFACES.md`.",
        "file_dependencies": ["INTERFACES.md"],
    },
    8: {
        "name": "Component Testing",
        "instructions": "Design programs to perform validation checks of each part from PLAN.md and write these tests to files.",
        "file_dependencies": [],
    },
    9: {
        "name": "Task Enactment",
        "instructions": "Systematically execute tasks in PLAN.md one-by-one. Align code with tests. Update PLAN.md with [Pending], [In Progress], or [Completed].",
        "file_dependencies": ["PLAN.md"],
    },
    10: {
        "name": "Test Components",
        "instructions": "Execute the tests developed in Stage 8 and evaluate whether the criteria in REQUIREMENTS.md are met.",
        "file_dependencies": [],
    },
    11: {
        "name": "Integration Testing",
        "instructions": "Write integration tests addressing stories in USE_CASES.md. Document results in TEST_RESULTS.log.",
        "file_dependencies": ["TEST_RESULTS.log"],
    },
    12: {
        "name": "Goal Validation",
        "instructions": "If all tests pass, ask explicitly: 'Has the goal been accomplished to your satisfaction?' Do not conclude until confirmed.",
        "file_dependencies": [],
    },
}


class WorkflowManager:
    def __init__(self, state_file=".workflow_state.json"):
        self.state_file = state_file
        self.current_stage = 1
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    self.current_stage = data.get("current_stage", 1)
            except Exception:
                self.current_stage = 1

    def save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump({"current_stage": self.current_stage}, f)
        except Exception as e:
            print(f"[Warning] Failed to save workflow state: {e}")

    def get_stage_prefix(self) -> str:
        stage_name = STAGES[self.current_stage]["name"]
        return f"[STAGE {self.current_stage}: {stage_name}]"

    def get_current_instructions(self) -> str:
        stage_info = STAGES[self.current_stage]
        deps = (
            f"\nFiles associated with this stage: {', '.join(stage_info['file_dependencies'])}"
            if stage_info["file_dependencies"]
            else ""
        )
        return f"CURRENT ACTIVE STAGE: {self.get_stage_prefix()}\nInstructions: {stage_info['instructions']}{deps}"

    def advance_stage(self) -> bool:
        if self.current_stage < len(STAGES):
            self.current_stage += 1
            self.save_state()
            return True
        return False

    def regress_stage(self) -> bool:
        if self.current_stage > 1:
            self.current_stage -= 1
            self.save_state()
            return True
        return False

#!/usr/bin/env python3

# see https://en.wikipedia.org/wiki/V-model

import json
import os

STAGES = {
    1: {
        "name": "Goal Specification",
        "instructions": "Prompt me to define the overall goal. Do not proceed to the next stage until the goal is established. The goal doesn't have to be something you can accomplish immediately as the next step will be to decompose the task. Goals that are ambitious or imprecise are acceptable. Once the goal has been set, write the file `GOAL.md`",
        "file_dependencies": ["GOAL.md"],
    },
    2: {
        "name": "Requirements Formulation",
        "instructions": "Read the file `GOAL.md` and brainstorm with me to iteratively draft specific, verifiable requirements. These requirements refine and support the content stated in `GOAL.md`. Propose one requirement at a time to be added. Once the user concurs with a requirement, Write the requirement to the file `REQUIREMENTS.md`. This stage is complete once the user signs off on the requirements being comprehensive.",
        "file_dependencies": ["REQUIREMENTS.md", "GOAL.md"],
    },
    3: {
        "name": "Completion Definitions",
        "instructions": "Read the file `REQUIREMENTS.md` and brainstorm with the user to come up with 'Definition of Done' or success criteria to each entries in `REQUIREMENTS.md`. Identify edge cases and propose quantitative boundary conditions. Once the user concurs with a proposed Definition of Done, append the explicit success criteria to each requirement.",
        "file_dependencies": ["REQUIREMENTS.md"],
    },
    4: {
        "name": "Use Cases",
        "instructions": "Read the `GOAL.md` file and the `REQUIREMENTS.md` file. Propose a use case describing the intended workflow. Once I concur, append the use case to the file `USE_CASES.md`. Propose additional use cases until I sign off on this stage.",
        "file_dependencies": ["USE_CASES.md"],
    },
    5: {
        "name": "High-Level Planning & Task Sequence",
        "instructions": "Based on reading the files `REQUIREMENTS.md` and `GOAL.md` and `USE_CASES.md`, brainstorm with me the design of a task sequence. Once I concur write the plan to a file called `PLAN.md`.",
        "file_dependencies": ["PLAN.md"],
    },
    6: {
        "name": "Design Evaluation & Recommendations",
        "instructions": "Read the files `REQUIREMENTS.md` and `GOAL.md` and `USE_CASES.md` and `PLAN.md`. Identify design options for implementation and propose the options to me. Examples include which programming language to use, which operating system to support, whether software should be command-line or have a GUI, etc. If I concur that the design option is relevant then document the design choice in `DESIGN.md`. Then recommend one of the options, explain the trade-offs. If I accept the selection then note which was accepted in `DESIGN.md`.",
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

#!/usr/bin/env python3

import os

# Python's `dataclasses` library explicitly prevents mutable lists.
# If that weren't used then lists would be created only once when the
# class itself is defined. Every instance of that class would then
# share the exact same list in memory.
from dataclasses import dataclass, field


@dataclass
class Config:

    # Google Gemini's OpenAI-compatible API base endpoint
    llm_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"

    # model list: https://ai.google.dev/gemini-api/docs/models
    # llm_model_name: str = "gemini-2.5-flash"
    llm_model_name: str = "gemini-3.1-flash-lite"
    # llm_model_name: str = "gemini-3-flash-preview"

    # Attempts to read from environment variable first, otherwise falls back to the string
    llm_api_key: str = os.environ.get("GEMINI_API_KEY", "YOUR_GOOGLE_GEMINI_API_KEY")

    # Sampling parameters
    llm_temperature: float = 0.1
    llm_top_p: float = 0.95

    # Determine whether to write prompts and responses to log files
    log_prompts: bool = False

    # -------------------------------------
    # Agent configuration
    # -------------------------------------

    starting_directory: str = None
    root_dir: str = None

    def __post_init__(self):
        # Dynamically set the root directory once the instance is initialized
        if self.starting_directory:
            self.root_dir = self.starting_directory
        else:
            self.root_dir = os.path.dirname(os.path.abspath(__file__))

    # Flag to enable container/VM specific commands
    inside_container_or_virtual_machine: bool = False

    @property
    def allowed_commands(self) -> list:
        commands = [
            "basename",
            "bc",
            "break",
            "cat",
            "cd",
            "continue",
            "cp",
            "date",
            "diff",
            "dmesg",
            "do",
            "du",
            "echo",
            "elif",
            "else",
            "fi",
            "find",
            "for",
            "grep",
            "head",
            "hostname",
            "if",
            "ifconfig",
            "ls",
            "mkdir",
            "netstat",
            "ping",
            "pwd",
            "sort",
            "tail",
            "time",
            "touch",
            "tr",
            "wc",
            "wget",
            "xargs",
        ]
        if self.inside_container_or_virtual_machine:
            commands.extend(
                [
                    "apptainer",
                    "awk",
                    "chgrp",
                    "chmod",
                    "chown",
                    "curl",
                    "dnf",
                    "docker",
                    "export",
                    "gh",
                    "git",
                    "glab",
                    "mv",
                    "pip3",
                    "podman",
                    "python3",
                    "rm",
                    "sed",
                    "ssh",
                    "ssh-keygen",
                ]
            )
        # Use dict.fromkeys to safely remove duplicates (like 'wget') while preserving list order
        return list(dict.fromkeys(commands))

    def generate_system_prompt(self, active_stage_instructions: str) -> str:
        """Generate the system prompt based on allowed commands and the active stage."""
        return f"""/think

You are a helpful and very concise Bash assistant executing commands in the shell.
You are helping the user execute a highly structured, gated workflow.

When a command is executed, you will be given the output from that command and any errors. Based on
that, either take further actions or yield control to the user.

The bash interpreter's output and current working directory will be given to you every time a
command is executed. Take that into account for the actions you are taking.
If there was an error during execution, tell the user what that error was exactly.

---
{active_stage_instructions}
---

Your role in this step is strictly bounded by the current active stage. 
Do not jump ahead to future stages or attempt to write code for future steps 
unless the current stage explicitly dictates it.

You are only allowed to execute the following commands:
```
{self.allowed_commands}
```

When telling the user commands to execute avoid line continuation as every line is executed separately in order.

Never attempt to execute a command not in this list. If asked to do so, politely refuse.
"""


#     @property
#     def system_prompt(self) -> str:
#         """Generate the system prompt for the LLM based on allowed commands."""
#         return f"""/think

# You are a helpful and very concise Bash assistant with the ability to execute commands in the shell.
# You engage with users to help answer questions about bash commands, or execute their intent.
# If user intent is unclear, keep engaging with them to figure out what they need and how to best help
# them.

# When a command is executed, you will be given the output from that command and any errors. Based on
# that, either take further actions or yield control to the user.

# The bash interpreter's output and current working directory will be given to you every time a
# command is executed. Take that into account for the next conversation.
# If there was an error during execution, tell the user what that error was exactly.

# You are only allowed to execute the following commands. Break complex tasks into shorter commands from this list:

# ```
# {self.allowed_commands}
# ```

# **Never** attempt to execute a command not in this list. If asked to do so, politely refuse.
# """


# EOF

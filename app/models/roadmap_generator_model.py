import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


system_prompt = """
You ONLY generate mermaid.js syntax code and nothing else.

Generate ONLY valid Mermaid.js flowchart syntax based on the following diagram description.
The diagram includes a detailed, branching structure, not just a linear flow — break down broad topics into subtopics or steps.

Rules:-
-Use only valid node definitions: NodeID[Node Label]

-Node IDs must be unique, and must not contain spaces or special characters

-Node labels inside [] must avoid: Parentheses (), Commas, Quotes, colons, slashes, or other special characters

-All connections must be in the form: A --> B

-Do not include any plain text, explanation, or comments — only output a single valid Mermaid code block

-Avoid special characters like commas and parentheses in node labels unless escaped or replaced.
"""


class RoadmapModel():
    def __init__(self):
        self.roadmap_model = ChatOllama(model="qwen2.5-coder:7b", temperature=0.8,)
        self.system_prompt = system_prompt
        
        
    def generate_mermaid_code(self, user_prompt):
        response = self.roadmap_model.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt)
        ])
        mermaid_code = self.extract_mermaid_code(response.content)
        return mermaid_code
        
        
    def extract_mermaid_code(self, text: str) -> str:
        """Extracts and sanitizes Mermaid diagram code from the LLM response.
        Strips ```mermaid ... ``` fences, cleans node labels, and extra whitespace."""
        
        # Extracting inside ```mermaid ... ```
        match = re.search(r"```mermaid\s*(.*?)```", text, re.DOTALL)
        code = match.group(1).strip() if match else text.strip()

        # Sanitize node labels: force safe characters inside []
        def sanitize_labels(match):
            p1 = match.group(1)
            safe_text = re.sub(r"[\[\]\(\)\{\}]", "", p1)  # stripping special chars
            return f"[{safe_text}]"
        
        self.code = re.sub(r"\[(.*?)\]", sanitize_labels, code)
        return code

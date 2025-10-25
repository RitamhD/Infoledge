import re
from ollama import Client


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

class RoadmapModel:
    model2 = "qwen2.5-coder:7b-cloud"
    model1 = "qwen3-coder:480b-cloud"
    
    def __init__(self):
        self.client = Client()  # uses logged-in Ollama credentials
        self.model_name = self.model1
        self.system_prompt = system_prompt

    def generate_mermaid_code(self, user_prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = self.client.chat(self.model_name, messages=messages)
        print(response)
        full_reply = response['message']['content']
        mermaid_code = self.extract_mermaid_code(full_reply)
        return mermaid_code

    def extract_mermaid_code(self, text: str) -> str:
        match = re.search(r"```mermaid\s*(.*?)```", text, re.DOTALL)
        code = match.group(1).strip() if match else text.strip()

        def sanitize_labels(match):
            p1 = match.group(1)
            safe_text = re.sub(r"[\[\]\(\)\{\}]", "", p1)
            return f"[{safe_text}]"
        
        code = re.sub(r"\[(.*?)\]", sanitize_labels, code)
        return code
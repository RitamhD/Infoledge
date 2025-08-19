from flask import Blueprint, render_template, request, jsonify
from langchain_core.messages import HumanMessage, SystemMessage
from ..models.roadmap_generator_model import extract_mermaid_code
from app import roadmap_model


roadmap_bp = Blueprint("roadmap", __name__)

system_prompt = """
Generate only valid Mermaid.js syntax based on the following diagram description.
Ensure:

The diagram includes a detailed, branching structure, not just a linear flow — break down broad topics into subtopics or steps.

Rules:-
-Use only valid node definitions: NodeID[Node Label]

-Node IDs must be unique, and must not contain spaces or special characters

-Node labels inside [] must avoid: Parentheses (), Commas, Quotes, colons, slashes, or other special characters

-All connections must be in the form: A --> B

-Do not include any plain text, explanation, or comments — only output a single valid Mermaid code block

-Avoid special characters like commas and parentheses in node labels unless escaped or replaced.
"""


@roadmap_bp.route("/generate_roadmap", methods=["GET", "POST"])
def generate_roadmap():
    if request.method == "GET":
        return render_template('roadmap.html')
    
    if request.method == "POST":
        try:
            data = request.get_json()    
            if not data or "prompt" not in data:
                return jsonify({"error": "Missing prompt"}), 400
            user_prompt = data["prompt"]
            print(user_prompt)
            response = roadmap_model.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])
            
            mermaid_code = extract_mermaid_code(response.content)
            
            print(mermaid_code)
            return jsonify({"mermaid_code": mermaid_code}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            

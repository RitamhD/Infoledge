from flask import Blueprint, render_template, request, jsonify, flash
from ..models.roadmap_generator_model import RoadmapModel


roadmap_bp = Blueprint("roadmap", __name__)

roadmap_model = RoadmapModel()

@roadmap_bp.route("/generate_roadmap", methods=["GET", "POST"])
def generate_roadmap():
    if request.method == "GET":
        return render_template('roadmap.html')
    
    if request.method == "POST":
        try:
            data = request.get_json()
            user_prompt = data["prompt"]
            print(user_prompt)
            mermaid_code = roadmap_model.generate_mermaid_code(user_prompt)
            
            return jsonify({"mermaid_code": mermaid_code}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

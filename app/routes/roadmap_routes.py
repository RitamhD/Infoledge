import time
from flask import Blueprint, render_template, request, jsonify, flash
from ..models.roadmap_generator_model import RoadmapModel


roadmap_bp = Blueprint("roadmap", __name__)

roadmap_model = RoadmapModel()

roadmaps = {}
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
            print(mermaid_code)
            roadmap_id = str(int(time.time() * 1000))
            roadmaps[roadmap_id] = {"roadmap_id": roadmap_id, "prompt": user_prompt, "mermaid_code": mermaid_code}
            
            return jsonify({"mermaid_code": mermaid_code, "roadmap_id": roadmap_id}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@roadmap_bp.route("/roadmap_link/<roadmap_id>")
def get_roadmap_link(roadmap_id):
    roadmap = roadmaps.get(roadmap_id)
    if not roadmap:
        return jsonify({"error": "Roadmap not found"}), 404
    return jsonify(roadmap)


@roadmap_bp.route("/roadmap_view/<roadmap_id>")
def roadmap_view(roadmap_id):
    roadmap = roadmaps.get(roadmap_id)
    if not roadmap:
        return jsonify({"error": "Roadmap not found"}), 404
    return render_template("roadmap_view.html", roadmap=roadmap)
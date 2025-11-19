from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import verify_jwt_in_request
from app import recommender


course_bp = Blueprint('course', __name__)

@course_bp.before_request
def protected():
    verify_jwt_in_request()

@course_bp.route('/recommend_courses', methods=["GET", "POST"])
def recommend_courses():
    if request.method == "GET":
        return render_template('courses.html')
    elif request.method == "POST":
        data = request.get_json()
        query = f"{data.get('level', '')} level course in {data.get('interest', '')} taught in {data.get('language', '')}"
        try:
            recommendations = recommender.getRecommendation(query)
            return jsonify(recommendations)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@course_bp.route('/recommend', methods=["POST"])
def recommend():
    data = request.get_json()
    query = data.get("query", "")
    try:
        recommendations = recommender.getRecommendation(query)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
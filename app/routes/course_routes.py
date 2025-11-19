from flask import Blueprint, render_template, request, jsonify
<<<<<<< HEAD
from flask_jwt_extended import jwt_required
=======
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
from app import recommender


course_bp = Blueprint('course', __name__)

<<<<<<< HEAD
@course_bp.before_request
@jwt_required()
def protected():
    pass

@course_bp.route('/recommend_courses', methods=["GET", "POST"])
=======
@course_bp.route('/recommend_courses', methods=["GET", "POST"])
# @login_required
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
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
<<<<<<< HEAD
=======
# @login_required
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
def recommend():
    data = request.get_json()
    query = data.get("query", "")
    try:
        recommendations = recommender.getRecommendation(query)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
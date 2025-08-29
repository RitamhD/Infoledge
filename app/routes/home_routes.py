from flask import Blueprint, render_template, redirect, url_for, request


home_bp = Blueprint("home", __name__)

@home_bp.route('/home', methods=["GET", "POST"])
@home_bp.route('/home/<user_name>', methods=["GET", "POST"])
def home(user_name=None):
    if request.method == "GET":
        return render_template('home.html', user_name=user_name)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "codemirror":
            return redirect(url_for('code.code_platform'))
        if action == "courses":
            return redirect(url_for('course.recommend_courses'))
        if action == "mermaid":
            return redirect(url_for('roadmap.generate_roadmap'))
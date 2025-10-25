from flask import Blueprint, render_template


code_bp = Blueprint('code', __name__)

@code_bp.route('/code_platform')
def code_platform():
    return render_template('code_platform.html')
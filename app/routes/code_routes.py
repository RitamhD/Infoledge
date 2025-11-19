from flask import Blueprint, render_template
from flask_jwt_extended import verify_jwt_in_request


code_bp = Blueprint('code', __name__)

@code_bp.before_request
def protected():
    verify_jwt_in_request()

@code_bp.route('/code_platform')
def code_platform():
    return render_template('code_platform.html')
from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required


code_bp = Blueprint('code', __name__)

@code_bp.before_request
@jwt_required()
def protected():
    pass

@code_bp.route('/code_platform')
def code_platform():
    return render_template('code_platform.html')
from flask import Blueprint, render_template
<<<<<<< HEAD
from flask_jwt_extended import jwt_required
=======
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935


code_bp = Blueprint('code', __name__)

<<<<<<< HEAD
@code_bp.before_request
@jwt_required()
def protected():
    pass

=======
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
@code_bp.route('/code_platform')
def code_platform():
    return render_template('code_platform.html')
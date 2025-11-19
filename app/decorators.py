<<<<<<< HEAD
# from functools import wraps
# from flask import session, redirect, url_for, flash, request, jsonify
# from app import db
# from .models.user import User
=======
from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify
from app import db
from .models.user import User
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935


# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.cookies.get('jwt_token')

#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401

#         try:
#             data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
#             current_user = User.query.filter_by(public_id=data['public_id']).first()
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 401

#         return f(current_user, *args, **kwargs)

#     return decorated
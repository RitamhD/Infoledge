import os
from flask import Blueprint, request, session, jsonify, Response
<<<<<<< HEAD
from flask_jwt_extended import jwt_required
=======
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
from app import chat_model


chat_bp = Blueprint("chat", __name__)

<<<<<<< HEAD
@chat_bp.before_request
@jwt_required()
def protected():
    pass

@chat_bp.route("/chat", methods=["POST"])
=======
@chat_bp.route("/chat", methods=["POST"])
# @login_required
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    if not user_message:
        return "No message from user", 400

    session_id = session.get("chat_session_id", os.urandom(8).hex())
    session["chat_session_id"] = session_id

    chain = chat_model.getChain()
    response = chain.invoke(user_message, config={"configurable": {"session_id": session_id}})
    return jsonify({"answer": response.content})


@chat_bp.route("/stream-chat", methods=["POST"])
<<<<<<< HEAD
=======
# @login_required
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
def stream_chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()
    if not user_message:
        return "No message from user", 400

    session_id = session.get("chat_session_id", os.urandom(8).hex())
    session["chat_session_id"] = session_id

    chain = chat_model.getChain()

    def generate():
        for chunk in chain.stream(user_message, config={"configurable": {"session_id": session_id}}):
            yield chunk.content

    return Response(generate(), content_type="text/plain; charset=utf-8")

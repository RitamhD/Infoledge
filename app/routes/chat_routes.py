import os
from flask import Blueprint, request, session, jsonify, Response
from flask_jwt_extended import verify_jwt_in_request
from app import chat_model


chat_bp = Blueprint("chat", __name__)

@chat_bp.before_request
def protected():
    verify_jwt_in_request()

@chat_bp.route("/chat", methods=["POST"])
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

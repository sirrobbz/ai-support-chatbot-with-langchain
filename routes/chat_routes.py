from flask import Blueprint, request, jsonify
from services.rag_service import build_rag_chain

chat_bp = Blueprint("chat", __name__)

_chain = None

def get_chain():
    global _chain
    if _chain is None:
        _chain = build_rag_chain()
    return _chain

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json

    message = data.get("message")
    session_id = data.get("session_id", "default")

    if not message:
        return jsonify({"error": "message required"}), 400

    try:
        chain = get_chain()
    except Exception as e:
        return jsonify({"error": f"Chain initialization failed: {str(e)}"}), 500

    response = chain.invoke(
        {"input": message},
        config={"configurable": {"session_id": session_id}}
    )

    print("DEBUG response type:", type(response))
    print("DEBUG response value:", response)

    # Handle both AIMessage and plain string outputs
    if hasattr(response, "content"):
        answer = response.content
    elif isinstance(response, str):
        answer = response
    elif isinstance(response, dict):
        answer = response.get("output") or response.get("answer") or response.get("text") or str(response)
    else:
        answer = str(response)

    return jsonify({
        "response": answer,
        "session_id": session_id
    })

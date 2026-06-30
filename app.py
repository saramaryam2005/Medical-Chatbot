import os
from flask import Flask, render_template, request, jsonify

from src.chatbot import get_response

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chat():

    try:
        user_message = request.form["msg"]

        result = get_response(user_message)

        return jsonify({
            "answer": result["answer"],
            "sources": result["sources"]
        })

    except Exception as e:
        print("ERROR:", str(e))

        return jsonify({
            "answer": f"Error: {str(e)}",
            "sources": []
        })
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
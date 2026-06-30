from flask import Flask, render_template, request, jsonify

from src.chatbot import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chat():

    user_message = request.form["msg"]

    result = get_response(user_message)

    return jsonify({
    "answer": result["answer"],
    "sources": result["sources"]
})


if __name__ == "__main__":
    app.run(debug=True)

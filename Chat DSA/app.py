from flask import Flask, render_template, request, jsonify
from chatbot import get_bot_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message")
    response = get_bot_response(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
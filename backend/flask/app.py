from atexit import register

from core import QA
from flask import Flask, abort, jsonify, request
from flask_cors import CORS


qa = QA()
register(qa.close)

app = Flask(__name__)
CORS(app)


@app.route("/q/<question>", methods=['GET', 'POST'])
def get_answer(question):

    if not question:
        abort(jsonify({"error": "问题不能为空"}), 400)

    return {"answer": qa.answer(question)}


@app.route("/q", methods=['POST'])
def get_ans():
    # data format = {q: "question"}
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        # 在这里处理接收到的JSON数据
        question = data.get('q')
    else:
        data = request.form
        # 在这里处理接收到的表单数据
        question = data.get('q')

    if not question:
        abort(jsonify({"error": "问题不能为空"}), 400)

    return {"answer": qa.answer(question)}


if __name__ == '__main__':
    app.run(port=8888)  # 指定端口号为 8000

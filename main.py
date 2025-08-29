from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 内存保存剪切板内容
clipboard_content = {"text": ""}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_content():
    return jsonify(clipboard_content)

@app.route("/set", methods=["POST"])
def set_content():
    data = request.json
    clipboard_content["text"] = data.get("text", "")
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, render_template, request, jsonify, send_file
import io

app = Flask(__name__)

# 内存中保存数据
clipboard_content = {"text": ""}
uploaded_file = {"data": None, "filename": "", "content_type": ""}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_content():
    # 返回文本和文件是否存在
    return jsonify({
        "text": clipboard_content["text"],
        "has_file": uploaded_file["data"] is not None
    })

@app.route("/set", methods=["POST"])
def set_content():
    data = request.json
    clipboard_content["text"] = data.get("text", "")
    return jsonify(success=True)

# --- 新增：文件上传接口 ---
@app.route("/upload", methods=["POST"])
def upload_file():
    global uploaded_file
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            # 将文件读入内存
            uploaded_file["data"] = file.read()
            uploaded_file["filename"] = file.filename
            uploaded_file["content_type"] = file.content_type
            return jsonify(success=True, filename=file.filename)
    return jsonify(success=False, error="No file selected")

# --- 新增：文件下载接口 ---
@app.route("/download")
def download_file():
    global uploaded_file
    if uploaded_file["data"] is not None:
        # 使用 BytesIO 将内存数据包装成文件流
        return send_file(
            io.BytesIO(uploaded_file["data"]),
            as_attachment=True,
            download_name=uploaded_file["filename"],
            mimetype=uploaded_file["content_type"]
        )
    return "No file to download", 404

# --- 新增：清除数据接口 ---
@app.route("/clear", methods=["POST"])
def clear_content():
    global clipboard_content, uploaded_file
    clipboard_content["text"] = ""
    uploaded_file = {"data": None, "filename": "", "content_type": ""}
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# app.py
import os
import json
from flask import Flask, render_template, request, jsonify, abort, send_from_directory
import markdown
from pathlib import Path
import sys

app = Flask(__name__)
# Read BASE_DIR from the startup command argument if provided, otherwise use the default directory.
BASE_DIR = Path(os.path.expanduser(sys.argv[1])) if len(sys.argv) > 1 else Path(__file__).parent
USERDATA_DIR = Path(__file__).parent / "userdata"
USERDATA_DIR.mkdir(exist_ok=True)
FAV_FILE = USERDATA_DIR / "favorites.json"

# 初始化收藏文件
if not FAV_FILE.exists():
    with open(FAV_FILE, "w") as f:
        json.dump([], f)

def is_safe_path(path):
    """验证路径是否在BASE_DIR下"""
    return True
    try:
        return os.path.commonpath([BASE_DIR, path]) == str(BASE_DIR)
    except:
        return False

def get_dir_tree(path):
    """获取指定路径的目录结构"""
    if not is_safe_path(path):
        return []
    
    items = []
    for item in Path(path).iterdir():
        if item.is_dir() or item.suffix == ".md":
            items.append({
                "name": item.name,
                "path": str(item.absolute()),
                "is_dir": item.is_dir(),
                "is_open": False  # 前端维护打开状态
            })
    return sorted(items, key=lambda x: (not x["is_dir"], x["name"]))

@app.route("/")
def index():
    # 将 BASE_DIR 作为模板变量传递
    return render_template("index.html", BASE_DIR=str(BASE_DIR))

@app.route("/api/get_children")
def get_children():
    """获取子目录内容"""
    path = request.args.get("path")
    assert path, "path参数不能为空"
    if "${BASE_DIR}" in path:
        path = path.replace("${BASE_DIR}", str(BASE_DIR))
    if not path or not is_safe_path(path):
        return jsonify([])
    return jsonify(get_dir_tree(path))

@app.route("/api/get_md")
def get_md():
    """获取Markdown内容"""
    path = request.args.get("path")
    assert path, "path参数不能为空"
    if not path or not is_safe_path(path) or not Path(path).is_file():
        abort(404)
    
    with open(path, "r", encoding="utf-8") as f:
        return markdown.markdown(f.read(), extensions=["extra"])

@app.route("/api/favorites", methods=["GET", "POST", "DELETE"])
def handle_favorites():
    """收藏操作"""
    if request.method == "GET":
        with open(FAV_FILE, "r") as f:
            return jsonify(json.load(f))
    
    data = request.get_json()
    if not data or "path" not in data or not is_safe_path(data["path"]):
        abort(400)
    
    with open(FAV_FILE, "r+") as f:
        favorites = json.load(f)
        if request.method == "POST":
            favorites.append({"path": data["path"], "note": data.get("note", "")})
        elif request.method == "DELETE":
            favorites = [fav for fav in favorites if fav["path"] != data["path"]]
        
        f.seek(0)
        json.dump(favorites, f)
        f.truncate()
    
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(port=8900, debug=True)
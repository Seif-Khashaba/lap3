from flask import Flask, request,jsonify

app = Flask(__name__)

TOKEN= "mysecrettoken"

todos = []  


@app.before_request

def authenticate_token():
    token = request.headers.get("Authorization")
    if not token or token !=  f"Bearer {TOKEN}":
        return jsonify({"error":"Unauthorized"}),401


@app.route("/todo", methods = ["GET"])
def get_todo():
    return jsonify(todos)

@app.route("/todo", methods =["POST"])
def Create_todo():
    title = request.json.get("title")
    if not title:
        return jsonify({"error": "No Title"}), 400
    todo ={
        "id": len(todos) + 1,
        "title": request.json.get("title"),
        "completed":request.json.get("completed", False)  
    }
    todos.append(todo)
    return jsonify(todo), 201

@app.route("/todo/<int:id>", methods = ["PUT"])
def update_todo(id):
    todo = next((t for t in todos if t["id"] == id ), None)
    if todo is None:
        return jsonify({"error": "todo not found"}), 404
    todo["title"] = request.json.get("completed",todo["completed"])
    return jsonify(todo)

@app.route("/todo/<int:id>", methods = ["DELETE"])
def delete_todo(id):
    global todos
    todos = [t for t in todos if t["id"] != id]
    return '', 204

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "resources not found"}), 404

app.run()
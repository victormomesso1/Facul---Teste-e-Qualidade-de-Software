from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random
import string

app = Flask(__name__)
CORS(app)

# "Banco" em memória (como no exemplo em Node)
users = [
    {
        "id": 1,
        "email": "teste@unisagrado.edu",
        "password": "123456",
        "name": "Usuário Teste"
    }
]

tasks = []
next_task_id = 1

# Sessões em memória: token -> userId
sessions = {}


def generate_token():
    """Gera um token simples só pro projeto."""
    rand = "".join(random.choices(string.ascii_letters + string.digits, k=16))
    return rand + str(int(datetime.utcnow().timestamp()))


def get_auth_token():
    """Extrai token do header Authorization: Bearer <token>"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    return auth_header[7:]


def require_auth():
    """Valida token e retorna o userId ou None."""
    token = get_auth_token()
    if not token:
        return None
    session = sessions.get(token)
    if not session:
        return None
    return session["userId"]


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "message": "API TaskManager rodando"})


# ---------- LOGIN ----------
@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "E-mail e senha são obrigatórios"}), 400

    user = next(
        (u for u in users if u["email"] == email and u["password"] == password),
        None,
    )
    if not user:
        return jsonify({"message": "E-mail ou senha inválidos"}), 401

    token = generate_token()
    sessions[token] = {"userId": user["id"]}

    return jsonify(
        {
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
            },
            "message": "Login realizado com sucesso",
        }
    )


# ---------- LOGOUT ----------
@app.post("/api/logout")
def logout():
    user_id = require_auth()
    if not user_id:
        return jsonify({"message": "Token inválido ou expirado"}), 401

    token = get_auth_token()
    if token in sessions:
        del sessions[token]

    return jsonify({"message": "Logout realizado com sucesso"})


# ---------- LISTAR TAREFAS ----------
@app.get("/api/tasks")
def list_tasks():
    user_id = require_auth()
    if not user_id:
        return jsonify({"message": "Token inválido ou expirado"}), 401

    status = request.args.get("status")
    user_tasks = [t for t in tasks if t["userId"] == user_id]

    if status and status != "Todas":
        user_tasks = [t for t in user_tasks if t["status"] == status]

    # Ordenar por createdAt desc
    user_tasks.sort(
        key=lambda t: t.get("createdAt") or "",
        reverse=True,
    )

    return jsonify(user_tasks)


# ---------- CRIAR TAREFA ----------
@app.post("/api/tasks")
def create_task():
    global next_task_id
    user_id = require_auth()
    if not user_id:
        return jsonify({"message": "Token inválido ou expirado"}), 401

    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    due_date = data.get("dueDate")

    if not title:
        return jsonify({"message": "Título é obrigatório"}), 400

    if len(title) > 100:
        return jsonify({"message": "Título deve ter no máximo 100 caracteres"}), 400

    # Limite de 100 tarefas pendentes por usuário
    pending_count = sum(
        1 for t in tasks if t["userId"] == user_id and t["status"] == "Pendente"
    )
    if pending_count >= 100:
        return jsonify({"message": "Limite máximo de tarefas ativas atingido"}), 400

    new_task = {
        "id": next_task_id,
        "userId": user_id,
        "title": title,
        "description": description,
        "dueDate": due_date,  # string yyyy-mm-dd ou None
        "status": "Pendente",
        "createdAt": datetime.utcnow().isoformat(),
    }
    next_task_id += 1
    tasks.append(new_task)

    return jsonify({"message": "Tarefa criada com sucesso", "task": new_task}), 201


# ---------- EDITAR TAREFA ----------
@app.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({"message": "Token inválido ou expirado"}), 401

    task = next((t for t in tasks if t["id"] == task_id and t["userId"] == user_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"message": "Título é obrigatório"}), 400
        if len(title) > 100:
            return jsonify({"message": "Título deve ter no máximo 100 caracteres"}), 400
        task["title"] = title

    if "description" in data:
        description = (data.get("description") or "").strip()
        task["description"] = description

    if "dueDate" in data:
        task["dueDate"] = data.get("dueDate")

    if "status" in data:
        status = data.get("status")
        if status not in ("Pendente", "Concluída"):
            return jsonify(
                {"message": "Status inválido. Use 'Pendente' ou 'Concluída'."}
            ), 400
        task["status"] = status

    return jsonify({"message": "Tarefa atualizada com sucesso", "task": task})


# ---------- MARCAR COMO CONCLUÍDA ----------
@app.post("/api/tasks/<int:task_id>/complete")
def complete_task(task_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({"message": "Token inválido ou expirado"}), 401

    task = next((t for t in tasks if t["id"] == task_id and t["userId"] == user_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    task["status"] = "Concluída"
    return jsonify({"message": "Tarefa concluída", "task": task})


# ---------- EXCLUIR TAREFA ----------
@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    user_id = require_auth()
    if not user_id:
        return jsonify({"message": "Token inválido ou expirado"}), 401

    global tasks
    original_len = len(tasks)
    tasks = [t for t in tasks if not (t["id"] == task_id and t["userId"] == user_id)]

    if len(tasks) == original_len:
        return jsonify({"message": "Tarefa não encontrada"}), 404

    return jsonify({"message": "Tarefa excluída com sucesso"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=False)

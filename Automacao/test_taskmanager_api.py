import requests

BASE_URL = "http://127.0.0.1:3000/api"  # mesma porta do Flask


def login(email: str, password: str) -> tuple[int, dict]:
    """Faz login na API e retorna (status_code, json)."""
    resp = requests.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password},
        timeout=5,
    )
    try:
        data = resp.json()
    except Exception:
        data = {}
    return resp.status_code, data


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# --------------------------
# 1) Login válido (CT-LOGIN-01)
# --------------------------
def test_login_valido():
    status, data = login("teste@unisagrado.edu", "123456")

    assert status == 200, "Login válido deve retornar HTTP 200"
    assert "token" in data, "Resposta deve conter token"
    assert data.get("user", {}).get("email") == "teste@unisagrado.edu"
    assert "Login realizado com sucesso" in data.get("message", "")


# --------------------------
# 2) Login inválido (CT-LOGIN-02)
# --------------------------
def test_login_invalido():
    status, data = login("teste@unisagrado.edu", "senha_errada")

    assert status == 401, "Login inválido deve retornar HTTP 401"
    assert "token" not in data, "Não deve retornar token em login inválido"
    assert "inválid" in data.get("message", "").lower()  # 'inválidos' ou 'inválido'


# --------------------------
# 3) Fluxo E2E via API (CT-E2E-01)
#    login -> criar tarefa -> listar -> concluir -> excluir -> logout
# --------------------------
def test_fluxo_e2e_completo():
    # 1. Login
    status, data = login("teste@unisagrado.edu", "123456")
    assert status == 200, "Login deve funcionar no fluxo E2E"
    token = data["token"]
    headers = auth_headers(token)

    # 2. Criar tarefa (CT-TASK-01)
    titulo = "Tarefa fluxo E2E"
    resp_create = requests.post(
        f"{BASE_URL}/tasks",
        json={"title": titulo, "description": "tarefa criada no teste E2E"},
        headers=headers,
        timeout=5,
    )
    assert resp_create.status_code == 201, "Criação de tarefa deve retornar 201"
    task = resp_create.json()["task"]
    task_id = task["id"]
    assert task["title"] == titulo
    assert task["status"] == "Pendente"

    # 3. Listar tarefas (RF04)
    resp_list = requests.get(
        f"{BASE_URL}/tasks",
        headers=headers,
        timeout=5,
    )
    assert resp_list.status_code == 200
    tasks_list = resp_list.json()
    assert any(t["id"] == task_id for t in tasks_list), "Tarefa criada deve aparecer na lista"

    # 4. Concluir tarefa (RF07)
    resp_complete = requests.post(
        f"{BASE_URL}/tasks/{task_id}/complete",
        headers=headers,
        timeout=5,
    )
    assert resp_complete.status_code == 200
    task_completed = resp_complete.json()["task"]
    assert task_completed["status"] == "Concluída"

    # 5. Excluir tarefa (RF06)
    resp_delete = requests.delete(
        f"{BASE_URL}/tasks/{task_id}",
        headers=headers,
        timeout=5,
    )
    assert resp_delete.status_code == 200

    # 6. Confirmar que não está mais na lista
    resp_list_after = requests.get(
        f"{BASE_URL}/tasks",
        headers=headers,
        timeout=5,
    )
    assert resp_list_after.status_code == 200
    tasks_list_after = resp_list_after.json()
    assert all(t["id"] != task_id for t in tasks_list_after), "Tarefa deve ter sido removida"

    # 7. Logout (RF02) – opcional na API
    resp_logout = requests.post(
        f"{BASE_URL}/logout",
        headers=headers,
        timeout=5,
    )
    assert resp_logout.status_code == 200

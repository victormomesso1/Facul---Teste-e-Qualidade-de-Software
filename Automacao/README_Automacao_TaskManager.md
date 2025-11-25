# Automação de Testes – TaskManager UNISAGRADO

Esta pasta contém os **scripts de automação** utilizados no Projeto Prático de Testes e Qualidade de Software para o sistema **TaskManager UNISAGRADO**.

A automação foi feita em **Python**, utilizando:

- [`pytest`](https://docs.pytest.org/) – framework de testes
- [`requests`](https://requests.readthedocs.io/) – consumo da API Flask

O objetivo desta automação é:
- Validar automaticamente casos de teste críticos (login e fluxo E2E);
- Apoiar a regressão após correções;
- Servir como evidência prática dos conceitos de testes e automação utilizados no projeto.

---

## Estrutura da pasta

```text
Automacao/
  test_taskmanager_api.py   # testes automatizados de API (pytest)
```

> As evidências (prints) da execução dos testes devem ser salvas fora desta pasta, em `evidencias/`, conforme orientações do projeto.

---

## Pré-requisitos

- Python 3 instalado (foi utilizado Python 3.13)
- Dependências da automação:

```bash
pip install pytest requests
```

> Observação: o `pytest` pode ficar fora do PATH no Windows. Neste README usamos o formato `python -m pytest` para evitar esse problema.

---

## Como executar o sistema antes da automação

1. Abrir um terminal / Prompt de Comando.
2. Ir até a pasta raiz do projeto():

3. Iniciar a API Flask (back-end):

   ```bash
   python app.py
   ```

   A API deve ficar disponível em:

   ```
   http://127.0.0.1:3000/api
   ```

4. Deixar essa janela aberta enquanto os testes automatizados forem executados.

---

## Como executar os testes automatizados

Em outro terminal:

1. Ir até a pasta de automação:

   ```bash
   cd C:\Users\victor\Downloads\projeto-taskmanager\Automacao
   ```

2. (Somente na primeira vez) instalar as dependências:

   ```bash
   pip install pytest requests
   ```

3. Executar os testes via `pytest`:

   ```bash
   python -m pytest -v test_taskmanager_api.py
   ```

Se tudo estiver correto, o resultado esperado é semelhante a:

```text
test_taskmanager_api.py::test_login_valido PASSED
test_taskmanager_api.py::test_login_invalido PASSED
test_taskmanager_api.py::test_fluxo_e2e_completo PASSED

======================== 3 passed in X.XXs ========================
```

Este print de saída deve ser salvo na pasta `evidencias/` como prova de execução da automação.

---

## Descrição dos testes automatizados

Arquivo: `test_taskmanager_api.py`  
Base da API utilizada nos testes:

```python
BASE_URL = "http://127.0.0.1:3000/api"
```

### 1. `test_login_valido`

- **Casos de teste relacionados:** `CT-LOGIN-01`
- **Requisitos cobertos:** `RF01` (Login), `RF10` (Mensagens de feedback)
- **Objetivo:** validar login com credenciais válidas.
- **Verificações principais:**
  - HTTP 200
  - presença de `token`
  - dados do usuário retornados corretamente
  - mensagem: “Login realizado com sucesso”

---

### 2. `test_login_invalido`

- **Casos de teste relacionados:** `CT-LOGIN-02`
- **Requisitos cobertos:** `RF01` (Login), `RF10` (Mensagens de feedback)
- **Objetivo:** validar comportamento do sistema quando a senha está incorreta.
- **Verificações principais:**
  - HTTP 401
  - não retorna `token`
  - mensagem de erro informando credenciais inválidas

---

### 3. `test_fluxo_e2e_completo`

- **Casos de teste relacionados:** `CT-E2E-01`
- **Requisitos cobertos:**  
  `RF01` (Login), `RF03` (Cadastro de tarefa), `RF04` (Listagem),  
  `RF07` (Concluir tarefa), `RF06` (Exclusão), `RF02` (Logout), `RF10` (feedback).
- **Objetivo:** validar o fluxo principal completo via API:
  1. Login com usuário válido;
  2. Criação de uma nova tarefa;
  3. Listagem das tarefas e verificação da tarefa criada;
  4. Marcação da tarefa como concluída;
  5. Exclusão da tarefa;
  6. Confirmação de que a tarefa não aparece mais na lista;
  7. Logout.

---

## Relação com o Projeto Acadêmico

Esta automação atende ao item:

> **“Automatizar pelo menos 3 testes: Login válido/inválido; Fluxo principal completo (E2E); API (com Postman/Newman ou equivalente)”**

Neste projeto, a API é exercitada por **scripts Python com `requests` + `pytest`**, que funcionam como alternativa a Postman/Newman.

Na documentação do projeto (relatórios e matriz de rastreabilidade), estes testes devem ser vinculados aos casos de teste pelos IDs:

- `CT-LOGIN-01` → `test_login_valido`
- `CT-LOGIN-02` → `test_login_invalido`
- `CT-E2E-01` → `test_fluxo_e2e_completo`

---

## Evidências recomendadas

Para compor o artefato de **evidências (prints/vídeos)**, recomenda-se salvar na pasta `evidencias/`:

- Print da execução de `python -m pytest -v test_taskmanager_api.py`, com todos os testes `PASSED`  
  - Ex.: `CT-LOGIN-01_02_CT-E2E-01_AUTOMACAO_OK.png`
- Prints adicionais, se desejado, mostrando:
  - Falha proposital em algum teste (para ilustrar detecção de defeito);
  - Tela da aplicação correspondente (por exemplo, login de sucesso/erro).

---

## Observações

- Se a porta ou URL da API forem alteradas no futuro, é necessário atualizar a constante `BASE_URL` em `test_taskmanager_api.py`.
- Os testes assumem a existência do usuário padrão:
  - **E-mail:** `teste@unisagrado.edu`  
  - **Senha:** `123456`  
  conforme definido no `app.py`.

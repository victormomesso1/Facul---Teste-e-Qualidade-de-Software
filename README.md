# Facul---Teste-e-Qualidade-de-Software
repositório do trabalho de testes e qualidade de software
# TaskManager UNISAGRADO – Projeto Prático de Testes e Qualidade de Software

Sistema simples de **gerenciamento de tarefas acadêmicas** utilizado como base para o Projeto Prático da disciplina de **Testes e Qualidade de Software**.

O foco deste projeto é **testar** o sistema (funcional, não funcional, automação, TDD, etc.), mas o código do sistema também foi desenvolvido pelo grupo.

---

## 1. Visão Geral do Sistema

**Nome:** TaskManager UNISAGRADO  
**Tipo:** Aplicação web (front-end + API back-end em Python/Flask)

### Funcionalidades principais

- Login e logout de usuário.
- Cadastro de tarefas:
  - Título (obrigatório, até 100 caracteres).
  - Descrição (opcional).
  - Data de vencimento (opcional).
- Listagem de tarefas do usuário logado.
- Edição de tarefas existentes.
- Exclusão de tarefas com confirmação.
- Marcação de tarefas como concluídas, com destaque visual.
- Filtro de tarefas por status (Todas, Pendentes, Concluídas).
- Regras de validação:
  - Título obrigatório.
  - Título com no máximo 100 caracteres.
  - Limite de 100 tarefas ativas (pendentes) por usuário.

---

## 2. Tecnologias Utilizadas

- **Back-end:** Python 3 + Flask (API REST, armazenamento em memória)
- **Front-end:** HTML, CSS, JavaScript (consumindo a API via `fetch`)
- **Automação de testes de API:** Python + `pytest` + `requests`
- **Ferramentas de apoio:** Navegador (Chrome/Firefox), terminal/Prompt de Comando

---

## 3. Estrutura de Pastas (simplificada)

```text
projeto-taskmanager/
  app.py                     # API Flask (back-end)
  index.html                 # Interface web (front-end)

  Automacao/
    test_taskmanager_api.py  # testes automatizados de API (pytest)
    README.md                # guia da automação

  Plano de Teste/ 
    Plano_de_Teste.docx/pdf
  Casos de teste + matriz de rastreabilidade
    Casos_de_Teste.xlsx
    Matriz_de_Rastreabilidade.xlsx
  RELATORIO_FINAL 
    Relatorio_Final.docx/pdf

  evidencias/
    (prints e vídeos de execução de testes, automação, TDD, etc.)
```

---

## 4. Pré-requisitos

- **Python 3.x** instalado (foi utilizado Python 3.13)
- Navegador (Chrome, Firefox ou equivalente)
- Opcional (para automação):  
  - `pytest`  
  - `requests`  

Instalação básica das dependências de automação:

```bash
pip install pytest requests
```

---

## 5. Como Executar o Back-end (API Flask)

1. Abrir um **Prompt de Comando/Terminal**.

2. Navegar até a pasta do projeto:

   ```bash
   cd C:\Users\victor\Downloads\projeto-taskmanager
   ```

3. Executar a API Flask:

   ```bash
   python app.py
   ```

4. Se tudo estiver correto, aparecerá algo como:

   ```text
   * Running on http://127.0.0.1:3000
   ```

5. A API ficará disponível em:

   - `http://127.0.0.1:3000/api`

> Deixe essa janela aberta enquanto for usar o sistema ou rodar os testes automatizados.

---

## 6. Como Executar o Front-end

O front-end é uma página HTML simples que consome a API Flask.

1. Com o back-end já rodando, abra o arquivo `index.html` no navegador:
   - Clique duas vezes no `index.html`, ou  
   - Clique com o botão direito → **Abrir com** → Chrome/Firefox.

2. Use o sistema normalmente:
   - Tela de login,
   - Lista de tarefas,
   - Nova tarefa,
   - Edição, exclusão, conclusão, etc.

Usuário de teste padrão configurado no `app.py`:

- **E-mail:** `teste@unisagrado.edu`  
- **Senha:** `123456`

---

## 7. Como Executar a Automação de Testes (API)

Os scripts de automação estão na pasta `Automacao/`.  
Para detalhes mais completos, consulte o `Automacao/README.md`.  

### Resumo de execução

1. Em um terminal separado, ir até a pasta `Automacao`:

   ```bash
   cd C:\Users\victor\Downloads\projeto-taskmanager\Automacao
   ```

2. (Somente na primeira vez) instalar dependências:

   ```bash
   pip install pytest requests
   ```

3. Com a API ainda rodando em outro terminal, executar:

   ```bash
   python -m pytest -v test_taskmanager_api.py
   ```

4. Os testes automatizados cobrem:
   - Login válido,
   - Login inválido,
   - Fluxo principal E2E via API (login → criar tarefa → listar → concluir → excluir → logout).

---

## 8. Testes, Documentação e Evidências

Além do código, o projeto inclui artefatos de teste, tais como:

- **Plano de Teste** (DOCX/PDF)
- **Casos de Teste** e **Matriz de Rastreabilidade** (planilhas)
- **Relatório Final de Testes**
- **Evidências** (prints e/ou vídeos), por exemplo:
  - Execução dos testes automatizados (`pytest`).
  - Telas do sistema em cenários de sucesso e erro.
  - Exemplos de TDD (teste falhando → depois passando).

Esses artefatos podem estar organizados em subpastas como `docs/` e `evidencias/`.

---

## 9. Integrantes do Grupo

- Victor Dionisio Momesso  
- Fausto Renato  
- Theo Rondon  
- Kevin Lopes  
- Pedro Rocha

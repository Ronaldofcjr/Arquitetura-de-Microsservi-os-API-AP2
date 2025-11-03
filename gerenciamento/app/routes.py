from flask import Blueprint, request, jsonify
from app.models import db, Aluno, Professor, Turma

gerenciamento_bp = Blueprint('gerenciamento', __name__)

# === CRUD ALUNO ===
@gerenciamento_bp.route('/alunos', methods=['POST'])
def criar_aluno():
    """
    Criar um novo aluno
    ---
    tags:
      - Alunos
    description: Cadastra um novo aluno no sistema de gerenciamento.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              example: "João da Silva"
    responses:
      201:
        description: Aluno criado com sucesso
        examples:
          application/json: {"id": 1, "nome": "João da Silva"}
    """
    data = request.get_json()
    aluno = Aluno(nome=data['nome'])
    db.session.add(aluno)
    db.session.commit()
    return jsonify({'id': aluno.id, 'nome': aluno.nome}), 201

@gerenciamento_bp.route('/alunos', methods=['GET'])
def listar_alunos():
    """
    Listar todos os alunos
    ---
    tags:
      - Alunos
    description: Retorna uma lista de todos os alunos cadastrados.
    responses:
      200:
        description: Lista de alunos
        examples:
          application/json: [
            {"id": 1, "nome": "Maria"},
            {"id": 2, "nome": "João"}
          ]
    """
    alunos = Aluno.query.all()
    return jsonify([{'id': a.id, 'nome': a.nome} for a in alunos])

# === CRUD PROFESSOR ===
@gerenciamento_bp.route('/professores', methods=['POST'])
def criar_professor():
    """
    Criar um novo professor
    ---
    tags:
      - Professores
    description: Cadastra um novo professor no sistema.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Carlos Pereira"
    responses:
      201:
        description: Professor criado
        examples:
          application/json: {"id": 1, "nome": "Carlos Pereira"}
    """
    data = request.get_json()
    prof = Professor(nome=data['nome'])
    db.session.add(prof)
    db.session.commit()
    return jsonify({'id': prof.id, 'nome': prof.nome}), 201

@gerenciamento_bp.route('/professores/<int:id>', methods=['GET'])
def obter_professor(id):
    """
    Obter um professor por ID
    ---
    tags:
      - Professores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do professor
        example: 1
    responses:
      200:
        description: Dados do professor
        examples:
          application/json: {"id": 1, "nome": "Carlos Pereira"}
      404:
        description: Professor não encontrado
    """
    prof = Professor.query.get(id)
    if not prof:
        return jsonify({'erro': 'Professor não encontrado'}), 404
    return jsonify({'id': prof.id, 'nome': prof.nome})

# === CRUD TURMA ===
@gerenciamento_bp.route('/turmas', methods=['POST'])
def criar_turma():
    """
    Criar uma nova turma
    ---
    tags:
      - Turmas
    description: Cadastra uma nova turma no sistema.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Turma de Matemática A"
    responses:
      201:
        description: Turma criada
        examples:
          application/json: {"id": 1, "nome": "Turma de Matemática A"}
    """
    data = request.get_json()
    turma = Turma(nome=data['nome'])
    db.session.add(turma)
    db.session.commit()
    return jsonify({'id': turma.id, 'nome': turma.nome}), 201

@gerenciamento_bp.route('/turmas/<int:id>', methods=['GET'])
def obter_turma(id):
    """
    Obter turma por ID
    ---
    tags:
      - Turmas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da turma
        example: 1
    responses:
      200:
        description: Dados da turma
        examples:
          application/json: {"id": 1, "nome": "Turma de Matemática A"}
      404:
        description: Turma não encontrada
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'erro': 'Turma não encontrada'}), 404
    return jsonify({'id': turma.id, 'nome': turma.nome})

from flask import Blueprint, request, jsonify
from app.models import db, Aluno, Professor, Turma
from datetime import datetime

gerenciamento_bp = Blueprint('gerenciamento', __name__)

# Helper para converter objeto para dicionário
def to_dict(obj):
    if obj is None:
        return None
    d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    if 'data_nascimento' in d and d['data_nascimento']:
        d['data_nascimento'] = d['data_nascimento'].isoformat()
    return d

# === CRUD PROFESSOR ===
@gerenciamento_bp.route('/professores', methods=['POST'])
def criar_professor():
    """
    Criar um novo professor
    ---
    tags:
      - Professores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [nome]
          properties:
            nome: { type: string, example: "Dr. House" }
            idade: { type: integer, example: 50 }
            materia: { type: string, example: "Diagnóstico" }
            observacoes: { type: string, example: "Especialista em doenças infecciosas" }
    responses:
      201: { description: "Professor criado" }
    """
    data = request.get_json()
    prof = Professor(
        nome=data['nome'],
        idade=data.get('idade'),
        materia=data.get('materia'),
        observacoes=data.get('observacoes')
    )
    db.session.add(prof)
    db.session.commit()
    return jsonify(to_dict(prof)), 201

@gerenciamento_bp.route('/professores', methods=['GET'])
def listar_professores():
    """
    Listar todos os professores
    ---
    tags: [Professores]
    responses:
      200: { description: "Lista de professores" }
    """
    professores = [to_dict(p) for p in Professor.query.all()]
    return jsonify(professores)

@gerenciamento_bp.route('/professores/<int:id>', methods=['GET'])
def obter_professor(id):
    """
    Obter um professor por ID
    ---
    tags: [Professores]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Dados do professor" }
      404: { description: "Professor não encontrado" }
    """
    prof = Professor.query.get(id)
    if not prof:
        return jsonify({'erro': 'Professor não encontrado'}), 404
    return jsonify(to_dict(prof))

@gerenciamento_bp.route('/professores/<int:id>', methods=['PUT'])
def atualizar_professor(id):
    """
    Atualizar um professor
    ---
    tags: [Professores]
    parameters:
      - { name: id, in: path, type: integer, required: true }
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome: { type: string }
            idade: { type: integer }
            materia: { type: string }
            observacoes: { type: string }
    responses:
      200: { description: "Professor atualizado" }
      404: { description: "Professor não encontrado" }
    """
    prof = Professor.query.get(id)
    if not prof:
        return jsonify({'erro': 'Professor não encontrado'}), 404
    data = request.get_json()
    prof.nome = data.get('nome', prof.nome)
    prof.idade = data.get('idade', prof.idade)
    prof.materia = data.get('materia', prof.materia)
    prof.observacoes = data.get('observacoes', prof.observacoes)
    db.session.commit()
    return jsonify(to_dict(prof))

@gerenciamento_bp.route('/professores/<int:id>', methods=['DELETE'])
def deletar_professor(id):
    """
    Deletar um professor
    ---
    tags: [Professores]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Professor deletado" }
      404: { description: "Professor não encontrado" }
    """
    prof = Professor.query.get(id)
    if not prof:
        return jsonify({'erro': 'Professor não encontrado'}), 404
    db.session.delete(prof)
    db.session.commit()
    return jsonify({'mensagem': 'Professor deletado com sucesso'})

# === CRUD TURMA ===
@gerenciamento_bp.route('/turmas', methods=['POST'])
def criar_turma():
    """
    Criar uma nova turma
    ---
    tags: [Turmas]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [descricao, professor_id]
          properties:
            descricao: { type: string, example: "Turma de Cálculo I" }
            professor_id: { type: integer, example: 1 }
            ativo: { type: boolean, example: true }
    responses:
      201: { description: "Turma criada" }
      404: { description: "Professor não encontrado" }
    """
    data = request.get_json()
    if not Professor.query.get(data['professor_id']):
        return jsonify({'erro': 'Professor não encontrado'}), 404
    turma = Turma(
        descricao=data['descricao'],
        professor_id=data['professor_id'],
        ativo=data.get('ativo', True)
    )
    db.session.add(turma)
    db.session.commit()
    return jsonify(to_dict(turma)), 201

@gerenciamento_bp.route('/turmas', methods=['GET'])
def listar_turmas():
    """
    Listar todas as turmas
    ---
    tags: [Turmas]
    responses:
      200: { description: "Lista de turmas" }
    """
    turmas = [to_dict(t) for t in Turma.query.all()]
    return jsonify(turmas)

@gerenciamento_bp.route('/turmas/<int:id>', methods=['GET'])
def obter_turma(id):
    """
    Obter turma por ID
    ---
    tags: [Turmas]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Dados da turma" }
      404: { description: "Turma não encontrada" }
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'erro': 'Turma não encontrada'}), 404
    return jsonify(to_dict(turma))

@gerenciamento_bp.route('/turmas/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    """
    Atualizar uma turma
    ---
    tags: [Turmas]
    parameters:
      - { name: id, in: path, type: integer, required: true }
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            descricao: { type: string }
            professor_id: { type: integer }
            ativo: { type: boolean }
    responses:
      200: { description: "Turma atualizada" }
      404: { description: "Turma ou Professor não encontrado" }
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'erro': 'Turma não encontrada'}), 404
    data = request.get_json()
    if 'professor_id' in data and not Professor.query.get(data['professor_id']):
        return jsonify({'erro': 'Professor não encontrado'}), 404
    turma.descricao = data.get('descricao', turma.descricao)
    turma.professor_id = data.get('professor_id', turma.professor_id)
    turma.ativo = data.get('ativo', turma.ativo)
    db.session.commit()
    return jsonify(to_dict(turma))

@gerenciamento_bp.route('/turmas/<int:id>', methods=['DELETE'])
def deletar_turma(id):
    """
    Deletar uma turma
    ---
    tags: [Turmas]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Turma deletada" }
      404: { description: "Turma não encontrada" }
    """
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'erro': 'Turma não encontrada'}), 404
    db.session.delete(turma)
    db.session.commit()
    return jsonify({'mensagem': 'Turma deletada com sucesso'})

# === CRUD ALUNO ===
@gerenciamento_bp.route('/alunos', methods=['POST'])
def criar_aluno():
    """
    Criar um novo aluno
    ---
    tags: [Alunos]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [nome, turma_id]
          properties:
            nome: { type: string, example: "John Doe" }
            idade: { type: integer, example: 20 }
            turma_id: { type: integer, example: 1 }
            data_nascimento: { type: string, format: date, example: "2004-01-15" }
            nota_primeiro_semestre: { type: number, format: float, example: 8.5 }
            nota_segundo_semestre: { type: number, format: float, example: 9.0 }
    responses:
      201: { description: "Aluno criado" }
      404: { description: "Turma não encontrada" }
    """
    data = request.get_json()
    if not Turma.query.get(data['turma_id']):
        return jsonify({'erro': 'Turma não encontrada'}), 404
    
    n1 = data.get('nota_primeiro_semestre')
    n2 = data.get('nota_segundo_semestre')
    media = (n1 + n2) / 2 if n1 is not None and n2 is not None else None

    aluno = Aluno(
        nome=data['nome'],
        idade=data.get('idade'),
        turma_id=data['turma_id'],
        data_nascimento=datetime.fromisoformat(data['data_nascimento']).date() if data.get('data_nascimento') else None,
        nota_primeiro_semestre=n1,
        nota_segundo_semestre=n2,
        media_final=media
    )
    db.session.add(aluno)
    db.session.commit()
    return jsonify(to_dict(aluno)), 201

@gerenciamento_bp.route('/alunos', methods=['GET'])
def listar_alunos():
    """
    Listar todos os alunos
    ---
    tags: [Alunos]
    responses:
      200: { description: "Lista de alunos" }
    """
    alunos = [to_dict(a) for a in Aluno.query.all()]
    return jsonify(alunos)

@gerenciamento_bp.route('/alunos/<int:id>', methods=['GET'])
def obter_aluno(id):
    """
    Obter um aluno por ID
    ---
    tags: [Alunos]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Dados do aluno" }
      404: { description: "Aluno não encontrado" }
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'erro': 'Aluno não encontrado'}), 404
    return jsonify(to_dict(aluno))

@gerenciamento_bp.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    """
    Atualizar um aluno
    ---
    tags: [Alunos]
    parameters:
      - { name: id, in: path, type: integer, required: true }
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome: { type: string }
            idade: { type: integer }
            turma_id: { type: integer }
            data_nascimento: { type: string, format: date }
            nota_primeiro_semestre: { type: number, format: float }
            nota_segundo_semestre: { type: number, format: float }
    responses:
      200: { description: "Aluno atualizado" }
      404: { description: "Aluno ou Turma não encontrado" }
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'erro': 'Aluno não encontrado'}), 404
    data = request.get_json()
    if 'turma_id' in data and not Turma.query.get(data['turma_id']):
        return jsonify({'erro': 'Turma não encontrada'}), 404

    aluno.nome = data.get('nome', aluno.nome)
    aluno.idade = data.get('idade', aluno.idade)
    aluno.turma_id = data.get('turma_id', aluno.turma_id)
    if 'data_nascimento' in data:
        aluno.data_nascimento = datetime.fromisoformat(data['data_nascimento']).date() if data.get('data_nascimento') else None
    
    n1 = data.get('nota_primeiro_semestre', aluno.nota_primeiro_semestre)
    n2 = data.get('nota_segundo_semestre', aluno.nota_segundo_semestre)
    aluno.nota_primeiro_semestre = n1
    aluno.nota_segundo_semestre = n2
    aluno.media_final = (n1 + n2) / 2 if n1 is not None and n2 is not None else aluno.media_final

    db.session.commit()
    return jsonify(to_dict(aluno))

@gerenciamento_bp.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    """
    Deletar um aluno
    ---
    tags: [Alunos]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Aluno deletado" }
      404: { description: "Aluno não encontrado" }
    """
    aluno = Aluno.query.get(id)
    if not aluno:
        return jsonify({'erro': 'Aluno não encontrado'}), 404
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'mensagem': 'Aluno deletado com sucesso'})

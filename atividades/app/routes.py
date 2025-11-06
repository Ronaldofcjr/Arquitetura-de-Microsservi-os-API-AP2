from flask import Blueprint, request, jsonify
from app.models import db, Atividade, Nota
import requests, os
from datetime import datetime

atividades_bp = Blueprint('atividades', __name__)
GERENCIAMENTO_URL = os.getenv('GERENCIAMENTO_URL', 'http://gerenciamento:5000')

# Helper to convert model objects to dictionary
def to_dict(obj):
    if obj is None:
        return None
    d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    if 'data_entrega' in d and d['data_entrega']:
        d['data_entrega'] = d['data_entrega'].isoformat()
    return d

# === CRUD ATIVIDADE ===

@atividades_bp.route('/atividades', methods=['POST'])
def criar_atividade():
    """
    Criar uma nova atividade
    ---
    tags: [Atividades]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [nome_atividade, descricao, peso_projeto, data_entrega, turma_id, professor_id]
          properties:
            nome_atividade: { type: string, example: "Trabalho 1" }
            descricao: { type: string, example: "Descrição do Trabalho 1" }
            peso_projeto: { type: number, format: float, example: 0.25 }
            data_entrega: { type: string, format: date, example: "2025-12-01" }
            turma_id: { type: integer, example: 1 }
            professor_id: { type: integer, example: 1 }
    responses:
      201: { description: "Atividade criada" }
      404: { description: "Professor ou Turma não encontrado" }
    """
    data = request.get_json()
    
    # Validate professor and turma exist in Gerenciamento
    p_resp = requests.get(f"{GERENCIAMENTO_URL}/professores/{data['professor_id']}")
    t_resp = requests.get(f"{GERENCIAMENTO_URL}/turmas/{data['turma_id']}")
    if p_resp.status_code != 200 or t_resp.status_code != 200:
        return jsonify({'erro': 'Professor ou Turma não encontrado'}), 404

    atividade = Atividade(
        nome_atividade=data['nome_atividade'],
        descricao=data['descricao'],
        peso_projeto=data['peso_projeto'],
        data_entrega=datetime.fromisoformat(data['data_entrega']).date(),
        turma_id=data['turma_id'],
        professor_id=data['professor_id']
    )
    db.session.add(atividade)
    db.session.commit()
    return jsonify(to_dict(atividade)), 201

@atividades_bp.route('/atividades', methods=['GET'])
def listar_atividades():
    """
    Listar todas as atividades
    ---
    tags: [Atividades]
    responses:
      200: { description: "Lista de atividades" }
    """
    atividades = [to_dict(a) for a in Atividade.query.all()]
    return jsonify(atividades)

@atividades_bp.route('/atividades/<int:id>', methods=['GET'])
def obter_atividade(id):
    """
    Obter uma atividade por ID
    ---
    tags: [Atividades]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Dados da atividade" }
      404: { description: "Atividade não encontrada" }
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    return jsonify(to_dict(atividade))

@atividades_bp.route('/atividades/<int:id>', methods=['PUT'])
def atualizar_atividade(id):
    """
    Atualizar uma atividade
    ---
    tags: [Atividades]
    parameters:
      - { name: id, in: path, type: integer, required: true }
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome_atividade: { type: string }
            descricao: { type: string }
            peso_projeto: { type: number, format: float }
            data_entrega: { type: string, format: date }
            turma_id: { type: integer }
            professor_id: { type: integer }
    responses:
      200: { description: "Atividade atualizada" }
      404: { description: "Atividade, Professor ou Turma não encontrado" }
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    data = request.get_json()

    if 'professor_id' in data:
        p_resp = requests.get(f"{GERENCIAMENTO_URL}/professores/{data['professor_id']}")
        if p_resp.status_code != 200:
            return jsonify({'erro': 'Professor não encontrado'}), 404
        atividade.professor_id = data['professor_id']
    
    if 'turma_id' in data:
        t_resp = requests.get(f"{GERENCIAMENTO_URL}/turmas/{data['turma_id']}")
        if t_resp.status_code != 200:
            return jsonify({'erro': 'Turma não encontrada'}), 404
        atividade.turma_id = data['turma_id']

    atividade.nome_atividade = data.get('nome_atividade', atividade.nome_atividade)
    atividade.descricao = data.get('descricao', atividade.descricao)
    atividade.peso_projeto = data.get('peso_projeto', atividade.peso_projeto)
    if 'data_entrega' in data:
        atividade.data_entrega = datetime.fromisoformat(data['data_entrega']).date()

    db.session.commit()
    return jsonify(to_dict(atividade))

@atividades_bp.route('/atividades/<int:id>', methods=['DELETE'])
def deletar_atividade(id):
    """
    Deletar uma atividade
    ---
    tags: [Atividades]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Atividade deletada" }
      404: { description: "Atividade não encontrada" }
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    db.session.delete(atividade)
    db.session.commit()
    return jsonify({'mensagem': 'Atividade deletada com sucesso'})

# === CRUD NOTA ===

@atividades_bp.route('/notas', methods=['POST'])
def criar_nota():
    """
    Criar uma nova nota
    ---
    tags: [Notas]
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [nota, aluno_id, atividade_id]
          properties:
            nota: { type: number, format: float, example: 8.5 }
            aluno_id: { type: integer, example: 1 }
            atividade_id: { type: integer, example: 1 }
    responses:
      201: { description: "Nota criada" }
      404: { description: "Aluno ou Atividade não encontrado" }
    """
    data = request.get_json()

    # Validate aluno exists in Gerenciamento
    a_resp = requests.get(f"{GERENCIAMENTO_URL}/alunos/{data['aluno_id']}")
    if a_resp.status_code != 200:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

    # Validate atividade exists
    if not Atividade.query.get(data['atividade_id']):
        return jsonify({'erro': 'Atividade não encontrada'}), 404

    nota = Nota(
        nota=data['nota'],
        aluno_id=data['aluno_id'],
        atividade_id=data['atividade_id']
    )
    db.session.add(nota)
    db.session.commit()
    return jsonify(to_dict(nota)), 201

@atividades_bp.route('/notas', methods=['GET'])
def listar_notas():
    """
    Listar todas as notas
    ---
    tags: [Notas]
    responses:
      200: { description: "Lista de notas" }
    """
    notas = [to_dict(n) for n in Nota.query.all()]
    return jsonify(notas)

@atividades_bp.route('/notas/<int:id>', methods=['GET'])
def obter_nota(id):
    """
    Obter uma nota por ID
    ---
    tags: [Notas]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Dados da nota" }
      404: { description: "Nota não encontrada" }
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({'erro': 'Nota não encontrada'}), 404
    return jsonify(to_dict(nota))

@atividades_bp.route('/notas/<int:id>', methods=['PUT'])
def atualizar_nota(id):
    """
    Atualizar uma nota
    ---
    tags: [Notas]
    parameters:
      - { name: id, in: path, type: integer, required: true }
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nota: { type: number, format: float }
            aluno_id: { type: integer }
            atividade_id: { type: integer }
    responses:
      200: { description: "Nota atualizada" }
      404: { description: "Nota, Aluno ou Atividade não encontrado" }
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({'erro': 'Nota não encontrada'}), 404
    data = request.get_json()

    if 'aluno_id' in data:
        a_resp = requests.get(f"{GERENCIAMENTO_URL}/alunos/{data['aluno_id']}")
        if a_resp.status_code != 200:
            return jsonify({'erro': 'Aluno não encontrado'}), 404
        nota.aluno_id = data['aluno_id']

    if 'atividade_id' in data:
        if not Atividade.query.get(data['atividade_id']):
            return jsonify({'erro': 'Atividade não encontrada'}), 404
        nota.atividade_id = data['atividade_id']

    nota.nota = data.get('nota', nota.nota)
    
    db.session.commit()
    return jsonify(to_dict(nota))

@atividades_bp.route('/notas/<int:id>', methods=['DELETE'])
def deletar_nota(id):
    """
    Deletar uma nota
    ---
    tags: [Notas]
    parameters:
      - { name: id, in: path, type: integer, required: true }
    responses:
      200: { description: "Nota deletada" }
      404: { description: "Nota não encontrada" }
    """
    nota = Nota.query.get(id)
    if not nota:
        return jsonify({'erro': 'Nota não encontrada'}), 404
    db.session.delete(nota)
    db.session.commit()
    return jsonify({'mensagem': 'Nota deletada com sucesso'})

@atividades_bp.route('/atividades/<int:id>/notas', methods=['GET'])
def listar_notas_por_atividade(id):
    """
    Listar todas as notas de uma atividade
    ---
    tags: [Notas]
    parameters:
      - { name: id, in: path, type: integer, required: true, description: "ID da Atividade" }
    responses:
      200: { description: "Lista de notas da atividade" }
      404: { description: "Atividade não encontrada" }
    """
    atividade = Atividade.query.get(id)
    if not atividade:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    
    notas = [to_dict(n) for n in atividade.notas]
    return jsonify(notas)

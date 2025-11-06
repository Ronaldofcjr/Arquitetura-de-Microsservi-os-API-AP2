from flask import Blueprint, request, jsonify
from app.models import db, Reserva
import requests, os

reservas_bp = Blueprint('reservas', __name__)
GERENCIAMENTO_URL = os.getenv('GERENCIAMENTO_URL', 'http://gerenciamento:5000')

@reservas_bp.route('/reservas', methods=['POST'])
def criar_reserva():
    """
    Criar uma nova reserva
    ---
    tags:
      - Reservas
    description: Cria uma nova reserva vinculada a uma turma existente no serviço de Gerenciamento.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id_turma
            - data
          properties:
            id_turma:
              type: integer
              description: ID da turma existente no serviço de gerenciamento
              example: 1
            data:
              type: string
              description: Data da reserva (pode ser texto livre ou formato ISO)
              example: "2025-11-05"
    responses:
      201:
        description: Reserva criada com sucesso
        examples:
          application/json: {
            "id": 1,
            "id_turma": 1,
            "data": "2025-11-05"
          }
      404:
        description: Turma não encontrada
        examples:
          application/json: {
            "erro": "Turma não encontrada"
          }
    """
    data = request.get_json()
    id_turma = data.get('id_turma')

    # valida se a turma existe no Gerenciamento
    resp = requests.get(f"{GERENCIAMENTO_URL}/turmas/{id_turma}")
    if resp.status_code != 200:
        return jsonify({'erro': 'Turma não encontrada'}), 404

    reserva = Reserva(id_turma=id_turma, data=data['data'])
    db.session.add(reserva)
    db.session.commit()
    return jsonify({'id': reserva.id, 'id_turma': id_turma, 'data': reserva.data}), 201

@reservas_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    """
    Listar todas as reservas
    ---
    tags:
      - Reservas
    description: Retorna uma lista de todas as reservas cadastradas.
    responses:
      200:
        description: Lista de reservas
        examples:
          application/json: [
            {"id": 1, "id_turma": 1, "data": "2025-11-05"},
            {"id": 2, "id_turma": 2, "data": "2025-11-06"}
          ]
    """
    reservas = Reserva.query.all()
    return jsonify([{'id': r.id, 'id_turma': r.id_turma, 'data': r.data} for r in reservas])

@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def obter_reserva(id):
    """
    Obter uma reserva por ID
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da reserva
    responses:
      200:
        description: Dados da reserva
      404:
        description: Reserva não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'erro': 'Reserva não encontrada'}), 404
    return jsonify({'id': reserva.id, 'id_turma': reserva.id_turma, 'data': reserva.data})

@reservas_bp.route('/reservas/<int:id>', methods=['PUT'])
def atualizar_reserva(id):
    """
    Atualizar uma reserva
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da reserva
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_turma:
              type: integer
            data:
              type: string
    responses:
      200:
        description: Reserva atualizada
      404:
        description: Reserva ou Turma não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'erro': 'Reserva não encontrada'}), 404
    data = request.get_json()
    id_turma = data.get('id_turma')
    if id_turma:
        resp = requests.get(f"{GERENCIAMENTO_URL}/turmas/{id_turma}")
        if resp.status_code != 200:
            return jsonify({'erro': 'Turma não encontrada'}), 404
        reserva.id_turma = id_turma
    reserva.data = data.get('data', reserva.data)
    db.session.commit()
    return jsonify({'id': reserva.id, 'id_turma': reserva.id_turma, 'data': reserva.data})

@reservas_bp.route('/reservas/<int:id>', methods=['DELETE'])
def deletar_reserva(id):
    """
    Deletar uma reserva
    ---
    tags:
      - Reservas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID da reserva
    responses:
      200:
        description: Reserva deletada
      404:
        description: Reserva não encontrada
    """
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({'erro': 'Reserva não encontrada'}), 404
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({'mensagem': 'Reserva deletada com sucesso'})

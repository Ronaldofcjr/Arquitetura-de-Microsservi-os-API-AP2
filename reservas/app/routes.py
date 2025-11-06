from flask import Blueprint, request, jsonify
from app.models import db, Reserva
import requests, os
from datetime import datetime

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
            - turma_id
            - num_sala
            - data
          properties:
            turma_id:
              type: integer
              description: ID da turma existente no serviço de gerenciamento
              example: 1
            num_sala:
              type: integer
              description: Número da sala reservada.
              example: 101
            lab:
              type: boolean
              description: Indica se a reserva é em um laboratório.
              example: false
            data:
              type: string
              format: date
              description: Data da reserva no formato YYYY-MM-DD.
              example: "2025-11-05"
    responses:
      201:
        description: Reserva criada com sucesso
      404:
        description: Turma não encontrada
    """
    data = request.get_json()
    turma_id = data.get('turma_id')
    num_sala = data.get('num_sala')
    lab = data.get('lab', False)
    data_str = data.get('data')

    if not all([turma_id, num_sala, data_str]):
        return jsonify({'erro': 'Campos obrigatórios ausentes'}), 400

    try:
        data_reserva = datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

    resp = requests.get(f"{GERENCIAMENTO_URL}/turmas/{turma_id}")
    if resp.status_code != 200:
        return jsonify({'erro': 'Turma não encontrada'}), 404

    reserva = Reserva(
        turma_id=turma_id,
        num_sala=num_sala,
        lab=lab,
        data=data_reserva
    )
    db.session.add(reserva)
    db.session.commit()
    
    return jsonify({
        'id': reserva.id,
        'turma_id': reserva.turma_id,
        'num_sala': reserva.num_sala,
        'lab': reserva.lab,
        'data': reserva.data.isoformat()
    }), 201

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
    """
    reservas = Reserva.query.all()
    return jsonify([
        {
            'id': r.id,
            'turma_id': r.turma_id,
            'num_sala': r.num_sala,
            'lab': r.lab,
            'data': r.data.isoformat()
        } for r in reservas
    ])

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
    return jsonify({
        'id': reserva.id,
        'turma_id': reserva.turma_id,
        'num_sala': reserva.num_sala,
        'lab': reserva.lab,
        'data': reserva.data.isoformat()
    })

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
            turma_id:
              type: integer
            num_sala:
              type: integer
            lab:
              type: boolean
            data:
              type: string
              format: date
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
    turma_id = data.get('turma_id')
    if turma_id:
        resp = requests.get(f"{GERENCIAMENTO_URL}/turmas/{turma_id}")
        if resp.status_code != 200:
            return jsonify({'erro': 'Turma não encontrada'}), 404
        reserva.turma_id = turma_id

    reserva.num_sala = data.get('num_sala', reserva.num_sala)
    reserva.lab = data.get('lab', reserva.lab)
    
    if 'data' in data:
        try:
            reserva.data = datetime.strptime(data['data'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

    db.session.commit()
    return jsonify({
        'id': reserva.id,
        'turma_id': reserva.turma_id,
        'num_sala': reserva.num_sala,
        'lab': reserva.lab,
        'data': reserva.data.isoformat()
    })

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

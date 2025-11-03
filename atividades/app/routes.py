from flask import Blueprint, request, jsonify
from app.models import db, Atividade
import requests, os

atividades_bp = Blueprint('atividades', __name__)
GERENCIAMENTO_URL = os.getenv('GERENCIAMENTO_URL', 'http://gerenciamento:5000')

@atividades_bp.route('/atividades', methods=['POST'])
def criar_atividade():
    """
    Criar uma nova atividade
    ---
    tags:
      - Atividades
    description: Cadastra uma nova atividade vinculada a um professor e a uma turma existentes.
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - id_professor
            - id_turma
            - descricao
          properties:
            id_professor:
              type: integer
              example: 1
            id_turma:
              type: integer
              example: 2
            descricao:
              type: string
              example: "Prova de Matemática - Capítulo 3"
    responses:
      201:
        description: Atividade criada com sucesso
        examples:
          application/json: {
            "id": 1,
            "id_professor": 1,
            "id_turma": 2,
            "descricao": "Prova de Matemática - Capítulo 3"
          }
      404:
        description: Professor ou turma inválidos
        examples:
          application/json: {"erro": "Professor ou Turma inválidos"}
    """
    data = request.get_json()
    id_professor = data.get('id_professor')
    id_turma = data.get('id_turma')

    # valida professor e turma no Gerenciamento
    p = requests.get(f"{GERENCIAMENTO_URL}/professores/{id_professor}")
    t = requests.get(f"{GERENCIAMENTO_URL}/turmas/{id_turma}")

    if p.status_code != 200 or t.status_code != 200:
        return jsonify({'erro': 'Professor ou Turma inválidos'}), 404

    atividade = Atividade(id_professor=id_professor, id_turma=id_turma, descricao=data['descricao'])
    db.session.add(atividade)
    db.session.commit()
    return jsonify({'id': atividade.id, 'descricao': atividade.descricao}), 201

@atividades_bp.route('/atividades', methods=['GET'])
def listar_atividades():
    """
    Listar todas as atividades
    ---
    tags:
      - Atividades
    description: Retorna todas as atividades cadastradas no sistema.
    responses:
      200:
        description: Lista de atividades
        examples:
          application/json: [
            {
              "id": 1,
              "id_professor": 1,
              "id_turma": 2,
              "descricao": "Prova de Matemática - Capítulo 3"
            },
            {
              "id": 2,
              "id_professor": 1,
              "id_turma": 2,
              "descricao": "Trabalho de Álgebra Linear"
            }
          ]
    """
    atividades = Atividade.query.all()
    return jsonify([{'id': a.id, 'id_professor': a.id_professor, 'id_turma': a.id_turma, 'descricao': a.descricao} for a in atividades])

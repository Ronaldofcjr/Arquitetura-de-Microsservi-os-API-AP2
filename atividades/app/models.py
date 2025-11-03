from app.database import db

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_professor = db.Column(db.Integer, nullable=False)
    id_turma = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)

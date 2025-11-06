from app.database import db

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    peso_projeto = db.Column(db.Float, nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)
    notas = db.relationship('Nota', backref='atividade', lazy=True, cascade="all, delete-orphan")

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividade.id'), nullable=False)

from app.database import db

class Atividade(db.Model):
    __tablename__ = 'atividades'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(100))
    peso_porcento = db.Column(db.Integer)
    data_entrega = db.Column(db.Date)
    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)

    notas = db.relationship('Nota', back_populates='atividade', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Atividade {self.nome_atividade}>'


class Nota(db.Model):
    __tablename__ = 'notas'

    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    aluno_id = db.Column(db.Integer, nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'))

    atividade = db.relationship('Atividade', back_populates='notas')

    def __repr__(self):
        return f'<Nota aluno={self.aluno_id} nota={self.nota}>'

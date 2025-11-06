from app.database import db

class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100))
    observacoes = db.Column(db.Text)

    turmas = db.relationship('Turma', back_populates='professor', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Professor {self.nome}>'


class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    professor = db.relationship('Professor', back_populates='turmas')
    
    alunos = db.relationship('Aluno', back_populates='turma', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Turma {self.descricao}>'


class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    data_nascimento = db.Column(db.Date)
    
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))
    turma = db.relationship('Turma', back_populates='alunos')

    def __repr__(self):
        return f'<Aluno {self.nome}>'

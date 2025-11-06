from app.database import db

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_turma = db.Column(db.Integer, nullable=False)
    data = db.Column(db.String(50), nullable=False)

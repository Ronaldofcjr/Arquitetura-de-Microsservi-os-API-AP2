from app.database import db

class Reserva(db.Model):
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.Date, nullable=False)
    
    turma_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Reserva sala={self.num_sala} data={self.data}>'

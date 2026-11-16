from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def agora_utc():
    return datetime.now(timezone.utc)

class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(60), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)


class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    data_retirada = db.Column(db.DateTime, nullable=False, default=agora_utc)
    data_devolucao = db.Column(db.DateTime, nullable=False, default=lambda: agora_utc() + timedelta(days=14))
    devolvido = db.Column(db.Boolean, default=False)

    livro = db.relationship('Livro', backref='emprestimos')

    @property
    def em_atraso(self):
        prevista = self.data_devolucao
        if prevista.tzinfo is None:
            prevista = prevista.replace(tzinfo=timezone.utc)
        return not self.devolvido and agora_utc() > prevista

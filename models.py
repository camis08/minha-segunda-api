from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Tarefas(db.Model):
    __tablename__ = 'tarefas'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return{
            'id':self.id,
            'titulo':self.titulo,
            'descricao':self.descricao,
            'concluida':self.concluida
        }



class Alunos(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id':self.id,
            'nome': self.nome,
            'curso': self.curso
        }
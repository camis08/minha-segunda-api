from flask import Flask, jsonify, request
from models import db, Alunos, Tarefas

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # configuracao url da base de dados
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False             # modificacao automatica desativada

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():                 # se nao tiver tabelas no models, cria
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    return jsonify(
        {
            'mensagem': 'API com Banco de dados'
        }
    ),200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}),200

@app.route('/tarefas', methods=['POST'])
def criar_tarefas():
    data = request.get_json()
    if not data:
         return jsonify({
            "erro": "nenhum dado foi enviado"
         }),400

    campos_obrigatorio = ["titulo", "descricao"]

    for campo in campos_obrigatorio:
        if campo not in data:
            return jsonify({
                "erro":f"O campo {campo} eh obrigatorio"
            }),400


    nova_tarefa = Tarefas(
        titulo = data['titulo'],
        descricao= data['descricao'],
        concluida = data.get('concluida', False)
    )

    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify(nova_tarefa.to_dict()),200

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():

    #criar a consulta:
    consulta = db.select(Tarefas).order_by(Tarefas.id)

    #exercutar a consulta e salvar na variavel 'resultado':
    resultado = db.session.execute(consulta)

    #salvar os resultado na variavel tarefas
    tarefas = resultado.scalars().all()

    #tarefas = Tarefas.query.order_by(Tarefas.id).all()

    lista_tarefas = []

    for tarefa in tarefas:
        lista_tarefas.append(tarefa.to_dict())

    return jsonify(lista_tarefas), 200

@app.route('/tarefas/<int:id_tarefas>', methods=['GET'])
def buscar_tarefas(id_tarefas):
    tarefa = db.session.get(Tarefas, id_tarefas)

    if tarefa is None:
        return jsonify({"erro": "Tarefa nao encontrada"}),404

    return jsonify(tarefa.to_dict()), 200

## aula de segunda feira
@app.route('/tarefas/<int:id_tarefa>', methods=['PUT'])
def atualizar_tarefas(id_tarefa):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi enviado"}), 400

    campos_obrigatorios = ["titulo", "descricao", "concluida"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"Campo {campo} eh obrigatorio"}), 404


    try:
        tarefa = db.session.get(Tarefas, id_tarefa)

        if tarefa is None:
            return jsonify({"erro": "Tarefa nao encontrada"}), 404

        tarefa.titulo = dados["titulo"]
        tarefa.descricao = dados["descricao"]
        tarefa.concluida = dados["concluida"]

        db.session.commit()

        return jsonify(tarefa.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


@app.route('/tarefas/<int:id_tarefa>', methods=['PATCH'])
def alterar_tarefas(id_tarefa):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi enviado"}), 400

    tarefa = db.session.get(Tarefas, id_tarefa)

    if tarefa is None:
        return jsonify({"erro": "Tarefa nao encontrada"}), 404

    if "titulos" in dados:
        tarefa.titulo = dados["titulo"]
    if "descricao" in dados:
        tarefa.descricao = dados["descricao"]
    if "concluida" in dados:
        tarefa.concluida = dados["concluida"]

    db.session.commit()
    return jsonify(tarefa.to_dict()), 200


@app.route ('/tarefas/<int:id_tarefa>', methods=['DELETE'])
def excluir_tarefas(id_tarefa):
    tarefa = db.session.get(Tarefas, id_tarefa)
    if tarefa is None:
        return jsonify({"erro": "Tarefa nao encontrada"}), 404

    db.session.delete(tarefa)
    db.session.commit()

    return jsonify({"status": "Tarefa deletada"}), 200

"""
Criar Classe Alunos models.py
Depois:

1- Criar rota GET alunos
2- Criar rota POST alunos
3- Criar rota POST alunos
4- Criar rota PUT alunos
5- Criar rota PATCH alunos
6- Criar rota DELETE alunos
"""

@app.route('/alunos' , methods=['POST'])
def criar_aluno():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "nenhum dado foi enviado"}),400

    campos_obrigatorios = ["nome", "curso"]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({
                "erro": f"O campo {campo} eh obrigatorio"
            }), 400

    novo_aluno = Alunos(
        nome=dados['nome'],
        curso=dados['curso']
    )

    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify(novo_aluno.to_dict()), 201

@app.route('/alunos', methods=['GET'])
def listar_alunos():

    #criar a consulta:
    consulta = db.select(Alunos).order_by(Alunos.id)

    resultado = db.session.execute(consulta)

    alunos = resultado.scalars().all()

    lista_alunos = []

    for aluno in alunos:
        lista_alunos.append(aluno.to_dict())

    return jsonify(lista_alunos), 200

 
@app.route('/alunos/<int:id_alunos>' , methods=['GET'])
def buscar_alunos(id_alunos):
    aluno = db.session.get(Alunos, id_alunos)

    if aluno is None:
        return jsonify({"erro": "Aluno nao encontrado"}),404

    return jsonify(aluno.to_dict()), 200


@app.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi enviado"}), 400

    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    campos_obrigatorios = ["nome", "curso"]

    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({"erro": f"O campo {campo} é obrigatório"}), 400

    try:
        aluno.nome = dados["nome"]
        aluno.curso = dados["curso"]

        db.session.commit()

        return jsonify(aluno.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


@app.route('/alunos/<int:id_aluno>', methods=['PATCH'])
def alterar_alunos(id_aluno):
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado foi enviado"}), 400

    aluno = db.session.get(Alunos, id_aluno)

    if aluno is None:
        return jsonify({"erro": "Aluno nao encontrado"}), 404
    if "nome" in dados:
        aluno.nome = dados["nome"]
    if "curso" in dados:
        aluno.curso = dados["curso"]

    db.session.commit()
    return jsonify(aluno.to_dict()), 200


@app.route ('/alunos/<int:id_aluno>', methods=['DELETE'])
def excluir_alunos(id_aluno):
    aluno = db.session.get(Alunos, id_aluno)
    if aluno is None:
        return jsonify({"erro": "Aluno nao encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()

    return jsonify({"status": "Aluno deletado!"}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
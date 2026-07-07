from flask import Flask, jsonify, request
from models import db, Tarefas
from models import db, Alunos

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # configuracao url da base de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False             # modificacao automatica desativada

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

## ALUNOS


@app.route('/alunos' , methods=['POST'])
def criar_aluno():
    data = request.get_json()
    if not data:
        return jsonify({"erro": "nenhum dado foi enviado"}),400

    campos_obrigatorio = ["nome", "curso"]

    for campo in campos_obrigatorio:
        if campo not in data:
            return jsonify({
                "erro": f"O campo {campo} eh obrigatorio"
            }), 400

    novo_aluno = Alunos(
        nome=data['nome'],
        curso=data['curso']
    )

    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify(novo_aluno.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
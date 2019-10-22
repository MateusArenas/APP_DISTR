from flask import Flask, jsonify, request
import util
app = Flask(__name__)


@app.route('/')
def all():
    return jsonify(database)

@app.route('/reseta', methods=['POST'])
def reseta():
  util.reseta()
  return 'banco resetado'


@app.route('/disciplinas', methods=['GET'])
def disciplinas():
  return jsonify(util.all_for_database('DICIPLINAS'))



@app.route('/disciplinas/<int:id_disciplina>', methods=['GET'])
def get_disciplina(id_disciplina):
  try: 
    disciplina = util.localiza(id_disciplina,'DICIPLINAS')
    return jsonify(disciplina)
  except util.NotFoundError:
    return jsonify({'erro':'disciplina nao encontrada'}),400

@app.route('/disciplinas/<int:id_disciplina>', methods=['DELETE'])
def deleta_disciplina(id_disciplina):
  try: 
    disciplina = util.localiza(id_disciplina,'DICIPLINAS')
    removido = util.remove(disciplina,'DICIPLINAS')
    return jsonify(removido)
  except util.NotFoundError:
    return jsonify({'erro':'disciplina nao encontrada'}),400

@app.route('/disciplinas/<int:id_disciplina>', methods=['PUT'])
def edita_disciplina(id_disciplina):
  try: 
    disciplina = util.localiza(id_disciplina,'DICIPLINAS')
    nova_disciplina = request.json
    if 'nome' not in nova_disciplina:
      return jsonify({'erro':'disciplina sem nome'}),400
    for key in disciplina:
      if key in nova_disciplina:
        disciplina[key] = nova_disciplina[key]
    return jsonify(disciplina)
  except util.NotFoundError:
    return jsonify({'erro':'disciplina nao encontrada'}),400

@app.route('/disciplinas', methods=['POST'])
def nova_disciplina():
  print('ola')
  nova_disciplina = request.json
  resposta,erro = util.verifica_campo(nova_disciplina,campos_inteiros=['id', 'status', 'carga_horaria'],campos_texto=['nome', 'plano_ensino'],campos_opcinais=['id_coordenador'])
  if resposta == False:
    return erro,400
  # campos = ['nome', 'id', 'status', 'plano_ensino', 'carga_horaria']
  # print(request.method)
  # for campo in campos:
  #   if campo not in nova_disciplina:
  #     return jsonify({'erro':'disciplina sem ' + campo}),400
  try:
    disciplina = util.localiza(nova_disciplina['id'],'DICIPLINAS')
    return jsonify({'erro':'id ja utilizada'}),400
  except util.NotFoundError:
    pass

  util.adiciona(nova_disciplina,'DICIPLINAS')
  return jsonify(util.all_for_database('DICIPLINAS'))



if __name__ == '__main__':
  app.run(host='localhost', port=5003, debug=True)

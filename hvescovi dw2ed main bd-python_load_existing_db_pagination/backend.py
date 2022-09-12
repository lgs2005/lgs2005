from urllib import request
from config import *
from modelo import *
from flask import request, jsonify

LIMITE_EMPRESAS = 50000


@app.route('/listar_empresas', methods=['GET'])
def listar_empresas():
    try:
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 100))
    except ValueError:
        offset = 0
        limit = 100

    if limit > LIMITE_EMPRESAS:
        limit = LIMITE_EMPRESAS

    empresas = Compania.query.offset(offset).limit(limit)
    empresas_json = [e.json() for e in empresas]

    resposta = jsonify(empresas_json)
    resposta.headers.set('Access-Control-Allow-Origin', '*')

    return resposta


if __name__ == '__main__':
    app.run(debug=True)

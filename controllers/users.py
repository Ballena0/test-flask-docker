import os
from flask import request, jsonify
from app import app, mongo
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(__name__, filename=os.path.join(ROOT_PATH, 'output.log'))

@app.route('/user', methods=['GET','POST','PATCH', 'DELETE'])
def user():
    if request.method == 'GET' :
        query = request.args
        data = mongo.db.users.find_one(query)
        return jsonify(data), 200

    data = request.get_json()
    if request.method == 'POST':
        if data.get('name', None) is not None and data.get('email', None) is not None:
            mongo.db.insert_one(data)
            return jsonify({'ok':True, 'mensaje':'Usuario creado con exito'}), 200
        else:
            return jsonify({'ok':False, 'mensaje':'Usuario no creado'}), 400

    if request.method == 'DELETE':
        if data.get('name',None) is not None:
            db_response = mongo.db.users.delete_one({'email':data['email']})
            if db_response.deleted_count == 1:
                response = {'ok':True, 'mensaje':'registro borrado'}
            else:
                response = {'ok':False, 'mensaje': 'registro no encontrado'}
            return jsonify(response), 200
        else:
            return jsonify({'ok':False, 'mensaje': 'parametros incorrectos'})

    if request.method == 'PATCH':
        if data.get('query',{}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})}
            )
            return jsonify({'ok':True, 'mensaje':'registro actualizado'}), 200
        else:
            return jsonify({'ok':False, 'mensaje':'parametros incorrectos'}), 400
import warnings

import subprocess

import database

from flask import Flask, jsonify, request, abort

warnings.filterwarnings("ignore")

app = Flask(__name__)

items = []

@app.route('/api/v1.0/etudiant', methods=['GET'])
def get_etudiants():
    database.getetudiants()
    result = database.resultsExportEtudiants
    print (result)
    return jsonify({'item': result}), 201


@app.route('/api/v1.0/etudiant', methods=['POST'])
def create_etudiant():
    database.createetudiant(request.json)

    return jsonify({'item': 'etudiant cree'}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

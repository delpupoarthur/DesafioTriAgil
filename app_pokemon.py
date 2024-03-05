from flask import Flask, jsonify, request
import requests
import json
import os

app = Flask(__name__)

# Função para buscar os dados de um Pokémon na pokeapi.co
def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_id = pokemon_data['id']
        pokemon_weight = pokemon_data['weight']
        pokemon_height = pokemon_data['height']
        return pokemon_id, pokemon_weight, pokemon_height
    else:
        return None, None, None

# Função para criar um novo ID para o time
def get_next_team_id(teams):
    return str(len(teams) + 1)

# Rota para listar todos os times registrados
@app.route('/api/teams', methods=['GET'])
def get_teams():
    try:
        with open('teams.txt', 'r') as file:
            teams = json.load(file)
            if not teams:
                return jsonify({'message': 'Nenhum time Pokemon cadastrado'}), 404
            return jsonify(teams)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return jsonify({'message': 'Nenhum time Pokemon cadastrado'}), 404

# Rota para buscar um time registrado por ID
@app.route('/api/teams/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id):
    try:
        with open('teams.txt', 'r') as file:
            teams = json.load(file)
            team = teams.get(str(team_id))
            if team:
                return jsonify(team)
            else:
                return jsonify({'error': 'Time não encontrado'}), 404
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return jsonify({'error': 'Nenhum time registrado'}), 404

# Rota para criação de um time de Pokémon
@app.route('/api/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    user = data.get('user')
    team = data.get('team')

    if not user or not team:
        return jsonify({'error': 'Usuário ou time não fornecido'}), 400

    team_data = []
    for pokemon_name in team:
        pokemon_id, pokemon_weight, pokemon_height = get_pokemon_data(pokemon_name)
        if pokemon_id is None:
            return jsonify({'error': f'Dados do Pokémon {pokemon_name} não encontrados'}), 400
        team_data.append({
            'id': pokemon_id,
            'name': pokemon_name,
            'weight': pokemon_weight,
            'height': pokemon_height
        })

    try:
        with open('teams.txt', 'r') as file:
            teams = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        teams = {}

    team_id = get_next_team_id(teams)
    new_team = {'owner': user, 'pokemons': team_data}

    teams[team_id] = new_team

    with open('teams.txt', 'w') as file:
        json.dump(teams, file)

    return jsonify({'message': 'Time criado com sucesso', 'id': team_id}), 201

if __name__ == '__main__':
    if not os.path.isfile('teams.txt'):
        with open('teams.txt', 'w') as file:
            file.write('{}')
    app.run(debug=True, host='0.0.0.0')

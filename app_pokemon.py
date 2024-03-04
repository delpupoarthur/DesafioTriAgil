from flask import Flask, jsonify, request
import requests
import json

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

# Rota para listar todos os times registrados
@app.route('/api/teams', methods=['GET'])
def get_teams():
    try:
        with open('teams.txt', 'r') as file:
            teams = json.load(file)
            return jsonify(teams)
    except FileNotFoundError:
        return jsonify({'error': 'Nenhum time registrado'}), 404

# Rota para buscar um time registrado por usuário
@app.route('/api/teams/<string:user>', methods=['GET'])
def get_team_by_user(user):
    try:
        with open('teams.txt', 'r') as file:
            teams = json.load(file)
            team = teams.get(user)
            if team:
                return jsonify(team)
            else:
                return jsonify({'error': 'Time não encontrado'}), 404
    except FileNotFoundError:
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
    except FileNotFoundError:
        teams = {}

    teams[user] = team_data

    with open('teams.txt', 'w') as file:
        json.dump(teams, file)

    return jsonify({'message': 'Time criado com sucesso', 'id': len(teams)}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

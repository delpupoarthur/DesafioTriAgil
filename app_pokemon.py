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

        # Extrai os dados solicitados do Pokemon
        pokemon_id = pokemon_data['id']
        pokemon_weight = pokemon_data['weight']
        pokemon_height = pokemon_data['height']
        return pokemon_id, pokemon_weight, pokemon_height
    # Retorna Nenhum para todos os dados se a requisição falhar
    else:
        return None, None, None

# Função para criar um novo ID para o time
def get_next_team_id(teams):
    return str(len(teams) + 1)

# Rota para listar todos os times registrados
@app.route('/api/teams', methods=['GET'])
def get_teams():
    try:
        with open('teams.json', 'r') as file:
            teams = json.load(file)
            return json.dumps(teams)
    # Retorna uma mensagem de erro se o arquivo estiver vazio
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return jsonify({'message': 'Nenhum time Pokemon cadastrado'}), 404

# Rota para buscar um time registrado por ID ou por owner
@app.route('/api/teams/<team_id_or_owner>', methods=['GET'])
def get_team(team_id_or_owner):
    try:
        with open('teams.json', 'r') as file:
            teams = json.load(file)

            # Verifica se a entrada é um ID
            if team_id_or_owner.isdigit():  
                team_id = int(team_id_or_owner)
                team = teams.get(str(team_id))
                if team:
                    return json.dumps(team)
                # Retorna um erro se o time não for encontrado
                else:
                    return jsonify({'error': 'Time nao encontrado'}), 404
                
            # Se não for por ID, é o owner
            else: 
                for team_id, team in teams.items():
                    if team['owner'] == team_id_or_owner:
                        return json.dumps(team)
                # Retorna um erro se o time não for encontrado
                return jsonify({'error': 'Time nao encontrado'}), 404
    # Retorna uma mensagem de erro se o arquivo estiver vazio
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return jsonify({'message': 'Nenhum time Pokemon cadastrado'}), 404


# Rota para criação de um time de Pokémon
@app.route('/api/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    user = data.get('user')
    team = data.get('team')
    
    # Retorna um erro se o usuário ou o time não forem fornecidos
    if not user or not team:
        return jsonify({'error': 'Usuario ou time nao fornecido'}), 400

    team_data = []
    for pokemon_name in team:
        pokemon_id, pokemon_weight, pokemon_height = get_pokemon_data(pokemon_name)
        if pokemon_id is None:
            # Retorna um erro se os dados de um Pokémon não forem encontrados
            return jsonify({'error': f'Dados do Pokemon {pokemon_name} nao encontrados'}), 400
        team_data.append({
            'id': pokemon_id,
            'name': pokemon_name,
            'weight': pokemon_weight,
            'height': pokemon_height
        })

    try:
        with open('teams.json', 'r') as file:
            teams = json.load(file)
    # Se o arquivo não existir ou estiver vazio, inicializa uma lista vazia de times
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        teams = {}

    team_id = get_next_team_id(teams)
    new_team = {'owner': user, 'pokemons': team_data}

    teams[team_id] = new_team

    # Salva os times atualizados
    with open('teams.json', 'w') as file:
        json.dump(teams, file)

    # Retorna uma mensagem de sucesso com o ID do novo time
    return jsonify({'message': 'Time criado com sucesso', 'id': team_id}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

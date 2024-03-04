import requests

# Dados do novo time de Pokémon
new_team_data = {
    "user": "josias",
    "team": [
        "ditto",
        "pikachu",
        "squirtle"
    ]
}

# URL da rota de criação de times
url = 'http://localhost:5000/api/teams'

# Envie uma solicitação POST com os dados do novo time
response = requests.post(url, json=new_team_data)

# Verifique a resposta da solicitação
if response.status_code == 201:
    print("Time criado com sucesso!")
    print("ID do time:", response.json()['id'])
else:
    print("Erro ao criar o time:", response.json())

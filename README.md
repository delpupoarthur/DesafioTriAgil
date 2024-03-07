# Flask Pokémon Teams API

Este aplicativo serve como um gerenciador para times de Pokémon utilizando dados da PokeAPI. Os usuários podem criar, buscar e listar times de Pokémon registrados no sistema. Cada time consiste em um usuário (owner) e uma lista de Pokémons.

Esse é um projeto desenvolvido para o processo seletivo da Triágil.

## Rotas

- GET /api/teams: Lista todos os times Pokémon registrados.
- GET /api/teams/{user}: Busca um time registrado por usuário, a busca pode ser feita pelo id ou pelo nome do treinador.
- POST /api/teams: Rota para criação de um time, que recebe um JSON.

## Tratamento de Erros
O app retorna erro nas seguintes situações:
- Nome de pokémon inválido.
- No caso de "team" vazio na rota POST /api/teams.
- No caso de "user" vazio na rota POST /api/teams. 
- User não encontrado durante a rota GET/api/teams{user}.
- Se nenhum time for encontrado durante a rota GET/api/teams.

### Exemplo de uso

Para criar um novo time de Pokémon, faça uma solicitação POST para `/api/teams` com o seguinte formato de JSON:

```json
{
  "user": "Ash Ketchum",
  "team": ["pikachu", "charizard", "bulbasaur", "snorlax"]
}
```

- user: Nome do treinador responsável pelo time.
- team: Lista de nomes de Pokémon no time.

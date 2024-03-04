# Use uma imagem base Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o contêiner
COPY . .

# Instale as dependências
RUN pip install flask requests

# Exponha a porta do aplicativo
EXPOSE 5000

# Comando para executar o aplicativo Flask
CMD ["python", "app_pokemon.py"]

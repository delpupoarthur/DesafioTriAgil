# Usar uma imagem base Python
FROM python:3.9-slim

# Definie o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos necessários para o contêiner
COPY . .

# Instale as dependências
RUN pip install flask requests

# Expor a porta do aplicativo
EXPOSE 5000

# Comando para executar o aplicativo
CMD ["python", "app_pokemon.py"]

# Usar a imagem oficial do Python
FROM python:3.9-slim

# Definir diretório de trabalho dentro do container
WORKDIR /app

# Copiar arquivos de código para o container
COPY . .

# Instalar as dependências do Python
RUN pip install -r requirements.txt

# Definir o comando para iniciar a aplicação
CMD ["python", "app.py"]

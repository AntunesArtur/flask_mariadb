from flask import Flask, request, jsonify
from flasgger import Swagger
import mysql.connector
import os

app = Flask(__name__)
swagger = Swagger(app)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        charset='utf8mb4',
        collation='utf8mb4_unicode_ci'
    )
    return conn

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Flask APP!'})

@app.route('/users', methods=['POST'])
def add_user():
    """
    Adiciona um usuário ao banco de dados.
    ---
    parameters:
      - name: user
        in: body
        required: true
        schema:
          id: User
          required:
            - name
          properties:
            name:
              type: string
              description: Nome do usuário
    responses:
      201:
        description: Usuário adicionado com sucesso.
      400:
        description: Erro de validação.
    """
    data = request.json
    name = data['name']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO users (name) VALUES (%s)', (name,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'User added successfully!'}), 201

@app.route('/users', methods=['GET'])
def get_users():
    """
    Lista todos os usuários do banco de dados.
    ---
    responses:
      200:
        description: Lista de usuários.
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
                description: ID do usuário.
              name:
                type: string
                description: Nome do usuário.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name FROM users')
    users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return conn

# Rota para adicionar um usuário no banco de dados
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO users (name) VALUES (%s)', (name,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return jsonify({'message': 'User added successfully!'})

# Rota para listar todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name FROM users')
    users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

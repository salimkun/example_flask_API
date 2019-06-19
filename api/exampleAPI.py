#!/usr/bin/python3
"""
Implementasi sederhana RESTful API menggunakan Flask.
Flask harus terlebih dahulu diinstal di komputer.
SQLite digunakan untuk contoh sederhana penyimpanan ke database.
Dibuat oleh Pipin Fitriadi (email: pipinfitriadi@gmail.com),
pada tanggal 28 Februari 2019.
"""
import json
import sqlite3
from sqlite3 import Error

from flask import abort, Flask, jsonify, redirect, request, url_for

def create_connection():
    """
    Fungsi untuk terhubung dengan database SQLite.
    """
    try:
        return sqlite3.connect('example_flask_api.db')
    except:
        print('Error! cannot create the database connection.')
        return None

def create_table():
    """
    Fungsi untuk membuat table 'users' di database, apabila tidak ada.
    """
    try:
        with create_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS users(
                    id integer PRIMARY KEY,
                    name text NOT NULL
                );
            ''')
    except Error as e:
        print(e)

def get(id=None, is_set=False):
    """
    Fungsi untuk mendapatkan data dari table 'users'.
    Key parameter id adalah integer dan tidak mandatory.
    Key parameter is_set adalah boolean dengan default nilai False.
    """
    with create_connection() as conn:
        c = conn.cursor()

        if id:
            c.execute(
                '''
                    SELECT *
                    FROM users
                    WHERE id = ?;
                ''',
                (id,)
            )

            row = c.fetchall()

            if row:
                row = row[0]
                data = {
                    'id': row[0],
                    'name': row[1]
                }
            else:
                data = []
        else:
            c.execute(
                '''
                    SELECT *
                    FROM users;
                ''',
            )
            
            data = [
                {
                    'id': row[0],
                    'name': row[1]
                } for row in c.fetchall()
            ]
    
    if data:
        data = {
            'code': 200,
            'message': 'User berhasil ditemukan.',
            'data': data
        }

        if is_set:
            data['code'] = 201
            data['message'] = 'Data user barhasil tersimpan.'
    else:
        abort(404)

    return data

def post():
    """
    Fungsi untuk menambahkan data ke table 'users'.
    Key parameter name adalah string dan mandatory.
    """
    with create_connection() as conn:
        c = conn.cursor()

        if request.json:
            name = json.loads(
                request.data
            ).get('name')
        else:
            name = request.form.get('name')

        if name:
            c.execute(
                '''
                    INSERT INTO users(name)
                                VALUES(?);
                ''',
                (name,)
            )

            id = c.lastrowid
        else:
            abort(400)
        
    return get(id, True)

def put(id):
    """
    Fungsi untuk mengubah salah satu data di table 'users'.
    Key parameter id adalah integer dan tidak mandatory.
    Key parameter name adalah string dan mandatory.
    """
    with create_connection() as conn:
        c = conn.cursor()

        if request.json:
            name = json.loads(
                request.data
            ).get('name')
        else:
            name = request.form.get('name')
        
        if name:
            c.execute(
                '''
                    UPDATE users
                    SET name = ?
                    WHERE id = ?;
                ''',
                (name, id)
            )
        else:
            abort(400)

    return get(id, True)

def delete(id):
    """
    Fungsi untuk menghapus salah satu data di table 'users'.
    Key parameter id adalah integer dan tidak mandatory.
    """
    with create_connection() as conn:
        c = conn.cursor()

        c.execute(
            '''
                DELETE
                FROM users
                WHERE id = ?;
            ''',
            (id,)
        )

    return {
        'code': 200,
        'message': 'Data user berhasil dihapus.',
        'data': None
    }

def response_api(data):
    """
    Fungsi untuk menampilkan data kedalam format Json.
    Key parameter data adalah dictionary dan mandatory.
    Berikut ini adalah contoh pengisian key parameter data:
    data = {
        'code': 200,
        'message': 'User berhasil ditemukan.',
        'data': [
            {
                'id': 1,
                'name': 'Kuda'
            }
        ]
    }
    """
    return (
        jsonify(**data),
        data['code']
    )

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(e):
    return response_api({
        'code': 400,
        'message': 'Ada kekeliruan input saat melakukan request.',
        'data': None
    })

@app.errorhandler(404)
def not_found(e):
    return response_api({
        'code': 404,
        'message': 'User tidak berhasil ditemukan.',
        'data': None
    })

@app.errorhandler(405)
def method_not_allowed(e):
    return response_api({
        'code': 405,
        'message': 'User tidak berhasil ditemukan.',
        'data': None
    })

@app.errorhandler(500)
def internal_server_error(e):
    return response_api({
        'code': 500,
        'message': 'Mohon maaf, ada gangguan pada server kami.',
        'data': None
    })

@app.route('/')
def root():
    return 'RESTful API Sederhana Menggunakan Flask'

@app.route('/users', methods=['GET', 'POST'])
@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def users(id=None):
    """
    RESTful API /users.
    """
    if request.method == 'GET':
        data = get(id)
    if request.method == 'POST':
        data = post()
    elif request.method == 'PUT':
        data = put(id)
    elif request.method == 'DELETE':
        data = delete(id)
    
    return response_api(data)

# if __name__ == '__main__':
#     create_table()
#     app.run(debug=True)
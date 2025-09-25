from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "delicatta.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        preco REAL NOT NULL,
                        estoque INTEGER NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        telefone TEXT,
                        email TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS fornecedores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        contato TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS vendas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cliente_id INTEGER,
                        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        pagamento TEXT,
                        total REAL,
                        FOREIGN KEY(cliente_id) REFERENCES clientes(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS itens_venda (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        venda_id INTEGER,
                        produto_id INTEGER,
                        quantidade INTEGER,
                        preco_unit REAL,
                        FOREIGN KEY(venda_id) REFERENCES vendas(id),
                        FOREIGN KEY(produto_id) REFERENCES produtos(id))''')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/produtos")
def produtos():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM produtos")
        produtos = c.fetchall()
    return render_template("produtos.html", produtos=produtos)

@app.route("/produtos/add", methods=["POST"])
def add_produto():
    nome = request.form["nome"]
    preco = request.form["preco"]
    estoque = request.form["estoque"]
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)", (nome, preco, estoque))
        conn.commit()
    return redirect(url_for("produtos"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)

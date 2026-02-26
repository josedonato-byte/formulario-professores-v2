from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from functools import wraps

app = Flask(__name__)

ARQUIVO = "respostas.xlsx"
SENHA_ADMIN = "admin123"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dados = request.form.to_dict()
        df_novo = pd.DataFrame([dados])

        if os.path.exists(ARQUIVO):
            df = pd.read_excel(ARQUIVO)
            df = pd.concat([df, df_novo], ignore_index=True)
        else:
            df = df_novo

        df.to_excel(ARQUIVO, index=False)
        return render_template("form.html", sucesso=True)

    return render_template("form.html", sucesso=False)


def verificar_senha(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        senha = request.args.get("senha")
        if senha != SENHA_ADMIN:
            return "Acesso negado."
        return func(*args, **kwargs)
    return wrapper


@app.route("/admin")
@verificar_senha
def admin():
    if os.path.exists(ARQUIVO):
        df = pd.read_excel(ARQUIVO)
        dados = df.to_dict(orient="records")
        colunas = df.columns
        return render_template("admin.html", dados=dados, colunas=colunas)
    return "Nenhuma resposta ainda."


@app.route("/download")
@verificar_senha
def download():
    if os.path.exists(ARQUIVO):
        return send_file(ARQUIVO, as_attachment=True)
    return "Arquivo não encontrado."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

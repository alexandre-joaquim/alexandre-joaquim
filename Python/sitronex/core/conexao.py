import os
import sqlite3

def obter_conexao_banco():
    """
    Retorna uma conexão com o banco de dados sitronex.db,
    localizado na pasta banco_dados, independente de onde o código for executado.
    """
    pasta_atual = os.path.dirname(os.path.abspath(__file__))  # core/
    caminho_db = os.path.join(pasta_atual, "..", "banco_dados", "sitronex.db")
    caminho_absoluto = os.path.abspath(caminho_db)

    if not os.path.exists(caminho_absoluto):
        raise FileNotFoundError(f"Banco de dados não encontrado em: {caminho_absoluto}")

    return sqlite3.connect(caminho_absoluto)


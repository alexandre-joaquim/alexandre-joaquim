# Projeto: Dashboard Profissional de Análise de Dados com Streamlit

import streamlit as st
import pandas as pd
import requests
import plotly.express as px 
import sqlite3
from datetime import datetime
import base64
import time

# ------------------------ CONFIGURAÇÕES DA PÁGINA ------------------------
st.set_page_config(page_title="Análise de Dados - Mercado Financeiro", layout="wide")
st.title("📊 Dashboard Profissional - Mercado Financeiro em Tempo Real")

# ------------------------ BANCO DE DADOS LOCAL (SQLite) ------------------
conn = sqlite3.connect("usuarios.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        senha TEXT NOT NULL,
        data_cadastro TEXT NOT NULL
    )
""")
conn.commit()

# ------------------------ FUNÇÕES DE CADASTRO E LOGIN ----------------------------
def cadastrar_usuario(nome, email, senha):
    data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO usuarios (nome, email, senha, data_cadastro) VALUES (?, ?, ?, ?)",
                   (nome, email, senha, data_cadastro))
    conn.commit()
    st.success("Usuário cadastrado com sucesso!")

def autenticar_usuario(email, senha):
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    return cursor.fetchone()

# ------------------------ LOGIN ------------------------------------------
if "usuario_autenticado" not in st.session_state:
    st.session_state.usuario_autenticado = False
    st.session_state.usuario_nome = ""

if not st.session_state.usuario_autenticado:
    st.sidebar.subheader("Login")
    email = st.sidebar.text_input("Email")
    senha = st.sidebar.text_input("Senha", type="password")
    botao_login = st.sidebar.button("Entrar")
    if email and senha and botao_login:
        user = autenticar_usuario(email, senha)
        if user:
            st.session_state.usuario_autenticado = True
            st.session_state.usuario_nome = user[1]
            st.rerun()
        else:
            st.sidebar.error("Credenciais inválidas.")
    st.stop()

# ------------------------ MENU PRINCIPAL ---------------------------
st.sidebar.success(f"Logado como: {st.session_state.usuario_nome}")
opcoes_paginas = ["Cadastro de Usuários", "Visualizar Usuários", "Dashboard - Criptomoedas", "Cotação de Moedas", "Sobre o Projeto"]
pagina = st.sidebar.radio("Navegação", opcoes_paginas)

# ------------------------ CADASTRO DE USUÁRIOS ---------------------------
if pagina == "Cadastro de Usuários":
    st.subheader("Cadastrar Novo Usuário")
    nome = st.text_input("Nome")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    if st.button("Cadastrar"):
        if nome and email and senha:
            cadastrar_usuario(nome, email, senha)
        else:
            st.warning("Por favor, preencha todos os campos.")

# ------------------------ VISUALIZAÇÃO DE USUÁRIOS ----------------------
elif pagina == "Visualizar Usuários":
    st.subheader("Usuários Cadastrados")
    df_usuarios = pd.read_sql("SELECT id, nome, email, data_cadastro FROM usuarios", conn)
    st.dataframe(df_usuarios)

# ------------------------ DASHBOARD COM API DE MERCADO ------------------
elif pagina == "Dashboard - Criptomoedas":
    st.subheader("Análise de Criptomoedas em Tempo Real")

    moedas = ["bitcoin", "ethereum", "cardano", "solana", "dogecoin"]
    moeda = st.selectbox("Escolha a Criptomoeda", moedas)

    url = f"https://api.coingecko.com/api/v3/coins/{moeda}/market_chart?vs_currency=usd&days=365"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        prices = data.get("prices", [])

        df = pd.DataFrame(prices, columns=["Timestamp", "Preço"])
        df["Data"] = pd.to_datetime(df["Timestamp"], unit="ms")
        df = df.drop("Timestamp", axis=1)
        df = df[["Data", "Preço"]]

        df["Média Móvel 7 dias"] = df["Preço"].rolling(window=7).mean()

        st.metric("Preço Atual (USD)", f"${df['Preço'].iloc[-1]:,.2f}")
        st.plotly_chart(px.line(df, x="Data", y=["Preço", "Média Móvel 7 dias"],
                                title=f"Variação de Preço - {moeda.upper()}"))

        with st.expander("Ver dados brutos"):
            st.dataframe(df)

        # Exportação para Excel
        csv = df.to_csv(index=False).encode('utf-8')
        b64 = base64.b64encode(csv).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{moeda}_precos.csv">📥 Baixar Dados em CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.error("Erro ao buscar dados da API CoinGecko.")

# ------------------------ PÁGINA DE COTAÇÃO DE MOEDAS ------------------
elif pagina == "Cotação de Moedas":
    st.subheader("Cotação de Moedas (Câmbio) - Fonte: AwesomeAPI")

    moedas = ["USD", "EUR", "GBP", "ARS", "BTC"]
    base = st.selectbox("Moeda base", moedas)

    url = f"https://economia.awesomeapi.com.br/json/last/{base}-BRL"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        try:
            dados = resposta.json()
            par = f"{base}BRL"
            if par in dados:
                info = dados[par]
                st.metric(label=f"💱 {base}/BRL", value=f"R$ {float(info['bid']):.2f}")
                st.write(f"""
                - 🕒 Última atualização: {info['create_date']}
                - 📈 Alta do dia: R$ {float(info['high']):.2f}
                - 📉 Baixa do dia: R$ {float(info['low']):.2f}
                - 📊 Variação: {float(info['pctChange']):.2f}%
                """)
                df = pd.DataFrame({
                    "Indicador": ["Alta", "Baixa", "Variação", "Compra", "Venda"],
                    "Valor (R$)": [
                        float(info["high"]),
                        float(info["low"]),
                        float(info["pctChange"]),
                        float(info["bid"]),
                        float(info["ask"])
                    ]
                })
                st.dataframe(df)
            else:
                st.warning("Par de moedas não encontrado.")
        except Exception as e:
            st.error(f"Erro ao processar resposta da API: {e}")
    else:
        st.error("Erro ao buscar dados da API de câmbio (AwesomeAPI).")

# ------------------------ SOBRE O PROJETO -------------------------------
elif pagina == "Sobre o Projeto":
    st.markdown("""
    ### Objetivo
    Este projeto foi desenvolvido com foco em **análise de dados aplicada ao mercado financeiro** utilizando as melhores práticas e tecnologias:

    - Interface interativa com Streamlit
    - Cadastro e gestão de usuários com autenticação
    - Integração com API pública em tempo real (CoinGecko - Criptomoedas)
    - Visualizações dinâmicas com Plotly
    - Exportação de relatórios
    - Análise de tendências com médias móveis

    ### Destaques Profissionais
    - Aplicação prática de engenharia e análise de dados
    - Projeto orientado a dados de alta relevância no mercado
    - Arquitetura modular e expansível
    - Ideal para apresentações profissionais e portfólio

    ### Expansões Incluídas
    - Login com autenticação de usuários
    - Exportação de relatórios em CSV
    - Cálculo de média móvel (análise de tendência)
    - Cotação de moedas (API ExchangeRate)
    - Acompanhamento de ações (Yahoo Finance API)

    ### Expansões Futuras
    - Alertas automáticos por e-mail
    - Upload e análise de dados personalizados pelo usuário
    """)
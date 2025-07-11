import os
import pandas as pd
import chardet
import re
import sqlite3
from sqlalchemy import create_engine

# === FUNÇÃO: Detecta encoding automaticamente ===
def detectar_encoding(caminho_arquivo, tamanho_amostra=10000):
    with open(caminho_arquivo, 'rb') as f:
        resultado = chardet.detect(f.read(tamanho_amostra))
    return resultado['encoding']

# === FUNÇÃO: Detecta separador automaticamente ===
def detectar_separador(caminho_arquivo, encoding, separadores=[';', ',', '|', '\t']):
    for sep in separadores:
        try:
            df_teste = pd.read_csv(caminho_arquivo, encoding=encoding, sep=sep, nrows=5)
            if df_teste.shape[1] > 1:
                return sep
        except Exception:
            continue
    return ';'

# === FUNÇÃO: Limpa caracteres especiais e invisíveis ===
def limpar_texto(texto):
    texto = re.sub(r'[\u200B\uFFFD\uFEFF]', '', str(texto))  # Caracteres invisíveis
    texto = re.sub(r'[^a-zA-Z0-9À-ÿ\s.,;:/()\-@]', '', texto)
    return texto.strip()

# === CONFIGURAÇÕES ===
caminho_pasta = r'C:\Users\ale\Desktop\Python\Arquivo_Procon'
saida_db = os.path.join(caminho_pasta, 'dados_consolidados.db')
nome_tabela = 'reclamacoes_procon'
dados_consolidados = []

# === PROCESSAMENTO ===
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        try:
            print(f"📄 Lendo {arquivo}...")
            encoding = detectar_encoding(caminho_arquivo)
            print(f"   → Encoding: {encoding}")
            sep = detectar_separador(caminho_arquivo, encoding)
            print(f"   → Separador: '{sep}'")

            df = pd.read_csv(caminho_arquivo, encoding=encoding, sep=sep, dtype=str, on_bad_lines='skip')
            df = df.loc[:, ~df.columns.duplicated()]
            df.columns = [limpar_texto(col) for col in df.columns]

            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].apply(limpar_texto)

            df['Arquivo_Origem'] = arquivo
            dados_consolidados.append(df)

        except Exception as e:
            print(f"❌ Erro no arquivo {arquivo}: {e}")

# === SALVAMENTO EM .DB ===
# === CONSOLIDAÇÃO COM PADRONIZAÇÃO DE COLUNAS ===
if dados_consolidados:
    # Intersecção de colunas comuns entre todos os DataFrames
    colunas_comuns = set(dados_consolidados[0].columns)
    for df in dados_consolidados[1:]:
        colunas_comuns &= set(df.columns)
    colunas_comuns = list(colunas_comuns)

    # Padroniza todos os DataFrames para ter apenas as colunas comuns
    dados_padronizados = [df[colunas_comuns].copy() for df in dados_consolidados]

    # Concatena
    df_final = pd.concat(dados_padronizados, ignore_index=True)

    # Limpeza final
    df_final = df_final.fillna('').replace('nan', '', regex=False)

    # Criação do banco SQLite
    from sqlalchemy import create_engine
    engine = create_engine(f'sqlite:///{saida_db}')
    df_final.to_sql(nome_tabela, con=engine, if_exists='replace', index=False)

    print(f"\n✅ Dados salvos com sucesso no banco SQLite: {saida_db}")
    print(f"   → Tabela criada: {nome_tabela}")
else:
    print("\n⚠️ Nenhum dado consolidado.")
    
    
    

'''

# === COMANDOS DA BIBLIOTECA os ===
os.listdir(pasta) = lista os arquivos dentro da pasta
os.path.join = junta caminhos (pasta + arquivo)

# === COMANDOS DA BIBLIOTECA pandas (pd) ===
pd.read_csv = lê um arquivo CSV como DataFrame (tabela)
pd.concat = junta vários DataFrames
pd.DataFrame(columns=...) = cria uma tabela vazia com colunas definidas
df.columns = acessa os nomes das colunas
df[col] = aplica valores/modificações a uma coluna
df.insert = insere uma nova coluna em posição específica
df.select_dtypes(include='object') = seleciona apenas colunas de texto
df.fillna('') = substitui valores nulos por vazio
df.replace('nan', '') = remove valores que são string 'nan'
df.to_sql = salva o DataFrame como tabela em banco de dados

# === COMANDOS DA BIBLIOTECA chardet ===
chardet.detect = detecta automaticamente o encoding de um arquivo

# === COMANDOS DA BIBLIOTECA re (expressões regulares) ===
re.sub = substitui caracteres com base em padrão

# === COMANDOS DA BIBLIOTECA datetime ===
datetime.datetime.now() = data e hora atual

# === COMANDOS DA BIBLIOTECA sqlalchemy ===
create_engine = cria uma conexão com banco de dados (ex: SQLite)
engine = objeto que representa essa conexão para operações

# === COMANDOS NATIVOS DO PYTHON ===
import = importa bibliotecas
def = define uma função
with open = abre arquivo (modo seguro)
for = laço de repetição
if / else = estruturas condicionais
in = verifica se está contido em algo
try / except = tenta executar / trata erro
print = imprime mensagens no terminal
append = adiciona item a uma lista
copy() = cria uma cópia do DataFrame
set() = cria um conjunto (usado aqui para intersecção de colunas)
list() = converte para lista
str = converte valor em texto

'''
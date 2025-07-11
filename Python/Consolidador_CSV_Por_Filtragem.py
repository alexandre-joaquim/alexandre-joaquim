import os
import pandas as pd
import chardet
import re

# === FUNÇÃO: Detecta encoding de forma automática ===
def detectar_encoding(caminho_arquivo, tamanho_amostra=10000):
    with open(caminho_arquivo, 'rb') as f:
        resultado = chardet.detect(f.read(tamanho_amostra))
    return resultado['encoding']

# === FUNÇÃO: Detecta separador adequado por tentativa ===
def detectar_separador(caminho_arquivo, encoding, separadores=[';', ',', '|', '\t']):
    for sep in separadores:
        try:
            df_teste = pd.read_csv(caminho_arquivo, encoding=encoding, sep=sep, nrows=5)
            if df_teste.shape[1] > 1:
                return sep
        except Exception:
            continue
    return ';'  # Padrão caso não detecte

# === FUNÇÃO: Limpa caracteres não pertencentes ao alfabeto brasileiro ===
def limpar_texto(texto):
    texto = re.sub(r'[\u200B\uFFFD\uFEFF]', '', str(texto))  # Invisíveis e substituição �
    texto = re.sub(r'[^a-zA-Z0-9À-ÿ\s.,;:/()\-@]', '', texto)
    return texto.strip()

# === CONFIGURAÇÕES ===
caminho_pasta = r'C:\Users\ale\Desktop\Python\Arquivo_Procon'
coluna_filtro = 'Nome Fantasia'
valor_desejado = 'Amazon.com.br'
caminho_saida = os.path.join(caminho_pasta, (f'1-{valor_desejado}.csv'))

dados_filtrados = []

# === PROCESSAMENTO DOS ARQUIVOS ===
for arquivo in os.listdir(caminho_pasta):
    if arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        try:
            print(f"📄 Lendo {arquivo}...")
            encoding = detectar_encoding(caminho_arquivo)
            print(f"   → Encoding detectado: {encoding}")

            sep = detectar_separador(caminho_arquivo, encoding)
            print(f"   → Separador identificado: '{sep}'")

            df = pd.read_csv(caminho_arquivo, encoding=encoding, sep=sep, dtype=str, on_bad_lines='skip')

            # Remove colunas duplicadas (mesmo nome)
            df = df.loc[:, ~df.columns.duplicated()]

            # LIMPEZA DOS NOMES DAS COLUNAS
            df.columns = [limpar_texto(col) for col in df.columns]

            # LIMPEZA DO CONTEÚDO DAS COLUNAS (apenas texto)
            for col in df.select_dtypes(include='object').columns:
                df[col] = df[col].apply(limpar_texto)

            # FILTRAGEM PELO VALOR DESEJADO
            if coluna_filtro in df.columns:
                df_filtrado = df[df[coluna_filtro] == valor_desejado].copy()
                df_filtrado['Arquivo_Origem'] = arquivo
                dados_filtrados.append(df_filtrado)
            else:
                print(f"⚠️  Coluna '{coluna_filtro}' não encontrada em: {arquivo}")
                print("    Colunas disponíveis:", df.columns.tolist())

        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")

# === CONSOLIDAÇÃO ===
if dados_filtrados:
    df_consolidado = pd.concat(dados_filtrados, ignore_index=True)

    # Substitui valores NaN e strings 'nan' por string vazia
    df_consolidado = df_consolidado.fillna('').replace('nan', '', regex=False)

    # Exporta para CSV forçando string vazia nas células faltantes
    df_consolidado.to_csv(
        caminho_saida,
        encoding='utf-8-sig',
        index=False,
        sep=';',
        na_rep=''
    )

    print(f"\n✅ Consolidação concluída!\n   Arquivo salvo em: {caminho_saida}")
else:
    print("\n❌ Nenhum dado válido foi encontrado para consolidar.")







'''

# === COMANDOS DA BIBLIOTECA os ===
os.listdir = lista arquivos de uma pasta
os.path.join = junta partes de um caminho (ex: pasta + nome do arquivo)

# === COMANDOS DA BIBLIOTECA pandas (pd) ===
pd.read_csv = lê arquivo CSV e cria tabela (DataFrame)
df.shape = mostra formato da tabela (linhas, colunas)
df.columns = lista os nomes das colunas
df.loc[:, ~df.columns.duplicated()] = remove colunas com nomes duplicados
df.select_dtypes(include='object') = seleciona colunas do tipo texto
df[col].apply(func) = aplica uma função a cada célula da coluna
pd.concat = junta várias tabelas em uma só
df.fillna('') = substitui valores vazios por string vazia
df.replace('nan', '') = substitui texto "nan" por string vazia
df.to_csv = salva a tabela em um arquivo CSV

# === COMANDOS DA BIBLIOTECA chardet ===
chardet.detect = detecta a codificação de caracteres de um arquivo

# === COMANDOS DA BIBLIOTECA re (expressões regulares) ===
re.sub = substitui padrões de texto por outro valor

# === COMANDOS NATIVOS DO PYTHON ===
import = importa biblioteca
def = define uma função
with open = abre arquivo com controle automático de fechamento
read = lê conteúdo de arquivo
return = retorna um valor de uma função
for = laço de repetição
if = condição (se)
else = senão
in = verifica se um item existe em outro
try / except = tenta executar / captura e trata erros
print = exibe mensagem no terminal
append = adiciona item a uma lista
copy = cria uma cópia de um objeto
strip = remove espaços no início e no fim da string
str = transforma um valor em texto
endswith = verifica se uma string termina com determinado sufixo

'''
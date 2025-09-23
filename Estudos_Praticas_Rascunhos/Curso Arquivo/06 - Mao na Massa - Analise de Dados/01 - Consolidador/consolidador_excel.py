import pandas as pd
import os
import datetime

data = datetime.datetime.now()

# criando um DataFrame vazio com a estrutura final do Consolidado
colunas = [
    'Segmento',
    'País',
    'Produto',
    'Qtde de Unidades Vendidas',
    'Preço Unitário',
    'Valor Total',
    'Desconto',
    'Valor Total c/ Desconto',
    'Custo Total',
    'Lucro',
    'Data',
    'Mês',
    'Ano'
]
consolidado = pd.DataFrame(columns=colunas)

# busca o nome dos arquivos a serem consolidados
arquivos = os.listdir("planilhas")

# realiza a consolidação dos arquivos (apenas .xlsx)
for excel in arquivos:

    if excel.endswith('.xlsx'):
        dados_arquivo = excel.split('-')
        segmento = dados_arquivo[0]
        pais = dados_arquivo[1].replace('.xlsx', '')
        
        try:
            df = pd.read_excel(f'planilhas\\{excel}')
            df.insert(0, 'Segmento', segmento)
            df.insert(1, 'País', pais)        
            consolidado = pd.concat([consolidado, df])    
        except:
            with open('log_erros.txt', 'a') as arquivo:
                arquivo.write(f'Erro ao tentar consolidar o arquivo {excel}.\n')
    else:
        with open('log_erros.txt', 'a') as arquivo:
            arquivo.write(f'O arquivo {excel} não é um arquivo Excel válido!\n')
            
# exporta o DataFrame consolidado para um arquivo Excel
consolidado.to_excel(f"Report-consolidado-{data.strftime('%d-%m-%Y')}.xlsx", 
                     index=False,
                     sheet_name='Report consolidado')



'''

# === COMANDOS DA BIBLIOTECA pandas (pd) ===
pd.DataFrame(columns=...) = cria uma tabela vazia com colunas definidas
pd.read_excel = lê um arquivo Excel e cria um DataFrame (tabela)
df.insert(posição, nome_coluna, valor) = insere nova coluna na posição desejada
pd.concat([a, b]) = junta dois DataFrames
df.to_excel = salva um DataFrame como arquivo Excel

# === COMANDOS DA BIBLIOTECA os ===
os.listdir('pasta') = lista os arquivos dentro da pasta indicada

# === COMANDOS DA BIBLIOTECA datetime ===
datetime.datetime.now() = retorna a data e hora atual
data.strftime('%d-%m-%Y') = formata a data no formato desejado (ex: 10-07-2025)

# === COMANDOS NATIVOS DO PYTHON ===
import = importa uma biblioteca
for = laço de repetição
if = condição (se)
else = senão
try / except = tenta executar / trata erro caso ocorra
with open = abre ou cria arquivo
.write() = escreve dentro de um arquivo de texto
.split('-') = divide a string usando o caractere hífen
.replace('.xlsx', '') = remove a extensão do nome do arquivo
.endswith('.xlsx') = verifica se o nome termina com .xlsx
= (atribuição) = atribui um valor a uma variável

'''
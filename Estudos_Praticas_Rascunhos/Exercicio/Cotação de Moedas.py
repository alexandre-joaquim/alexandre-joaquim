import tkinter as tk  # importa o tkinter pra criar a interface gráfica
import requests        # importa o requests pra fazer a requisição na API

# cria a janela principal
janela = tk.Tk()
janela.title('Cotação de Moedas')     # define o título da janela
janela.geometry('300x300')            # define o tamanho da janela

# cria o campo onde o usuário vai digitar a sigla da moeda (ex: usd)
entrada = tk.Entry()
entrada.pack(pady=10)  # coloca o campo na tela com espaço em cima e embaixo

# essa é a função que vai rodar quando clicar no botão
def cotacao_br():
    moeda = entrada.get().upper()  # pega o que o usuário digitou e transforma em maiúsculo
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}-BRL"  # monta o link da API com a moeda que o usuário digitou

    respsta = requests.get(url)  # faz a requisição pra API
    chave = moeda + "BRL"        # monta o nome da chave que a API retorna, tipo: USDBRL, EURBRL, etc.

    if respsta.status_code == 200:  # se a API respondeu com sucesso
        dados = respsta.json()      # transforma a resposta em dicionário
        if 'erro' in dados:         # se veio um erro na resposta (ex: moeda inválida)
            resultado["text"] = "Moeda não encontrada."  # mostra mensagem de erro
        else:
            resultado["text"] = dados[chave]['bid']  # se deu tudo certo, mostra a cotação (campo 'bid')
    else:
        resultado["text"] = "Erro na requisição."  # se a API não respondeu certo, mostra isso

# botão que chama a função cotacao_br quando clicado
botao = tk.Button(janela, text="Buscar Cotação", command=cotacao_br)
botao.pack(pady=10)

# esse é o campo onde o resultado vai aparecer
resultado = tk.Label(janela, text="", justify="left", font=("Arial", 12))
resultado.pack(pady=10)

# isso aqui mantém a janela funcionando
janela.mainloop()
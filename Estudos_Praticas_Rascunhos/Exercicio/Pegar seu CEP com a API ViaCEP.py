import requests         # importa a biblioteca requests pra fazer a requisição à API
import tkinter as tk    # importa tkinter pra criar a interface gráfica

# cria a janela principal
janela = tk.Tk()
janela.title("Busca de CEP")         # define o título da janela
janela.geometry("300x250")           # define o tamanho da janela (largura x altura)

# cria o campo de entrada onde o usuário vai digitar o CEP
entrada = tk.Entry(janela, font=("Arial", 14))
entrada.pack(pady=10)  # espaço em cima e embaixo


# função que vai ser chamada quando o botão for clicado
def buscar_cep():
    cep = entrada.get()  # pega o texto digitado no campo
    url = f"https://viacep.com.br/ws/{cep}/json/"  # monta a URL da API com o CEP
    resposta = requests.get(url)  # faz a requisição

    if resposta.status_code == 200:  # se a resposta foi OK (código 200)
        dados = resposta.json()      # converte JSON pra dicionário

        if "erro" in dados:  # se tiver "erro" no dicionário, o CEP não existe
            resultado["text"] = "CEP não encontrado."
        else:
            # mostra os dados formatados
            resultado["text"] = (f"CEP: {dados['cep']}\n"
                                 f"Logradouro: {dados['logradouro']}\n"
                                 f"Bairro: {dados['bairro']}\n"
                                 f"Cidade: {dados['localidade']}\n"
                                 f"Estado: {dados['uf']}\n"
                                 f"DDD: {dados['ddd']}")
    else:
        resultado["text"] = "Erro na requisição."  # se a API falhar
# Botao para buscar o CEP
botao = tk.Button(janela, text="Buscar CEP", command=buscar_cep) # o botão chama a função buscar_cep
botao.pack(pady=10)

# área onde vai aparecer o resultado
resultado = tk.Label(janela, text="", justify="left", font=("Arial", 12))
resultado.pack(pady=20)

# iniciar a janela
janela.mainloop()

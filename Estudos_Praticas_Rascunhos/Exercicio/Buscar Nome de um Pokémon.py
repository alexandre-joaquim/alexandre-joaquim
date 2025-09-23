import tkinter as tk
import requests

janela = tk.Tk()
janela.title("Busca de Pokémon")
janela.geometry("300x250")
entrada = tk.Entry(janela, font=("Arial", 14))
entrada.pack(pady=10)

def buscar_pokemon():
    pokemon = entrada.get().lower() # entrada de texto do usuário
    url = f'https://pokeapi.co/api/v2/pokemon/pikachu'
    resposta = requests.get(url)
    if resposta.status_code == 200: # verifica se o status.code é 200, ou seja, se a requisição foi bem sucedida
        dados = resposta.json() # converte a resposta em json para obter os dados
        if "erro" in dados:
            resultado["text"] = "Pokémon não encontrado."
        else:
            resultado["text"] = (f"Nome: {dados['name'].capitalize()}\n"
                                 f"Número: {dados['id']}\n"
                                 f"Tipo: {', '.join([t['type']['name'] for t in dados['types']])}")
    else:
        resultado["text"] = "Erro na requisição."
# Botão para buscar o Pokémon
botao = tk.Button(janela, text="Buscar Pokémon", command=buscar_pokemon) # o botão chama a função buscar_pokemon
botao.pack(pady=10)

resultado = tk.Label(janela, text="", justify="left", font=("Arial", 12)) # nessa linha ele cria um label(rotulo) para exibir o resultado
resultado.pack(pady=20) 
# iniciar a janela
janela.mainloop()
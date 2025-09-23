import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO


def nomes_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000" # tds os pokemon
    resposta = requests.get(url) # tras os dados da API
    dados = resposta.json() #converte para json
    nomes = [p["name"] for p in dados["results"]] # lista de nomes dos pokemons
    return nomes


def atualizar_sugestoes(event):
    texto = entrada.get().lower()
    sugestoes.delete(0, tk.END)

    if not texto:
        return

    correspondentes = [nome for nome in nomes_pokemon if nome.startswith(texto)]
    for nome in correspondentes[:10]:
        sugestoes.insert(tk.END, nome)

# Busca os dados do Pokémon selecionado
def buscar_dados(event):
    if not sugestoes.curselection():
        return

    selecao = sugestoes.get(sugestoes.curselection())
    url = f"https://pokeapi.co/api/v2/pokemon/{selecao.lower()}"
    resposta = requests.get(url)
    if resposta.status_code != 200:
        resultado["text"] = "Pokémon não encontrado."
        return

    dados = resposta.json()
    nome = dados["name"].capitalize()
    numero = dados["id"]
    tipos = ", ".join([t["type"]["name"].capitalize() for t in dados["types"]])
    sprite_url = dados["sprites"]["front_default"]

    # Atualiza os dados na interface
    resultado["text"] = f"Nome: {nome}\nNúmero: #{numero}\nTipo(s): {tipos}"
    mostrar_imagem(sprite_url)

# Carrega e exibe a imagem do Pokémon
def mostrar_imagem(url):
    resposta = requests.get(url)
    imagem_bytes = BytesIO(resposta.content)
    imagem_pil = Image.open(imagem_bytes)
    imagem_pil = imagem_pil.resize((96, 96))
    imagem_tk = ImageTk.PhotoImage(imagem_pil)
    
    imagem_label.configure(image=imagem_tk)
    imagem_label.image = imagem_tk  # Importante para manter referência

# Inicia a interface
janela = tk.Tk()
janela.title("Autocomplete Pokémon")
janela.geometry("400x500")

# Campo de entrada
entrada = tk.Entry(janela, font=("Arial", 14)) #
entrada.pack(pady=10)
entrada.bind("<KeyRelease>", atualizar_sugestoes)

# Lista de sugestões
sugestoes = tk.Listbox(janela, font=("Arial", 12), height=8)
sugestoes.pack()
sugestoes.bind("<<ListboxSelect>>", buscar_dados)

# Resultado do Pokémon
resultado = tk.Label(janela, text="", font=("Arial", 12), justify="left")
resultado.pack(pady=10)

# Imagem do Pokémon
imagem_label = tk.Label(janela)
imagem_label.pack(pady=10)

# Carrega nomes ao iniciar
resultado["text"] = "Carregando dados da PokéAPI..."
janela.update()
nomes_pokemon = nomes_pokemon()
resultado["text"] = "Digite o nome de um Pokémon."

# Inicia a interface
janela.mainloop()

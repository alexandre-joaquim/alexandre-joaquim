import os

def obter_icon():
    """
    Retorna o caminho absoluto do ícone da janela.
    Gera erro se o ícone não for encontrado.
    """
    # Caminho base: utilitários → volta para raiz → entra na pasta interface/icones
    pasta_atual = os.path.dirname(os.path.abspath(__file__))  # /sitronex/utilitarios
    caminho_icon = os.path.join(pasta_atual, "..", "icones", "infinidade.ico")
    caminho_absoluto = os.path.abspath(caminho_icon)

    if not os.path.exists(caminho_absoluto):
        raise FileNotFoundError(f"Ícone não encontrado em: {caminho_absoluto}")

    return caminho_absoluto
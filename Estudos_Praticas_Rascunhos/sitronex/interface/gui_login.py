import customtkinter as ctk  # Interface gráfica moderna
from core.seguranca import gerar_hash  # Função para gerar hash seguro
from core.conexao import obter_conexao_banco  # Função para conexão com o banco
from interface.icones.icones import obter_icon  # Caminho do ícone

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Estado interno da janela
        self.login_sucesso = False
        self.usuario_logado = None
        self.nivel_acesso = None

        # Configurações visuais da janela
        self.title("Sitronex - Login")
        self.geometry("400x450")
        self.resizable(False, False)
        self.iconbitmap(obter_icon())

        # Construção da interface gráfica
        self._construir_interface()
        self.protocol("WM_DELETE_WINDOW", self.destroy)  # Fecha a janela corretamente
        self.mainloop()

    def _construir_interface(self):
        # Título principal
        self.label_titulo = ctk.CTkLabel(self, text="Sitronex", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=(30, 10))

        # Subtítulo
        self.label_subtitulo = ctk.CTkLabel(self, text="Faça login para continuar", font=("Arial", 14))
        self.label_subtitulo.pack(pady=(0, 20))

        # Campo de usuário
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.entry_usuario.pack(pady=10, padx=40, fill="x")

        # Campo de senha oculto
        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_senha.pack(pady=10, padx=40, fill="x")

        # Botão para acessar
        self.botao_acessar = ctk.CTkButton(self, text="Acessar", command=self._validar_login)
        self.botao_acessar.pack(pady=20, padx=40, fill="x")

        # Botão "Esqueci minha senha"
        self.botao_esqueci = ctk.CTkButton(
            self,
            text="Esqueci minha senha",
            fg_color="transparent",
            text_color="blue",
            hover_color="lightblue"
        )
        self.botao_esqueci.pack(pady=5)

        # Label para mensagens de erro
        self.label_erro = ctk.CTkLabel(self, text="", text_color="red")
        self.label_erro.pack(pady=5)

    def _validar_login(self):
        # Limpa mensagem de erro
        self.label_erro.configure(text="")

        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        # Verifica se campos estão preenchidos
        if not usuario or not senha:
            self.label_erro.configure(text="Por favor, preencha todos os campos.")
            return

        try:
            with obter_conexao_banco() as conexao:
                cursor = conexao.cursor()

                # Busca senha, status e nível de acesso do usuário
                cursor.execute(
                    "SELECT senha_hash, ativo, nivel_acesso, nome_completo, setor FROM usuarios WHERE nome_usuario = ?",
                    (usuario,)
                )
                resultado = cursor.fetchone()

                if resultado:
                    senha_hash_banco, ativo, nivel_acesso, nome_completo, setor = resultado

                    # Verifica se usuário está ativo
                    if not ativo or int(ativo) != 1:
                        self.label_erro.configure(text="Usuário desativado.")
                        return

                    # Valida a senha
                    if gerar_hash(senha) == senha_hash_banco: # Compara hash da senha
                        self.login_sucesso = True # Define sucesso do login
                        self.usuario_logado = usuario # Armazena usuário logado
                        self.nivel_acesso = nivel_acesso # Armazena nível de acesso
                        self.nome_completo = nome_completo # Armazena nome completo
                        self.primeiro_nome = nome_completo.split()[0] # Extrai primeiro nome
                        self.setor = setor # Armazena setor do usuário
                        self.destroy()
                    
                        print(f"Login bem-sucedido para {usuario} com nível {nivel_acesso}.")
                    else:
                        self.label_erro.configure(text="Senha incorreta.")
                else:
                    self.label_erro.configure(text="Usuário não encontrado.")

        except Exception as e:
            self.label_erro.configure(text="Erro ao acessar o banco.")
            print("Erro de conexão:", e)

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
    print("Login sucesso:", app.login_sucesso)
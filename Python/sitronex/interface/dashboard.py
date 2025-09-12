import customtkinter as ctk
from interface.icones.icones import obter_icon

class DashboardWindow(ctk.CTk):
    def __init__(self, usuario, nivel_acesso, setor):
        super().__init__()

        self.usuario = usuario # Armazena usuário logado
        self.nivel_acesso = nivel_acesso # Armazena nível de acesso
        self.setor = setor # Armazena setor do usuário
        self.title(f"Sitronex - Dashboard ({self.usuario})")
        self.geometry("1280x720")
        self.minsize(900, 550)
        self.iconbitmap(obter_icon())

        self._set_appearance()
        self._criar_widgets()
        
        self.protocol("WM_DELETE_WINDOW", self.destroy)  # Fecha a janela corretamente
        self.mainloop()

    def _set_appearance(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

    def _criar_widgets(self):
        # Barra superior com os departamentos/setores
        self.frame_top = ctk.CTkFrame(self, height=50)
        self.frame_top.pack(side="top", fill="x")
        
        boas_vindas = ctk.CTkLabel(self.frame_top, text=f"Bem-vindo, {self.usuario}", font=("Arial", 14, "bold"))
        boas_vindas.pack(side="top", padx=10)

        self.departamentos = [
            "Geral", "Recursos Humanos", "Financeiro", "Vendas", "Estoque",
            "Compras/Fornecedores", "TI/Sistema", "Relatórios/BI",
            "Marketing/CRM", "Jurídico/Contratos", "Logística"
        ]

        self.botoes_departamento = {}
        for dept in self.departamentos:
            btn = ctk.CTkButton(self.frame_top, text=dept, command=lambda d=dept: self._selecionar_departamento(d))
            btn.pack(side="left", padx=6, pady=10)
            self.botoes_departamento[dept] = btn

        # Área principal com lateral e conteúdo
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True)

        self.frame_lateral = ctk.CTkFrame(self.frame_principal, width=220)
        self.frame_lateral.pack(side="left", fill="y")

        self.frame_conteudo = ctk.CTkFrame(self.frame_principal)
        self.frame_conteudo.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Mostra o setor inicial
        self._selecionar_departamento(self.setor if self.setor in self.departamentos else "Geral")

    def _selecionar_departamento(self, departamento):
        for widget in self.frame_lateral.winfo_children():
            widget.destroy()
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        funcoes = []

        if departamento == "Geral":
            funcoes = [
                "Painel de controle", "Análises de acesso",
                "Logs e ações", "Configurações administrativas"
            ]
        elif departamento == "Recursos Humanos":
            funcoes = [
                "Cadastro de funcionários", "Controle de ponto",
                "Avaliações de desempenho", "Histórico de acessos"
            ]
        elif departamento == "Financeiro":
            funcoes = [
                "Fluxo de caixa", "Contas a pagar/receber",
                "Relatórios financeiros", "Integração bancária (simulada)"
            ]
        elif departamento == "Vendas":
            funcoes = [
                "Cadastro de clientes", "Pedidos de venda",
                "Ranking de produtos", "Metas e comissões"
            ]
        elif departamento == "Estoque":
            funcoes = [
                "Entradas e saídas", "Estoque mínimo",
                "Validade e lote", "Reposição automática"
            ]
        elif departamento == "Compras/Fornecedores":
            funcoes = [
                "Cadastro de fornecedores", "Ordens de compra",
                "Histórico de compras", "Comparação de preços"
            ]
        elif departamento == "TI/Sistema":
            funcoes = [
                "Usuários e permissões", "Backup e restauração",
                "Logs do sistema", "Modo offline"
            ]
        elif departamento == "Relatórios/BI":
            funcoes = [
                "Relatórios customizados", "Dashboard com gráficos",
                "Relatórios por e-mail", "Análises preditivas"
            ]
        elif departamento == "Marketing/CRM":
            funcoes = [
                "Campanhas de marketing", "Contato com clientes",
                "Análise de satisfação"
            ]
        elif departamento == "Jurídico/Contratos":
            funcoes = [
                "Gerenciamento de contratos", "Processos em andamento"
            ]
        elif departamento == "Logística":
            funcoes = [
                "Rastreamento de entregas", "Rotas e transporte"
            ]

        for funcao in funcoes:
            btn = ctk.CTkButton(self.frame_lateral, text=funcao, command=lambda f=funcao: self._mostrar_conteudo(f))
            btn.pack(fill="x", pady=5, padx=10)

        if funcoes:
            self._mostrar_conteudo(funcoes[0])

    def _mostrar_conteudo(self, funcao):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(
            self.frame_conteudo,
            text=f"Conteúdo: {funcao}",
            font=("Arial", 20)
        )
        label.pack(pady=20, padx=20)

if __name__ == "__main__":
    app = DashboardWindow(usuario="admin", nivel_acesso="admin")
    app.mainloop()
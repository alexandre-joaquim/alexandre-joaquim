from interface.gui_login import LoginWindow
from interface.dashboard import DashboardWindow

def main():
    login_app = LoginWindow()
    login_app.mainloop()
    
    
    # Se o login foi bem-sucedido, abre o dashboard
    # Caso contrário, encerra o sistema

    if login_app.login_sucesso:
        print(f"Login aprovado! Usuário: {login_app.usuario_logado}")
        dashboard = DashboardWindow(
            usuario=login_app.primeiro_nome,
            nivel_acesso=login_app.nivel_acesso,
            setor=login_app.setor
        )
        dashboard.mainloop()
    else:
        print("Login cancelado ou inválido. Encerrando sistema.")
        exit(0)
if __name__ == "__main__":
    main()
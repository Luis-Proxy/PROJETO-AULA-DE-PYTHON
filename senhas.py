import flet as ft
import random
import string

# Senha mestre usada para liberar o acesso ao programa
MASTER_PASSWORD = "admin123"


# Função principal do Flet (ponto de entrada do app)
def main(page: ft.Page):
    # Configurações da janela
    page.title = "Gerador de Senhas"
    page.window_width = 400
    page.window_height = 500
    page.window_resizable = False

    # ------------------ TELA DE LOGIN ------------------
    def login_screen():
        # Campo para digitar a senha (oculto por segurança)
        senha_input = ft.TextField(
            password=True, 
            can_reveal_password=True,  # permite mostrar/ocultar
            label="Senha Mestre"
        )

        # Texto de erro caso a senha esteja incorreta
        erro_text = ft.Text("", color="red")

        # Função que valida a senha digitada
        def validar(e):
            if senha_input.value == MASTER_PASSWORD:
                main_screen()   # abre a tela principal se acertar
            else:
                erro_text.value = "Senha incorreta!"
                page.update()

        # Botão de login
        btn_login = ft.ElevatedButton("Entrar", on_click=validar)

        # Limpa a tela e adiciona os componentes do login
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("🔐 Acesso Restrito", size=22, weight="bold"),
                    senha_input,
                    btn_login,
                    erro_text
                ],
                horizontal_alignment="center",
                alignment="center"
            )
        )

    # ------------------ TELA PRINCIPAL ------------------
    def main_screen():
        # Slider para escolher o tamanho da senha
        tamanho_slider = ft.Slider(
            min=1, max=20, divisions=19, value=12,
            label="Tamanho: {value}"
        )

        # Checkboxes para escolher o que a senha deve conter
        chk_maius = ft.Checkbox(label="Letras maiúsculas (A-Z)", value=True)
        chk_minus = ft.Checkbox(label="Letras minúsculas (a-z)", value=True)
        chk_num = ft.Checkbox(label="Números (0-9)", value=True)
        chk_esp = ft.Checkbox(label="Caracteres especiais (!, @, #, ...)", value=True)

        # Campo onde a senha final será exibida
        senha_output = ft.TextField(label="Senha Gerada", read_only=True)

        # Função que gera a senha
        def gerar_senha(e):
            chars = ""  # conjunto de caracteres que serão usados

            # Adiciona tipos de caracteres conforme os checkboxes marcados
            if chk_maius.value:
                chars += string.ascii_uppercase
            if chk_minus.value:
                chars += string.ascii_lowercase
            if chk_num.value:
                chars += string.digits
            if chk_esp.value:
                chars += "!@#$%&*()-_=+{}[]<>?"

            # Se nenhum tipo foi selecionado, avisa o usuário
            if chars == "":
                senha_output.value = "Selecione ao menos 1 tipo!"
                page.update()
                return

            # Define o tamanho e gera uma senha aleatória
            tamanho = int(tamanho_slider.value)
            senha = ''.join(random.choice(chars) for _ in range(tamanho))

            # Mostra a senha gerada no campo
            senha_output.value = senha
            page.update()

        # Função para copiar a senha para a área de transferência
        def copiar_senha(e):
            if senha_output.value:
                page.set_clipboard(senha_output.value)  # copia
                page.snack_bar = ft.SnackBar(ft.Text("Senha copiada!"))
                page.snack_bar.open = True
                page.update()

        # Limpa a tela e mostra a interface principal
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("🔑 Gerador de Senhas", size=22, weight="bold"),

                    ft.Text("Escolha o tamanho da senha:"),
                    tamanho_slider,

                    ft.Text("Selecione o que incluir:"),
                    chk_maius,
                    chk_minus,
                    chk_num,
                    chk_esp,

                    ft.ElevatedButton("Gerar Senha", on_click=gerar_senha),
                    senha_output,
                    ft.ElevatedButton("Copiar Senha", on_click=copiar_senha)
                ],
                scroll="adaptive"  # permite rolagem se necessário
            )
        )

    # Quando o programa abre, inicia pela tela de login
    login_screen()


# Inicia o app
ft.app(target=main)

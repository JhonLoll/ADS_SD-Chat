import flet as ft

class ServerConfig(ft.AlertDialog):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)

        self.page = page
        self.title = "Configurações do Servidor"
        self.content = ft.Column(
            [
                ft.Text("Configurações do servidor"),
                ft.Row(
                    [
                        ft.TextField(label="Host", width=200),
                        ft.TextField(label="Porta", width=100),
                    ]
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("Salvar", on_click=self.save_config),
                        ft.ElevatedButton("Cancelar", on_click=self.close),
                    ]
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    # Método para salvar as configurações do servidor
    def save_config(self, e):
        host = self.content.controls[1].controls[0].value
        port = self.content.controls[1].controls[1].value

        # Aqui você pode adicionar a lógica para salvar as configurações do servidor
        print(f"Configurações salvas: Host={host}, Porta={port}")

        self.close()

    # 


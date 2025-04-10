import flet as ft
from datetime import datetime

class Message:
    def __init__(self, sender: str, content: str, message_type: str = "text"):
        self.sender = sender
        self.content = content
        self.message_type = message_type
        self.timestamp = datetime.now()

class ChatMessage(ft.Row):
    def __init__(self, message: Message, **kwargs):
        super().__init__(**kwargs)

        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_iniciais(message.sender), 
                size=20, color=ft.Colors.WHITE), 
                bgcolor=self.get_avatar_color(message.sender),
            ),
            ft.Column(
                [
                    ft.Text(
                        message.sender,
                        weight=ft.FontWeight.BOLD,
                        size=12,
                    ),
                    ft.Text(
                        message.content,
                        size=14,
                        selectable=True,
                    ),
                ],
                tight=True,
                spacing=5,
                wrap=True,
            )
        ]

    def get_iniciais(self, name: str):
        if name:
            return name[:1].capitalize()
        else:
            return "Anonymous"
        
    def get_avatar_color(self, name: str):
        list_colors = [
            ft.Colors.RED_100,
            ft.Colors.GREEN_100,
            ft.Colors.BLUE_100,
            ft.Colors.YELLOW_100,
            ft.Colors.PURPLE_100,
        ]

        if name:
            return list_colors[hash(name) % len(list_colors)]
        else:
            return ft.Colors.GREY_100
        
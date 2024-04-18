import flet as ft


def content_sizes(data):
    return [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Количество: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(f"{data['quantity']}\xa0шт.", ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
        ft.Divider(),
        ft.ResponsiveRow(
            [
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Высота: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['height']}\xa0мм", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Ширина: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['width']}\xa0мм", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Размер: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['size']}\xa0м²", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]


def content_comments_and_list_files(data):
    comment_1, comment_2 = data['comments']
    return [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Комментарий для верстки:\n', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(comment_1, ft.TextStyle(weight=ft.FontWeight.W_700)),
            ],
            col={'xs': 12, 'sm': 4}
        ),
        ft.Divider(),
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Комментарий для производства:\n', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(comment_2, ft.TextStyle(weight=ft.FontWeight.W_700)),
            ],
            col={'xs': 12, 'sm': 4}
        ),
        ft.Divider(),
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Список файлов макета: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(f"{data['upload_files']}", ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        )
    ]
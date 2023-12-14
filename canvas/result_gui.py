import flet as ft
from other_func import card_result


def content_material(data):
    return [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Материал: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['material']['name'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
        ft.Divider(),
        ft.ResponsiveRow(
            [
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Себестоимость\xa0(м²): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['material']['price']}\xa0₽", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 6}
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Стоимость продажи\xa0(м²): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['material']['sale_price']}\xa0₽", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 6}
                ),
            ]
        )
    ]


def content_processing(data):
    processing_content = [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Обработка: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['processing']['type'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
        ft.Divider(),
        ft.ResponsiveRow(
            [
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Себестоимость\xa0(м²): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['processing']['price']}\xa0₽", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 6}
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Стоимость продажи\xa0(м²): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(
                            f"{data['processing']['sale_price']}\xa0₽", ft.TextStyle(weight=ft.FontWeight.W_700)
                        ),
                    ],
                    col={'xs': 12, 'sm': 6}
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    ]
    return processing_content


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


def content_consumables(data):
    consumption = []
    
    if data['material']['consumption'] or data['processing']['consumption']:
        consumption.extend([
            ft.Text('Расходные материалы', text_align=ft.TextAlign.CENTER),
            ft.Divider()
        ])
    if data['material']['consumption']:
        consumption.extend([
            ft.ResponsiveRow(
                [
                    ft.Text(
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan('Материал: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                            ft.TextSpan(data['material']['full_name'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                    ft.Text(
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan('Расход: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                            ft.TextSpan(
                                f"{data['material']['consumption']}\xa0м²", ft.TextStyle(weight=ft.FontWeight.W_700)
                            ),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ])
    if data['processing']['consumption']:
        consumption.extend([
            ft.Divider(),
            ft.ResponsiveRow(
                [
                    ft.Text(
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan('Материал обработки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                            ft.TextSpan(data['processing']['material'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                    ft.Text(
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan('Расход: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                            ft.TextSpan(
                                f"{data['processing']['consumption']}\xa0м", ft.TextStyle(weight=ft.FontWeight.W_700)
                            ),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ])
    return consumption


def result_content(data):
    list_content = []
    list_content.extend(card_result(content_material(data), 'Материал'))
    list_content.extend(card_result(content_processing(data), 'Обработка'))
    list_content.extend(card_result(content_sizes(data), 'Общие параметры'))
    consumables = content_consumables(data)
    if consumables:
        list_content.extend(card_result(consumables, 'Расходные материалы'))
    
    return ft.Container(
        content=ft.Column(
            controls=list_content,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        
        ),
    )

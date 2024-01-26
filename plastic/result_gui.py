import flet as ft
from other_func import card_result


def content_material(data):
    content_list = [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Материал: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['material']['name'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
    ]
    if data['material']['print_quality']:
        content_list.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Качество печати: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['material']['print_quality'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    if data['material']['color_material']:
        content_list.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Цвет плёнки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['material']['color_material'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    content_list.extend(
        [
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
                            ft.TextSpan(f"{data['material']['sale_price']}\xa0₽",
                                        ft.TextStyle(weight=ft.FontWeight.W_700)),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                ]
            )
        ]
    )
    return content_list


def content_processing(data):
    content_process = [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Вид обработки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['processing']['processing'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
    ]
    if data['processing']['sampling_method']:
        content_process.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Вид выборки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['processing']['sampling_method'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    if data['processing']['sampling_complexity']:
        content_process.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Сложность выборки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['processing']['sampling_complexity'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    if data['processing']['mounting_plastic']:
        content_process.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Монтажная пленка: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['processing']['mounting_plastic'],
                                ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    if data['processing']['processing'] == 'Резка с запасом':
        metric = 'м'
    else:
        metric = 'м²'
    content_process.extend(
        [
            ft.Divider(),
            ft.ResponsiveRow(
                [
                    ft.Text(
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan(f'Себестоимость\xa0({metric}): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                            ft.TextSpan(f"{data['processing']['price']}\xa0₽",
                                        ft.TextStyle(weight=ft.FontWeight.W_700)),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                    ft.Text(
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan(f'Стоимость продажи\xa0({metric}): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                            ft.TextSpan(f"{data['processing']['sale_price']}\xa0₽",
                                        ft.TextStyle(weight=ft.FontWeight.W_700)),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]
    )
    return content_process


def content_lamination(data):
    if data['processing']['lamination']:
        return [
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Ламинация: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['processing']['lamination'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
            ft.Divider(),
            ft.ResponsiveRow(
                [
                    ft.Text(
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan(f'Себестоимость\xa0(м²): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                            ft.TextSpan(f"{data['processing']['price']}\xa0₽",
                                        ft.TextStyle(weight=ft.FontWeight.W_700)),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                    ft.Text(
                        text_align=ft.TextAlign.CENTER,
                        spans=[
                            ft.TextSpan(f'Стоимость продажи\xa0(м²): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                            ft.TextSpan(f"{data['processing']['sale_price']}\xa0₽",
                                        ft.TextStyle(weight=ft.FontWeight.W_700)),
                        ],
                        col={'xs': 12, 'sm': 6}
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            
        ]
    else:
        return None


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


def result_content(data):
    list_content = []
    list_content.extend(card_result(content_material(data), 'Материал'))
    list_content.extend(card_result(content_processing(data), 'Обработка'))
    content_lamin = content_lamination(data)
    if content_lamin:
        list_content.extend(card_result(content_lamin, 'Ламинация'))
    list_content.extend(card_result(content_sizes(data), 'Общие параметры'))
    
    return ft.Container(
        content=ft.Column(
            controls=list_content,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        
        ),
    )

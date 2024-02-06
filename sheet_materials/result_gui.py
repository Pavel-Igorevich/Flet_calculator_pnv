import flet as ft
from other_func import card_result
from plastic import result_gui as plastic_result


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
    if data['material']['type']:
        content_list.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Вид материала: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['material']['type'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    content_list.append(
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Толщина материала: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['material']['thickness'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
    )
    if data['material']['edge']:
        content_list.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Кромка: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['material']['edge'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    if data['material']['color']:
        content_list.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Цвет композита: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['material']['color'], ft.TextStyle(weight=ft.FontWeight.W_700)),
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
    return [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Вид резки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['processing']['type_cut'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Накатка пленки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['processing']['rolling_film'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Держатель: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['processing']['holder'], ft.TextStyle(weight=ft.FontWeight.W_700)),
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
                        ft.TextSpan(f"{data['processing']['sale_price']}\xa0₽",
                                    ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 6}
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    ]


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


def content_backlighting(data):
    content_list = [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Вид подсветки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['backlighting']['type'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
    ]
    if data['backlighting']['lightbox_thickness']:
        content_list.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Толщина лайтбокса: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(
                        f"{data['backlighting']['lightbox_thickness']}\xa0мм", ft.TextStyle(weight=ft.FontWeight.W_700)
                    ),
                ]
            )
        )
    if data['backlighting']['type'] != 'Не требуется':
        content_list.extend(
            [
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Цвет света: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(data['backlighting']['color'],
                                    ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ]
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Вид света: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(data['backlighting']['type_light'],
                                    ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ]
                )
            ]
        )
    if data['backlighting']['cable']:
        content_list.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan(
                        'Дополнительный кабель (без\xa0учета\xa05\xa0комплектных\xa0метров): ',
                        ft.TextStyle(weight=ft.FontWeight.W_200)
                    ),
                    ft.TextSpan(f"{data['backlighting']['cable']}\xa0м", ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            )
        )
    return content_list


# def content_consumables(data):
#     consumption = []
#
#     if data['material']['consumption'] or data['processing']['consumption']:
#         consumption.extend([
#             ft.Text('Расходные материалы', text_align=ft.TextAlign.CENTER),
#             ft.Divider()
#         ])
#     if data['material']['consumption']:
#         consumption.extend([
#             ft.ResponsiveRow(
#                 [
#                     ft.Text(
#                         text_align=ft.TextAlign.CENTER,
#                         spans=[
#                             ft.TextSpan('Материал: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
#                             ft.TextSpan(data['material']['full_name'], ft.TextStyle(weight=ft.FontWeight.W_700)),
#                         ],
#                         col={'xs': 12, 'sm': 6}
#                     ),
#                     ft.Text(
#                         text_align=ft.TextAlign.CENTER,
#                         spans=[
#                             ft.TextSpan('Расход: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
#                             ft.TextSpan(
#                                 f"{data['material']['consumption']}\xa0м²", ft.TextStyle(weight=ft.FontWeight.W_700)
#                             ),
#                         ],
#                         col={'xs': 12, 'sm': 6}
#                     ),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#             )
#         ])
#     if data['processing']['consumption']:
#         consumption.extend([
#             ft.Divider(),
#             ft.ResponsiveRow(
#                 [
#                     ft.Text(
#                         text_align=ft.TextAlign.CENTER,
#                         spans=[
#                             ft.TextSpan('Материал обработки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
#                             ft.TextSpan(data['processing']['material'], ft.TextStyle(weight=ft.FontWeight.W_700)),
#                         ],
#                         col={'xs': 12, 'sm': 6}
#                     ),
#                     ft.Text(
#                         text_align=ft.TextAlign.CENTER,
#                         spans=[
#                             ft.TextSpan('Расход: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
#                             ft.TextSpan(
#                                 f"{data['processing']['consumption']}\xa0м", ft.TextStyle(weight=ft.FontWeight.W_700)
#                             ),
#                         ],
#                         col={'xs': 12, 'sm': 6}
#                     ),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#             ),
#         ])
#     return consumption

def card_general_prices(data):
    return [
        ft.Text(
            'Листовые материалы',
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(weight=ft.FontWeight.W_900)
        ),
        ft.ResponsiveRow(
            [
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Общая себестоимость: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['sheet_main_price']}\xa0мм", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Коэффициент: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['coefficient']}\xa0мм", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Общая стоимость: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['sheet_main_sale_price']}\xa0м²", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Divider(),
        ft.Text(
            'Плёнка',
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(weight=ft.FontWeight.W_900)
        ),
        ft.ResponsiveRow(
            [
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Общая себестоимость: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(f"{data['plastic']['main_price']}\xa0мм", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Коэффициент: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(
                            f"{data['plastic']['coefficient']}\xa0мм", ft.TextStyle(weight=ft.FontWeight.W_700)
                        ),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
                ft.Text(
                    text_align=ft.TextAlign.CENTER,
                    spans=[
                        ft.TextSpan('Общая стоимость: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                        ft.TextSpan(
                            f"{data['plastic']['main_sale_price']}\xa0м²", ft.TextStyle(weight=ft.FontWeight.W_700)
                        ),
                    ],
                    col={'xs': 12, 'sm': 4}
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    ]


def result_content(data):
    list_content = []
    list_content.extend(card_result(content_material(data), 'Материал'))
    list_content.extend(card_result(content_processing(data), 'Обработка'))
    list_content.extend(card_result(content_backlighting(data), 'Световое исполнение'))
    if data.get('plastic'):
        list_content.extend(card_result(plastic_result.content_material(data['plastic']), 'Материал плёнки'))
        list_content.extend(card_result(plastic_result.content_processing(data['plastic']), 'Обработка плёнки'))
        content_lamin = plastic_result.content_lamination(data['plastic'])
        if content_lamin:
            list_content.extend(card_result(content_lamin, 'Ламинация плёнки'))
    list_content.extend(card_result(content_sizes(data), 'Общие параметры'))
    if data.get('plastic'):
        list_content.extend(card_result(card_general_prices(data), 'Сводка стоимостей'))
    return ft.Container(
        content=ft.Column(
            controls=list_content,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        
        ),
    )

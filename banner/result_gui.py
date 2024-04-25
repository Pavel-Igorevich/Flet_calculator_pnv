import flet as ft

from other_func import card_result
from results_other_func import content_sizes, content_comments_and_list_files


def price_element(price, sale_price, label="м²"):
    return ft.ResponsiveRow(
        [
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan(f'Себестоимость\xa0({label}): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    # ft.TextSpan(f"{data['material']['price']}\xa0₽", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ft.TextSpan(f"{price}\xa0₽", ft.TextStyle(weight=ft.FontWeight.W_700)),
                ],
                col={'xs': 12, 'sm': 6}
            ),
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan(f'Стоимость продажи\xa0({label}): ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    # ft.TextSpan(f"{data['material']['sale_price']}\xa0₽", ft.TextStyle(weight=ft.FontWeight.W_700)),
                    ft.TextSpan(f"{sale_price}\xa0₽", ft.TextStyle(weight=ft.FontWeight.W_700)),
                ],
                col={'xs': 12, 'sm': 6}
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )


def content_material(data):
    return [
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Материал: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['material']['name'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
        ft.Text(
            text_align=ft.TextAlign.CENTER,
            spans=[
                ft.TextSpan('Качество печати: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                ft.TextSpan(data['material']['print_quality'], ft.TextStyle(weight=ft.FontWeight.W_700)),
            ]
        ),
        ft.Divider(),
        price_element(data['material']['price'], data['material']['sale_price'])
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
    ]
    if data['processing']['sides']:
        processing_content.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Стороны обработки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['processing']['sides'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    if data['processing']['welding_step']:
        processing_content.append(
            ft.Text(
                text_align=ft.TextAlign.CENTER,
                spans=[
                    ft.TextSpan('Шаг сварки: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                    ft.TextSpan(data['processing']['welding_step'], ft.TextStyle(weight=ft.FontWeight.W_700)),
                ]
            ),
        )
    processing_content.append(ft.Divider())
    processing_content.append(
        price_element(data['processing']['price'], data['processing']['sale_price'], "шт.")
    ),
    return processing_content


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
    list_content.extend(card_result(content_comments_and_list_files(data), 'Комментарии и файлы макета'))
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

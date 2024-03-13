import flet as ft

from banner.result_gui import result_content as banner_result
from canvas.result_gui import result_content as canvas_result
from list_orders import ORDERS
from plastic.result_gui import result_content as plastic_result
from sheet_materials.result_gui import result_content as sheet_materials_result


class OrdersGUI(ft.UserControl):

    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.card_dict = {}
        self.default_card = None

    def show_details(self, event):
        if event.control.key in ORDERS:
            data = ORDERS[event.control.key]
            self.main_price.text = f"{data['main_price']}\xa0₽"
            self.main_sale_price.text = f"{data['main_sale_price']}\xa0₽"
            self.coefficient.text = data['coefficient']
            if 'banner' == data['result_content']:
                content_data = banner_result(data)
                self.page.dialog.content = content_data
            elif 'canvas' == data['result_content']:
                content_data = canvas_result(data)
                self.page.dialog.content = content_data
            elif 'sheet_materials' == data['result_content']:
                content_data = sheet_materials_result(data)
                self.page.dialog.content = content_data
            elif 'plastic' == data['result_content']:
                content_data = plastic_result(data)
                self.page.dialog.content = content_data
            self.page.dialog.open = True
            self.page.update()

    def delete_order(self, event):
        if event.control.key in ORDERS:
            del ORDERS[event.control.key]
            self.card_dict[event.control.key].visible = False
        if not ORDERS:
            self.default_card.visible = True
        self.update()

    def create_card(self, key, content_card):
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    content_card
                ),
                padding=10,
            )
        )
        self.card_dict[key] = card
        return card

    def create_fields(self):
        list_orders = []
        self.default_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(
                                'Нет расчетов', weight=ft.FontWeight.W_500
                            ),
                            subtitle=ft.Text(
                                "ожидание расчетов",
                                weight=ft.FontWeight.W_200
                            ),

                        )
                    ],
                ),
                padding=10,
                alignment=ft.alignment.center,
            )
        )
        visible_def_card = False
        for order, data in ORDERS.items():
            content = [
                ft.ListTile(
                    title=ft.Text(order, weight=ft.FontWeight.W_500),
                    subtitle=ft.Text(
                        f"Стоимость продажи: {data['main_sale_price']}\xa0₽",
                        weight=ft.FontWeight.W_200
                    ),
                ),
                ft.Row(
                    [
                        ft.TextButton(
                            "Подробнее",
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.AMBER,
                                color=ft.colors.BLACK
                            ),
                            key=order,
                            on_click=self.show_details
                        ),
                        ft.TextButton(
                            "Удалить",
                            style=ft.ButtonStyle(
                                bgcolor=ft.colors.RED_500,
                                color=ft.colors.WHITE
                            ),
                            key=order,
                            on_click=self.delete_order
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ]
            list_orders.append(self.create_card(order, content))
        if not list_orders:
            visible_def_card = True
        self.default_card.visible = visible_def_card
        list_orders.append(self.default_card)
        return list_orders

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=self.create_fields(),
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            ),
            padding=20,
            margin=10,
            width=500
        )

from datetime import datetime

import flet as ft

from calculations.canvas_calc import main_calc
from canvas.result_gui import result_content
from data import MAIN_DATA
from list_orders import ORDERS
from other_func import card, checking_size, checking_quantity, load_files, create_general_params, \
    create_comments_and_layout_files_fields


class CanvasGUI(ft.UserControl):
    DATA = MAIN_DATA['Холст']

    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.material = None
        self.processing = None
        self.height_canvas = None
        self.width_canvas = None
        self.quantity = None

        self.load_file_btn = None
        self.load_file_text = None
        self.pick_files_dialog = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        self.upload_files = []
        self.comment_field_1, self.comment_field_2 = None, None

        self.button_send = None

    def checking_size(self, event):
        checking_size(event)
        self.update()

    def checking_quantity(self, event):
        checking_quantity(event)
        self.update()

    def load_file(self, e: ft.FilePickerResultEvent):
        self.load_file_text.value, self.upload_files = load_files(e, "Макет_Холста")
        self.update()

    def create_fields_general_params(self):
        self.width_canvas, self.height_canvas, self.quantity = (
            create_general_params()
        )
        self.width_canvas.on_change = self.checking_size
        self.height_canvas.on_change = self.checking_size
        self.quantity.on_change = self.checking_quantity

        card_params = card(
            'Общие параметры',
            [
                self.width_canvas,
                self.height_canvas,
                self.quantity
            ]
        )
        card_comments, contents = create_comments_and_layout_files_fields()

        self.comment_field_1, self.comment_field_2, self.load_file_text, self.load_file_btn = contents
        self.load_file_btn.on_click = lambda _: self.pick_files_dialog.pick_files(
            allow_multiple=True
        )
        return card_params, card_comments

    def create_fields(self):
        material_choices = list(self.DATA['Материал'].keys())

        self.material = ft.Dropdown(
            label="Материал холста",
            options=[
                ft.dropdown.Option(choice) for choice in material_choices
            ],
            value=material_choices[0],
            alignment=ft.alignment.center,
        )

        processing_choices = list(self.DATA['Обработка'].keys())

        self.processing = ft.Dropdown(
            label="Вид обработки",
            options=[
                ft.dropdown.Option(choice) for choice in processing_choices
            ],
            value=processing_choices[0],
            alignment=ft.alignment.center,
        )
        column_controls = [
            ft.Row(
                [ft.Text('Холст', size=25)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            card("Материал", [self.material, ]),
            card("Обработка", [self.processing, ])
        ]
        column_controls.extend(self.create_fields_general_params())
        self.button_send = ft.ElevatedButton(
            'Рассчитать',
            style=ft.ButtonStyle(
                padding={ft.MaterialState.DEFAULT: 20}, bgcolor=ft.colors.AMBER, color=ft.colors.BLACK
            ),
            on_click=self.checking_entered_values
        )
        column_controls.append(self.button_send)
        return column_controls

    def checking_entered_values(self, _event):
        checked_var = True
        if self.page.banner:
            self.page.banner.open = False
            self.page.update()

        if self.height_canvas.error_text or self.width_canvas.error_text or self.quantity.error_text:
            checked_var = False
        else:
            for elem in [self.height_canvas, self.width_canvas, self.quantity]:
                if not elem.value:
                    elem.error_text = 'Не может быть пустым'
                    checked_var = False

        if not checked_var:
            self.page.banner.open = True
            self.page.update()
        else:
            data = main_calc(self.create_data())
            self.main_price.text = f"{data['main_price']}\xa0₽"
            self.main_sale_price.text = f"{data['main_sale_price']}\xa0₽"
            self.coefficient.text = data['coefficient']
            self.page.dialog.content = result_content(data)
            ORDERS[f'Холст - {datetime.now().strftime("%d.%m.%Y (%H:%M:%S)")}'] = data
            data['result_content'] = 'canvas'
            self.page.dialog.open = True
            self.page.banner.open = False
            self.page.update()
        self.update()

    def create_data(self):
        data = {
            'material': {
                'name': self.material.value,
            },
            'processing': {
                'type': self.processing.value,
            },
            'height': self.height_canvas.value,
            'width': self.width_canvas.value,
            'quantity': self.quantity.value,
        }
        if self.upload_files:
            data['upload_files'] = ", ".join(self.upload_files)
        else:
            data['upload_files'] = 'Файлы не добавлены'

        list_comments = []
        for comment in [self.comment_field_1, self.comment_field_2]:
            if self.comment_field_1.value:
                comment = comment.value
            else:
                comment = "Нет"
            list_comments.append(comment)
        data['comments'] = list_comments
        return data

    def build(self):
        self.create_fields()
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

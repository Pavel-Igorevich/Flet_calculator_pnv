from datetime import datetime
import flet as ft

from banner.result_gui import result_content
from calculations.banner_calc import main_calc
from data import MAIN_DATA
from list_orders import ORDERS
from other_func import card, checking_size, checking_quantity, load_files, create_general_params, \
    create_comments_and_layout_files_fields


class Banner:
    def __init__(self):
        self.data = MAIN_DATA['Баннер']
        self.data_material = self.data["Материал"]
        self.data_processing = self.data['Обработка']

        self.material, self.print_quality = None, None
        self.processing, self.welding_step, self.text_side, self.error_message_sides = None, None, None, None
        self.row_sides_icon = None
        self.side_data = None
        self.button_send = None

    @staticmethod
    def create_side_data():
        return {
            "Левая": {
                'obj': None,
                'icon': ft.icons.BORDER_LEFT
            },
            "Правая": {
                'obj': None,
                'icon': ft.icons.BORDER_RIGHT
            },
            "Верх": {
                'obj': None,
                'icon': ft.icons.BORDER_TOP
            },
            "Низ": {
                'obj': None,
                'icon': ft.icons.BORDER_BOTTOM
            },
            "Все стороны": {
                'obj': None,
                'icon': ft.icons.BORDER_OUTER
            },
            "По углам": {
                'obj': None,
                'icon': ft.icons.ALL_OUT
            }
        }

    def material_events(self):
        list_choices = list(self.data_material[self.material.value]['Качество печати'].keys())
        self.print_quality.options = [ft.dropdown.Option(quality) for quality in list_choices]
        self.print_quality.value = list_choices[0]

    def visible_welding_step(self):
        step = self.data_processing[self.processing.value].get('Шаг сварки')
        if step:
            steps = list(step.keys())
            self.welding_step.options = [ft.dropdown.Option(step) for step in steps]
            self.welding_step.value = steps[0]
            self.welding_step.visible = True

        else:
            self.welding_step.visible = False

    def visible_sides(self):
        if self.processing:
            sides = self.data_processing[self.processing.value].get('Сторона')
        else:
            sides = None

        if sides:
            self.text_side.visible = True
            self.row_sides_icon.visible = True
            for name_side in self.side_data.keys():
                check = False
                if name_side in sides:
                    check = True
                self.side_data[name_side]['obj'].visible = check
        else:
            for side_data in self.side_data.values():
                side_data['obj'].visible = False
            self.text_side.visible = False
            self.row_sides_icon.visible = False
            self.error_message_sides.visible = False

    def processing_events(self):
        self.visible_welding_step()
        self.visible_sides()

    def create_fields_material(self):
        material_choices = list(self.data_material.keys())
        default_material = material_choices[0]
        print_quality_choices = list(self.data_material[default_material]['Качество печати'].keys())

        self.material = ft.Dropdown(
            label="Материал баннера",
            options=[
                ft.dropdown.Option(material) for material in material_choices
            ],
            value=material_choices[0],
            alignment=ft.alignment.center,
        )
        self.print_quality = ft.Dropdown(
            label="Качество печати",
            options=[
                ft.dropdown.Option(quality) for quality in print_quality_choices
            ],
            value=print_quality_choices[0],
            alignment=ft.alignment.center,
        )
        return card('Материал', [self.material, self.print_quality])

    def remove_selection_side(self):
        for data in self.side_data.values():
            if data['obj'].selected:
                data['obj'].selected = False

    def chip_event_events(self, event):
        if event.control.tooltip in ('Все стороны', 'По углам'):
            self.remove_selection_side()
            self.side_data[event.control.tooltip]['obj'].selected = True
        else:
            list_sides = ['Левая', 'Правая', 'Верх', 'Низ']
            if all([self.side_data[side]['obj'].selected for side in list_sides]):
                self.remove_selection_side()
                self.side_data["Все стороны"]['obj'].selected = True
            else:
                for side in ('Все стороны', 'По углам'):
                    if self.side_data[side]['obj'].selected:
                        self.side_data[side]['obj'].selected = False
        if any([data['obj'].selected for data in self.side_data.values()]):
            self.error_message_sides.visible = False

    def create_sides_processing(self):
        elems = []
        for label, data in self.side_data.items():
            data['obj'] = ft.Chip(
                label=ft.Icon(data['icon'], size=20),
                selected_color=ft.colors.GREEN_200,
                col={"xs": 6, 'sm': 2},
                tooltip=label,
                visible=False
            )
            elems.append(data['obj'])
        self.row_sides_icon = ft.ResponsiveRow(elems, alignment=ft.MainAxisAlignment.CENTER, visible=False)

    def create_fields_processing(self):
        processing_choices = list(self.data_processing.keys())
        self.side_data = self.create_side_data()
        self.create_sides_processing()

        self.processing = ft.Dropdown(
            label="Обработка",
            options=[
                ft.dropdown.Option(processing) for processing in processing_choices
            ],
            value=processing_choices[0],
            alignment=ft.alignment.center,
        )
        self.welding_step = ft.Dropdown(
            label="Шаг сварки",
            options=[],
            alignment=ft.alignment.center,
            visible=False
        )
        self.text_side = ft.Row([ft.Text('Выбор стороны обработки')], alignment=ft.MainAxisAlignment.CENTER)
        self.error_message_sides = ft.Container(
            content=ft.Text('Необходимо выбрать стороны обработки', color=ft.colors.WHITE),
            alignment=ft.alignment.center,
            bgcolor=ft.colors.RED_ACCENT_200,
            border_radius=10,
            padding=10,
            visible=False
        )

        return card(
            'Обработка',
            [
                self.processing,
                self.welding_step,
                self.text_side,
                self.error_message_sides,
                self.row_sides_icon
            ]
        )

    def create_fields(self, fields_general_params=None, btn_send=True):
        column_controls = [
            ft.Row(
                [ft.Text('Баннер', size=25)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            self.create_fields_material(),
            self.create_fields_processing()
        ]
        if fields_general_params:
            column_controls.extend(fields_general_params)
        if btn_send:
            self.button_send = ft.ElevatedButton(
                'Рассчитать',
                style=ft.ButtonStyle(
                    padding={ft.MaterialState.DEFAULT: 20}, bgcolor=ft.colors.AMBER, color=ft.colors.BLACK
                ),
            )
            column_controls.append(self.button_send)
        self.visible_sides()
        self.visible_welding_step()
        return column_controls


class BannerGUI(ft.UserControl, Banner):

    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.height_banner = None
        self.width_banner = None
        self.quantity = None
        self.result_modal = None
        self.pick_files_dialog = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        self.upload_files = []

        self.comment_field_1, self.comment_field_2 = None, None

        self.load_file_btn = None
        self.load_file_text = None

    def load_file(self, e: ft.FilePickerResultEvent):
        self.load_file_text.value, self.upload_files = load_files(e, "Макет_Баннера")
        self.update()

    def checking_size(self, event):
        checking_size(event)
        self.update()

    def checking_quantity(self, event):
        checking_quantity(event)
        self.update()

    def create_fields_general_params(self):
        self.width_banner, self.height_banner, self.quantity = (
            create_general_params()
        )
        self.width_banner.on_change = self.checking_size
        self.height_banner.on_change = self.checking_size
        self.quantity.on_change = self.checking_quantity
        card_params = card(
            'Общие параметры',
            [
                self.width_banner,
                self.height_banner,
                self.quantity
            ]
        )
        card_comments, contents = create_comments_and_layout_files_fields()

        self.comment_field_1, self.comment_field_2, self.load_file_text, self.load_file_btn = contents
        self.load_file_btn.on_click = lambda _: self.pick_files_dialog.pick_files(
            allow_multiple=True
        )
        return card_params, card_comments

    def material_func(self, _event):
        self.material_events()
        self.update()

    def processing_func(self, _event):
        self.processing_events()
        self.update()

    def chip_event_func(self, event):
        self.chip_event_events(event)
        self.update()

    def create_on_change_events(self):
        self.material.on_change = self.material_func
        self.processing.on_change = self.processing_func
        self.button_send.on_click = self.checking_entered_values
        for data in self.side_data.values():
            data['obj'].on_select = self.chip_event_func

    def create_data(self):
        data = {
            'material': {
                'name': self.material.value,
                'print_quality': self.print_quality.value,
            },
            'processing': {
                'type': self.processing.value,
            },
            'height': self.height_banner.value,
            'width': self.width_banner.value,
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

        if self.data_processing[self.processing.value].get('Сторона'):
            processing_sides = [name_side for name_side, data in self.side_data.items() if data['obj'].selected]
            data['processing']['sides'] = ', '.join(processing_sides)
        else:
            data['processing']['sides'] = None

        if self.data_processing[self.processing.value].get('Шаг сварки'):
            data['processing']['welding_step'] = self.welding_step.value
        else:
            data['processing']['welding_step'] = None

        material = self.data_processing[self.processing.value].get('Материал')
        data['processing']['material'] = material

        return data

    def checking_entered_values(self, _event):
        checked_var = True
        if self.page.banner:
            self.page.banner.open = False
            self.page.update()

        if self.text_side.visible:
            if not any([data['obj'].selected for data in self.side_data.values()]):
                self.error_message_sides.visible = True
                checked_var = False
        if self.height_banner.error_text or self.width_banner.error_text or self.quantity.error_text:
            checked_var = False
        else:
            for elem in [self.height_banner, self.width_banner, self.quantity]:
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
            ORDERS[f'Баннер - {datetime.now().strftime("%d.%m.%Y (%H:%M:%S)")}'] = data
            data['result_content'] = 'banner'
            self.page.dialog.open = True
            self.page.banner.open = False
            self.page.update()
        self.update()

    def build(self):
        fields = self.create_fields(
            fields_general_params=self.create_fields_general_params()
        )
        self.create_on_change_events()
        return ft.Container(
            content=ft.Column(
                controls=fields,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            ),
            padding=20,
            margin=10,
            width=500
        )

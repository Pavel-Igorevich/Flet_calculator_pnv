from datetime import datetime

import flet as ft

from calculations.plastic_calc import main_calc as plastic_calc
from calculations.sheet_materials_calc import main_calc
from data import MAIN_DATA
from list_orders import ORDERS
from other_func import card, checking_size, checking_quantity, load_files, create_general_params, \
    create_comments_and_layout_files_fields
from plastic.plastic_gui import PlasticElements
from sheet_materials.result_gui import result_content


class SheetMaterials:
    not_required = 'Не требуется'
    data = MAIN_DATA['Листовые материалы']

    def __init__(self):
        self.data_material = SheetMaterials.data['Материал']
        self.data_backlighting = SheetMaterials.data['Световое исполнение']
        self.data_processing = SheetMaterials.data['Обработка']

        self.material = None
        self.material_type = None
        self.material_thickness = None
        self.material_color = None
        self.material_edge = None
        self.proces_type_cutting = None
        self.proces_rolling_film = None
        self.proces_holder = None
        self.backlighting = None
        self.backlighting_color = None
        self.backlighting_lightbox_thickness = None
        self.backlighting_neon_thickness = None
        self.backlighting_type_light = None
        self.default_type_light = list(self.data_backlighting['Вид света'].keys())
        self.backlighting_cable = None
        self.button_send = None

        self.plastic_class = PlasticElements()
        self.side_film_app = None

    def visible_type_mat(self):
        material_data = self.data_material[self.material.value]
        point_keys = list(material_data['Вид'].keys())
        if None in point_keys:
            self.material_type.value = None
            self.material_type.visible = False
        else:
            point_keys.sort()
            self.material_type.options = [ft.dropdown.Option(key) for key in point_keys]
            self.material_type.value = point_keys[0]
            self.material_type.visible = True
        edge_keys = material_data.get('Кромка')
        if edge_keys:
            self.material_edge.options = [ft.dropdown.Option(key) for key in edge_keys]
            self.material_edge.value = edge_keys[0]
            self.material_edge.visible = True
        else:
            self.material_edge.value = None
            self.material_edge.visible = False

    def visible_thickness_color_mat(self):
        material_data = self.data_material[self.material.value]
        if not self.material_type.value:
            key = None
        else:
            key = self.material_type.value
        thickness_keys = list(material_data['Вид'][key]['Толщина'].keys())
        if len(thickness_keys) == 1:
            self.material_thickness.options = [ft.dropdown.Option(key) for key in thickness_keys]
            self.material_thickness.value = thickness_keys[0]
            self.material_thickness.disabled = True
        else:
            self.material_thickness.disabled = False
            self.material_thickness.options = [ft.dropdown.Option(key) for key in thickness_keys]
            self.material_thickness.value = thickness_keys[0]
        color_keys = material_data['Вид'][key].get('Цвет')
        if color_keys:
            self.material_color.visible = True
        else:
            self.material_color.visible = False
            self.material_color.value = None

    def visible_proces_rolling_film(self):
        material_data = self.data_material[self.material.value]
        visible_roll_film = material_data.get('Накатка')
        if visible_roll_film is not None:
            self.proces_rolling_film.visible = visible_roll_film
            self.proces_rolling_film.value = self.not_required
        else:
            self.proces_rolling_film.visible = True

    def material_events(self):
        self.visible_type_mat()
        self.visible_thickness_color_mat()
        self.visible_proces_rolling_film()
        self.plastic_events()

    def type_mat_events(self):
        self.visible_thickness_color_mat()
        self.visible_side_film_app()

    def checking_cable(self):
        event = self.backlighting_cable
        if event.control.value:
            if event.control.value == '0':
                event.control.value = ''
            elif not event.control.value.isdigit():
                event.control.error_text = 'Необходимо целое число'
            else:
                event.control.error_text = ''

        else:
            event.control.error_text = ''

    def checking_thickness(self):
        event = self.backlighting_lightbox_thickness
        if len(event.control.value) == 0:
            event.control.error_text = 'Не может быть пустым'
        elif len(event.control.value) < 2 or not event.control.value.isdigit():
            event.control.error_text = 'Размер задается целым числом от 50'
        else:
            if int(event.control.value) < 50:
                event.control.error_text = 'Размер задается целым числом от 50'
            else:
                event.control.error_text = ''

    def create_data(self, general_params_data):
        visible_roll = self.data_material[self.material.value].get('Накатка')
        values_roll = self.proces_rolling_film.value if visible_roll is None or visible_roll else None
        if self.side_film_app.visible:
            value_side_film = self.side_film_app.value
        else:
            value_side_film = None
        data = {
            'material': {
                'name': self.material.value,
                'type': self.material_type.value,
                'thickness': self.material_thickness.value,
                'edge': self.material_edge.value,
                'color': self.material_color.value
            },
            'processing': {
                'type_cut': self.proces_type_cutting.value,
                'rolling_film': values_roll,
                'side_film': value_side_film,
                'holder': self.proces_holder.value
            },
            'backlighting': {
                'type': self.backlighting.value,
                'color': self.backlighting_color.value,
                'type_light': self.backlighting_type_light.value,
                'cable': self.backlighting_cable.value
            },
        }
        match self.backlighting.value:
            case 'Лайтбокс':
                data['backlighting']['thickness'] = int(self.backlighting_lightbox_thickness.value)
            case 'Гибкий неон':
                value = int(self.backlighting_neon_thickness.value.split(' ')[0])
                data['backlighting']['thickness'] = value
        if general_params_data:
            data.update(general_params_data)
        return data

    def create_data_plastic(self, general_params_data):
        data_plastic = self.plastic_class.create_data_elems()
        if isinstance(data_plastic, dict) and general_params_data:
            data_plastic.update(general_params_data)
        else:
            raise TypeError()
        return data_plastic

    def checking_plastic_values(self):
        if self.plastic_class.name.visible:
            return self.plastic_class.checking_values_elems()
        else:
            return True

    def checking_material_values(self):
        if self.material_color.visible and not self.material_color.value:
            if not self.material_color.error_text:
                self.material_color.error_text = 'Введите цвет композита'
            return False
        return True

    def checking_backlighting_cable_values(self):
        if self.backlighting_cable.visible and self.backlighting_cable.error_text:
            return False
        return True

    def checking_backlighting_lightbox_thickness(self):
        check = True
        if self.backlighting.value == 'Лайтбокс':
            thickness_data = self.backlighting_lightbox_thickness
            if not thickness_data.value:
                thickness_data.error_text = 'Не может быть пустым'
                check = False
            elif not thickness_data.value.isdigit():
                thickness_data.error_text = 'Количество задается целым числом'
                check = False
            else:
                thickness_data.error_text = ''
        return check

    def on_off_visible_backlighting(self, on: bool):
        self.backlighting_neon_thickness.visible = False
        self.backlighting_lightbox_thickness.visible = False
        self.backlighting_color.visible = on
        self.backlighting_type_light.visible = on
        self.backlighting_cable.visible = on
        self.backlighting_cable.value = None

    def visible_backlighting_param(self):
        if self.backlighting.value != self.not_required:
            self.on_off_visible_backlighting(on=True)

            if self.backlighting.value == "Гибкий неон":
                self.backlighting_neon_thickness.visible = True
                self.backlighting_type_light.options = [ft.dropdown.Option(self.backlighting.value)]
                self.backlighting_type_light.value = self.backlighting.value
            else:
                if self.backlighting.value == "Лайтбокс":
                    self.backlighting_lightbox_thickness.visible = True
                self.backlighting_type_light.options = [
                    ft.dropdown.Option(choice) for choice in self.default_type_light
                ]
                self.backlighting_type_light.value = self.default_type_light[0]
        else:
            self.on_off_visible_backlighting(on=False)

    def backlighting_events(self):
        self.visible_backlighting_param()

    def color_mat_events(self):
        self.material_color.error_text = ''
        if self.material.value == 'Композит' and self.material_type.value == 'Матовый':
            if not self.material_color.value:
                self.material_color.error_text = 'Введите цвет композита'

    def create_fields_material(self):
        material_choices = list(self.data_material.keys())
        default_material = material_choices[0]

        self.material = ft.Dropdown(
            label="Материал",
            options=[
                ft.dropdown.Option(material) for material in material_choices
            ],
            value=default_material,
            alignment=ft.alignment.center,
        )

        self.material_type = ft.Dropdown(
            label="Вид материала",
            options=[],
            value=None,
            alignment=ft.alignment.center,
            visible=False
        )

        self.material_thickness = ft.Dropdown(
            label="Толщина",
            options=[],
            value=None,
            alignment=ft.alignment.center,
        )

        self.material_color = ft.TextField(
            label="Цвет материала",
            visible=False,

        )
        self.material_edge = ft.Dropdown(
            label="Кромка",
            options=[],
            value=None,
            alignment=ft.alignment.center,
            visible=False
        )

        return card(
            'Материал',
            [self.material, self.material_type, self.material_thickness, self.material_color, self.material_edge]
        )

    def create_fields_process(self):
        process_cutting_choices = list(self.data_processing['Вид резки'].keys())
        self.proces_type_cutting = ft.Dropdown(
            label="Вид резки",
            options=[
                ft.dropdown.Option(choice) for choice in process_cutting_choices
            ],
            value=process_cutting_choices[0],
            alignment=ft.alignment.center,
        )

        process_film_choices = list(self.data_processing['Накатка пленки'].keys())
        self.proces_rolling_film = ft.Dropdown(
            label="Накатка пленки",
            options=[
                ft.dropdown.Option(choice) for choice in process_film_choices
            ],
            value=process_film_choices[0],
            alignment=ft.alignment.center,
        )
        self.side_film_app = ft.Dropdown(
            label="Сторона накатки",
            options=[
                ft.dropdown.Option(material) for material in ['Лицевая', 'Тыльная']
            ],
            value='Лицевая',
            alignment=ft.alignment.center,
            visible=False
        )

        proces_holder_choices = list(self.data_processing['Держатель'].keys())
        self.proces_holder = ft.Dropdown(
            label="Держатель",
            options=[
                ft.dropdown.Option(choice) for choice in proces_holder_choices
            ],
            value=proces_holder_choices[0],
            alignment=ft.alignment.center,
        )
        return card(
            'Обработка',
            [
                self.proces_type_cutting,
                self.proces_rolling_film,
                self.side_film_app,
                self.proces_holder
            ]
        )

    def create_fields_backlighting(self):
        backlighting_data = self.data_backlighting
        backlighting_choices = list(backlighting_data['Вид подсветки'].keys())
        self.backlighting = ft.Dropdown(
            label="Вид подсветки",
            options=[
                ft.dropdown.Option(choice) for choice in backlighting_choices
            ],
            value=backlighting_choices[0],
            alignment=ft.alignment.center,
        )
        self.backlighting_lightbox_thickness = ft.TextField(
            label="Толщина лайтбокса",
            suffix_text="мм",
        )
        data_backlighting_neon = self.data_backlighting["Вид подсветки"]["Гибкий неон"]["Толщина неона"]
        self.backlighting_neon_thickness = ft.Dropdown(
            label="Толщина неона",
            options=[
                ft.dropdown.Option(choice)
                for choice in data_backlighting_neon
            ],
            value=data_backlighting_neon[0],
            alignment=ft.alignment.center
        )
        backlighting_color_choices = list(self.data_backlighting['Цвет света'].keys())
        self.backlighting_color = ft.Dropdown(
            label="Цвет света",
            options=[ft.dropdown.Option(choice) for choice in backlighting_color_choices],
            alignment=ft.alignment.center,
            value=backlighting_color_choices[0]
        )

        self.backlighting_type_light = ft.Dropdown(
            label="Вид света",
            options=[],
            alignment=ft.alignment.center,
        )

        self.backlighting_cable = ft.TextField(
            label="Дополнительный провод",
            suffix_text="м",
            visible=False,
            hint_text=self.not_required,
            counter_text='В комплекте уже есть пять метров'
        )
        return card(
            'Световое исполнение',
            [
                self.backlighting,
                self.backlighting_lightbox_thickness,
                self.backlighting_neon_thickness,
                self.backlighting_color,
                self.backlighting_type_light,
                self.backlighting_cable
            ]
        )

    def plastic_material_events(self):
        self.plastic_class.visible_material_fields()

    def plastic_color_material_events(self):
        if self.plastic_class.color_material and self.plastic_class.color_material.value:
            self.plastic_class.color_material.error_text = ''

    def plastic_processing_events(self):
        self.plastic_class.visible_processing_fields()

    def plastic_sampling_events(self, event):
        self.plastic_class.visible_sampling_func(event)

    def visible_side_film_app(self):
        type_value = self.material_type.value
        if type_value and 'Прозрач' in type_value and self.proces_rolling_film.value != self.not_required:
            self.side_film_app.visible = True
        else:
            self.side_film_app.visible = False

    def create_fields_plastic(self):
        self.plastic_class.name = ft.Row(
            [ft.Text('Плёнка', size=25)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
        self.plastic_class.divider_top = ft.Divider()
        self.plastic_class.divider_down = ft.Divider()
        column_plastic = [
            self.plastic_class.divider_top,
            self.plastic_class.name,
            self.plastic_class.create_elements_material(),
            self.plastic_class.create_elements_processing(),
            self.plastic_class.divider_down
        ]
        self.plastic_class.visible_material_fields()
        self.plastic_class.visible_processing_fields()
        self.plastic_class.visible_elems(False)
        return column_plastic

    def plastic_events(self):
        check = bool(self.proces_rolling_film.value != self.not_required)
        plotter_name = 'Плоттер'
        if check:
            if self.proces_rolling_film.value == plotter_name:
                self.plastic_class.processing.options = [ft.dropdown.Option(plotter_name), ]
                self.plastic_class.processing.value = plotter_name
            else:
                self.plastic_class.processing.options = [ft.dropdown.Option('Резка с запасом'), ]
                self.plastic_class.processing.value = 'Резка с запасом'
            self.plastic_class.visible_processing_fields()
        self.plastic_class.visible_elems(check)
        self.visible_side_film_app()

    def create_fields(self, fields_general_params=None, btn_send=True):
        column_controls = [
            ft.Row(
                [ft.Text('Листовые материалы', size=25)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            self.create_fields_material(),
            self.create_fields_process(),
            self.create_fields_backlighting()
        ]
        column_plastic = self.create_fields_plastic()
        column_controls.extend(column_plastic)
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
        self.visible_backlighting_param()
        self.visible_type_mat()
        self.visible_thickness_color_mat()
        self.visible_proces_rolling_film()
        self.visible_side_film_app()
        return column_controls


class SheetMaterialsGUI(ft.UserControl, SheetMaterials):
    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.pick_files_dialog = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.pick_files_dialog)
        self.width_sheet, self.height_sheet, self.quantity = None, None, None
        self.page.update()
        self.upload_files = []

        self.comment_field_1, self.comment_field_2 = None, None
        self.load_file_btn = None
        self.load_file_text = None

    def material_func(self, _event):
        self.material_events()
        self.update()

    def type_mat_func(self, _event):
        self.type_mat_events()
        self.update()

    def color_mat_func(self, _event):
        self.color_mat_events()
        self.update()

    def plastic_func(self, _event):
        self.plastic_events()
        self.update()

    def backlighting_func(self, _event):
        self.backlighting_events()
        self.update()

    def checking_thickness_func(self, _event):
        self.checking_thickness()
        self.update()

    def checking_cable_func(self, _event):
        self.checking_cable()
        self.update()

    def plastic_material_func(self, _event):
        self.plastic_material_events()
        self.update()

    def plastic_color_material_func(self, _event):
        self.plastic_color_material_events()
        self.update()

    def plastic_processing_func(self, _event):
        self.plastic_processing_events()
        self.update()

    def plastic_sampling_func(self, event):
        self.plastic_sampling_events(event)
        self.update()

    def create_on_change_material_events(self):
        self.material.on_change = self.material_func
        self.material_type.on_change = self.type_mat_func
        self.material_color.on_change = self.color_mat_func

    def create_on_change_backlighting_events(self):
        self.backlighting.on_change = self.backlighting_func
        self.backlighting_lightbox_thickness.on_change = self.checking_thickness_func
        self.backlighting_cable.on_change = self.checking_cable_func

    def create_on_change_plastic_events(self):
        self.plastic_class.material.on_change = self.plastic_material_func
        self.plastic_class.color_material.on_change = self.plastic_color_material_func
        self.plastic_class.lamination.on_change = self.plastic_processing_func
        self.plastic_class.processing.on_change = self.plastic_processing_func
        self.plastic_class.sampling_method.on_change = self.plastic_sampling_func

    def create_on_change_events(self):
        self.create_on_change_material_events()
        self.create_on_change_backlighting_events()
        self.create_on_change_plastic_events()
        self.proces_rolling_film.on_change = self.plastic_func
        self.button_send.on_click = self.checking_entered_values

    def load_file(self, e: ft.FilePickerResultEvent):
        self.load_file_text.value, self.upload_files = load_files(e, "Макет_Листовых_материалов")
        self.update()

    def checking_size(self, event):
        checking_size(event)
        self.update()

    def checking_quantity(self, event):
        checking_quantity(event)
        self.update()

    def create_fields_general_params(self):
        self.width_sheet, self.height_sheet, self.quantity = (
            create_general_params()
        )
        self.width_sheet.on_change = self.checking_size
        self.height_sheet.on_change = self.checking_size
        self.quantity.on_change = self.checking_quantity
        card_params = card(
            'Общие параметры',
            [
                self.width_sheet,
                self.height_sheet,
                self.quantity
            ]
        )
        card_comments, contents = create_comments_and_layout_files_fields()

        self.comment_field_1, self.comment_field_2, self.load_file_text, self.load_file_btn = contents
        self.load_file_btn.on_click = lambda _: self.pick_files_dialog.pick_files(
            allow_multiple=True
        )
        return card_params, card_comments

    def checking_general_parameters(self):
        checked_var = True
        if self.height_sheet.error_text or self.width_sheet.error_text or self.quantity.error_text:
            checked_var = False
        else:
            for elem in [self.height_sheet, self.width_sheet, self.quantity]:
                if not elem.value:
                    elem.error_text = 'Не может быть пустым'
                    checked_var = False
        return checked_var

    def check_all_conditions(self):
        checks = [
            self.checking_plastic_values(),
            self.checking_material_values(),
            self.checking_backlighting_cable_values(),
            self.checking_general_parameters(),
            self.checking_backlighting_lightbox_thickness()
        ]
        return all(checks)

    def checking_entered_values(self, _event):
        checked_var = self.check_all_conditions()
        first_data = {
            'height': self.height_sheet.value,
            'width': self.width_sheet.value,
            'quantity': self.quantity.value,
        }
        if self.upload_files:
            first_data['upload_files'] = ", ".join(self.upload_files)
        else:
            first_data['upload_files'] = 'Файлы не добавлены'

        list_comments = []
        for comment in [self.comment_field_1, self.comment_field_2]:
            if self.comment_field_1.value:
                comment = comment.value
            else:
                comment = "Нет"
            list_comments.append(comment)
        first_data['comments'] = list_comments

        if not checked_var:
            self.page.banner.open = True
            self.page.update()
        else:
            general_data = self.create_data(
                first_data
            )
            if self.plastic_class.name.visible:
                plastic_data = plastic_calc(
                    self.create_data_plastic(
                        first_data
                    )
                )
                general_data['plastic'] = plastic_data
            data = main_calc(general_data)
            self.coefficient.text = data['coefficient']
            self.main_price.text = f"{data['main_price']}\xa0₽"
            self.main_sale_price.text = f"{data['main_sale_price']}\xa0₽"
            self.page.dialog.content = result_content(data)
            key = f'Листовые материалы - {datetime.now().strftime("%d.%m.%Y (%H:%M:%S)")}'
            if self.plastic_class.name.visible:
                key = f'Листовые материалы + Пленка - {datetime.now().strftime("%d.%m.%Y (%H:%M:%S)")}'
            ORDERS[key] = data
            data['result_content'] = 'sheet_materials'
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

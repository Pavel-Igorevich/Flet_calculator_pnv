import flet as ft
from data import DATA
from calculations.sheet_materials_calc import main_calc
from other_func import card, checking_size, checking_quantity
from list_orders import ORDERS
from sheet_materials.result_gui import result_content
from calculations.plastic_calc import main_calc as plastic_calc
from plastic.plastic_gui import PlasticElements
from datetime import datetime


class SheetMaterials(ft.UserControl):
    
    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
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
        self.backlighting_type_light = None
        self.backlighting_cable = None
        self.height_sheet = None
        self.width_sheet = None
        self.quantity = None
        self.button_send = None
        
        self.plastic_class = PlasticElements()
        
        self.load_file_btn = None
        self.load_file_text = None
        self.pick_files_dialog = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        self.upload_files = []
        
    def load_file(self, e: ft.FilePickerResultEvent):
        if not e.files:
            self.load_file_text.value = ''
            self.upload_files = []
        else:
            self.load_file_text.value = ", ".join(map(lambda f: f.name, e.files))
            # todo реализация только для пк, потом переделать
            for num, file in enumerate(e.files):
                self.upload_files.append(
                    [f"Макет_Листовых_материалов_{num}.{file.name.split('.')[-1]}", file.path]
                )
        self.update()
        
    def visible_type_mat(self):
        material_data = DATA['Листовые материалы']['Материал'][self.material.value]
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
        material_data = DATA['Листовые материалы']['Материал'][self.material.value]
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
    
    def material_func(self, _event):
        self.visible_type_mat()
        self.visible_thickness_color_mat()
        self.update()
        
    def type_mat_func(self, _event):
        self.visible_thickness_color_mat()
        self.update()
    
    def checking_cable(self, event):
        if event.control.value:
            if event.control.value == '0':
                event.control.value = ''
            elif not event.control.value.isdigit():
                event.control.error_text = 'Необходимо целое число'
            else:
                event.control.error_text = ''
            
        else:
            event.control.error_text = ''
        self.update()

    def checking_thickness(self, event):
        if len(event.control.value) == 0:
            event.control.error_text = 'Не может быть пустым'
        elif len(event.control.value) < 2 or not event.control.value.isdigit():
            event.control.error_text = 'Размер задается целым числом от 50'
        else:
            if int(event.control.value) < 50:
                event.control.error_text = 'Размер задается целым числом от 50'
            else:
                event.control.error_text = ''
        self.update()

    def checking_size(self, event):
        checking_size(event)
        self.update()

    def create_data(self):
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
                'rolling_film': self.proces_rolling_film.value,
                'holder': self.proces_holder.value
            },
            'backlighting': {
                'type': self.backlighting.value,
                'color': self.backlighting_color.value,
                'type_light': self.backlighting_type_light.value,
                'lightbox_thickness': self.backlighting_lightbox_thickness.value,
                'cable': self.backlighting_cable.value
            },
            'height': self.height_sheet.value,
            'width': self.width_sheet.value,
            'quantity': self.quantity.value,
        }
        return data
    
    def create_data_plastic(self):
        data_plastic = self.plastic_class.create_data_elems()
        if isinstance(data_plastic, dict):
            data_plastic.update(
                {
                    'height': self.height_sheet.value,
                    'width': self.width_sheet.value,
                    'quantity': self.quantity.value
                }
            )
        else:
            raise TypeError()
        return data_plastic
        
    def checking_entered_values(self, _event):
        if self.plastic_class.name.visible:
            checked_var = self.plastic_class.checking_values_elems()
        else:
            checked_var = True
        if self.material_color.visible:
            if not self.material_color.value:
                if not self.material_color.error_text:
                    self.material_color.error_text = 'Введите цвет композита'
                checked_var = False
        if self.backlighting_cable.visible and self.backlighting_cable.error_text:
            checked_var = False
        if self.height_sheet.error_text or self.width_sheet.error_text or self.quantity.error_text:
            checked_var = False
        else:
            for elem in [self.height_sheet, self.width_sheet, self.quantity]:
                if not elem.value:
                    elem.error_text = 'Не может быть пустым'
                    checked_var = False
        
        if not checked_var:
            self.page.banner.open = True
            self.page.update()
        else:
            general_data = self.create_data()
            if self.plastic_class.name.visible:
                plastic_data = plastic_calc(self.create_data_plastic())
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
            self.page.update()
        self.update()
        
    def visible_backlighting_param(self):
        if self.backlighting.value != 'Не требуется':
            if self.backlighting.value == 'Лайтбокс':
                self.backlighting_lightbox_thickness.visible = True
            self.backlighting_color.visible = True
            self.backlighting_type_light.visible = True
            self.backlighting_cable.visible = True
            
            self.backlighting_lightbox_thickness.value = None
            self.backlighting_cable.value = None

            backlighting_data = DATA['Листовые материалы']['Световое исполнение']
            
            backlighting_color_choices = list(backlighting_data['Цвет света'].keys())
            self.backlighting_color.options = [
                ft.dropdown.Option(choice) for choice in backlighting_color_choices
            ]
            self.backlighting_color.value = backlighting_color_choices[0]
            
            backlighting_type_choices = list(backlighting_data['Вид света'].keys())
            self.backlighting_type_light.options = [
                ft.dropdown.Option(choice) for choice in backlighting_type_choices
            ]
            self.backlighting_type_light.value = backlighting_type_choices[0]
        else:
            self.backlighting_lightbox_thickness.value = None
            self.backlighting_color.value = None
            self.backlighting_type_light.value = None
            self.backlighting_cable.value = None
            self.backlighting_lightbox_thickness.visible = False
            self.backlighting_color.visible = False
            self.backlighting_type_light.visible = False
            self.backlighting_cable.visible = False
        
    def backlighting_func(self, _event):
        self.visible_backlighting_param()
        self.update()

    def checking_quantity(self, event):
        checking_quantity(event)
        self.update()
        
    def color_mat_func(self, _event):
        self.material_color.error_text = ''
        if self.material.value == 'Композит' and self.material_type.value == 'Матовый':
            if not self.material_color.value:
                self.material_color.error_text = 'Введите цвет композита'
        self.update()
        
    def create_fields_material(self):
        material_choices = list(DATA['Листовые материалы']['Материал'].keys())
        material_choices.sort()
        default_material = material_choices[0]
    
        self.material = ft.Dropdown(
            label="Материал",
            options=[
                ft.dropdown.Option(material) for material in material_choices
            ],
            value=default_material,
            alignment=ft.alignment.center,
            on_change=self.material_func,
            bgcolor=ft.colors.WHITE,
        )
    
        self.material_type = ft.Dropdown(
            label="Вид материала",
            options=[],
            value=None,
            alignment=ft.alignment.center,
            on_change=self.type_mat_func,
            bgcolor=ft.colors.WHITE,
            visible=False
        )
    
        self.material_thickness = ft.Dropdown(
            label="Толщина",
            options=[],
            value=None,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
    
        self.material_color = ft.TextField(
            label="Цвет материала",
            visible=False,
            on_change=self.color_mat_func
        )
        self.material_edge = ft.Dropdown(
            label="Кромка",
            options=[],
            value=None,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            visible=False
        )
        
        return card(
                'Материал',
                [self.material, self.material_type, self.material_thickness, self.material_color, self.material_edge]
            )
    
    def create_fields_process(self):
        process_cutting_choices = list(DATA['Листовые материалы']['Обработка']['Вид резки'].keys())
        self.proces_type_cutting = ft.Dropdown(
            label="Вид резки",
            options=[
                ft.dropdown.Option(choice) for choice in process_cutting_choices
            ],
            value=process_cutting_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
    
        process_film_choices = list(DATA['Листовые материалы']['Обработка']['Накатка пленки'].keys())
        self.proces_rolling_film = ft.Dropdown(
            label="Накатка пленки",
            options=[
                ft.dropdown.Option(choice) for choice in process_film_choices
            ],
            value=process_film_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            on_change=self.plastic_func
        )
    
        proces_holder_choices = list(DATA['Листовые материалы']['Обработка']['Держатель'].keys())
        self.proces_holder = ft.Dropdown(
            label="Держатель",
            options=[
                ft.dropdown.Option(choice) for choice in proces_holder_choices
            ],
            value=proces_holder_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
        return card(
                'Обработка',
                [
                    self.proces_type_cutting,
                    self.proces_rolling_film,
                    self.proces_holder
                ]
            )
    
    def create_fields_backlighting(self):
        backlighting_data = DATA['Листовые материалы']['Световое исполнение']
        backlighting_choices = list(backlighting_data['Вид подсветки'].keys())
        self.backlighting = ft.Dropdown(
            label="Вид подсветки",
            options=[
                ft.dropdown.Option(choice) for choice in backlighting_choices
            ],
            value=backlighting_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            on_change=self.backlighting_func
        )
        self.backlighting_lightbox_thickness = ft.TextField(
            label="Толщина лайтбокса",
            suffix_text="мм",
            on_change=self.checking_thickness,
        )
        self.backlighting_color = ft.Dropdown(
            label="Цвет света",
            options=[],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
    
        self.backlighting_type_light = ft.Dropdown(
            label="Вид света",
            options=[],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
    
        self.backlighting_cable = ft.TextField(
            label="Дополнительный провод",
            suffix_text="м",
            visible=False,
            on_change=self.checking_cable,
            hint_text='Не требуется',
            counter_text='В комплекте уже есть пять метров'
        )
        return card(
                'Световое исполнение',
                [
                    self.backlighting,
                    self.backlighting_lightbox_thickness,
                    self.backlighting_color,
                    self.backlighting_type_light,
                    self.backlighting_cable
                ])
    
    def create_fields_general_params(self):
        self.width_sheet = ft.TextField(
            label="Ширина",
            suffix_text="мм",
            on_change=self.checking_size,
        )
        self.height_sheet = ft.TextField(
            label="Высота",
            suffix_text="мм",
            on_change=self.checking_size,
        )
        self.quantity = ft.TextField(
            label="Количество",
            suffix_text="шт.",
            on_change=self.checking_quantity,
        )
        self.load_file_text = ft.TextField(
            label="Файлы макета",
            read_only=True,
            col={'xs': 12, 'sm': 10}
        )
        self.load_file_btn = ft.IconButton(
            icon=ft.icons.UPLOAD_FILE,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.AMBER, color=ft.colors.BLACK, padding=10
            ),
            on_click=lambda _: self.pick_files_dialog.pick_files(
                allow_multiple=True
            ),
        )
        content_files = ft.ResponsiveRow(
            [
                self.load_file_text,
                ft.Container(
                    content=self.load_file_btn,
                    alignment=ft.alignment.center,
                    col={'xs': 12, 'sm': 2},
                    padding=ft.padding.only(top=5)
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        return card(
                'Общие параметры',
                [self.width_sheet, self.height_sheet, self.quantity, ft.Divider(), content_files]
            )
    
    def plastic_material_func(self, _event):
        self.plastic_class.visible_material_fields()
        self.update()
        
    def plastic_color_material_func(self, _event):
        if self.plastic_class.color_material and self.plastic_class.color_material.value:
            self.plastic_class.color_material.error_text = ''
        self.update()
        
    def plastic_processing_func(self, _event):
        self.plastic_class.visible_processing_fields()
        self.update()
        
    def plastic_sampling_func(self, event):
        self.plastic_class.visible_sampling_func(event)
        self.update()
    
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
        self.plastic_class.material.on_change = self.plastic_material_func
        self.plastic_class.color_material.on_change = self.plastic_color_material_func
        self.plastic_class.lamination.on_change = self.plastic_processing_func
        self.plastic_class.processing.on_change = self.plastic_processing_func
        self.plastic_class.sampling_method.on_change = self.plastic_sampling_func
        self.plastic_class.visible_material_fields()
        self.plastic_class.visible_processing_fields()
        self.plastic_class.visible_elems(False)
        return column_plastic
    
    def plastic_func(self, _event):
        check = bool(self.proces_rolling_film.value != 'Не требуется')
        if check:
            if self.proces_rolling_film.value == 'Плоттер':
                self.plastic_class.processing.options = [ft.dropdown.Option('Плоттер'), ]
                self.plastic_class.processing.value = 'Плоттер'
            else:
                processing_choices = list(DATA['Плёнка']['Обработка']['Вид обработки'].keys())
                if 'Плоттер' in processing_choices:
                    processing_choices.remove('Плоттер')
                self.plastic_class.processing.options = [ft.dropdown.Option(choice) for choice in processing_choices]
                if processing_choices:
                    self.plastic_class.processing.value = processing_choices[0]
            self.plastic_class.visible_processing_fields()
        self.plastic_class.visible_elems(check)
        self.update()

    def create_fields(self):
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
        column_controls.append(self.create_fields_general_params())
        self.button_send = ft.ElevatedButton(
            'Рассчитать',
            style=ft.ButtonStyle(
                padding={ft.MaterialState.DEFAULT: 20}, bgcolor=ft.colors.AMBER, color=ft.colors.BLACK
            ),
            on_click=self.checking_entered_values
        )
        column_controls.append(self.button_send)
        self.visible_backlighting_param()
        self.visible_type_mat()
        self.visible_thickness_color_mat()
        return column_controls

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
    
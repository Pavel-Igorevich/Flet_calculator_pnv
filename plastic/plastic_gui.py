from datetime import datetime

import flet as ft
from data import DATA
from other_func import card, checking_size, checking_quantity
from calculations.plastic_calc import main_calc
from plastic.result_gui import result_content
from list_orders import ORDERS


class PlasticElements:
    def __init__(self):
        self.material = None
        self.color_material = None
        self.print_quality = None
        self.processing = None
        self.lamination = None
        self.lamination_divider = None
        self.sampling_method = None
        self.sampling_complexity = None
        self.mounting_plastic = None
        self.card_material = None
        self.card_process = None
        self.name = None
        self.divider_down = None
        self.divider_top = None
        
    def visible_material_fields(self):
        fields_data = DATA['Плёнка']['Материал'][self.material.value]
        self.print_quality.visible = False
        self.color_material.visible = False
        if 'Качество печати' in fields_data:
            options_print = list(fields_data['Качество печати'].keys())
            self.print_quality.options = [
                ft.dropdown.Option(quality) for quality in options_print
            ]
            self.print_quality.value = options_print[0]
            self.print_quality.visible = True
        if 'Цвет' in fields_data:
            self.color_material.visible = True
        if 'Ламинация' in fields_data:
            self.lamination.visible = fields_data['Ламинация']
            self.lamination_divider.visible = fields_data['Ламинация']
        else:
            self.lamination.visible = True
            self.lamination_divider.visible = True
        
    def create_elements_material(self):
        material_choices = list(DATA['Плёнка']['Материал'].keys())
        default_material = material_choices[0]
        self.material = ft.Dropdown(
            label="Материал плёнки",
            options=[
                ft.dropdown.Option(material) for material in material_choices
            ],
            value=default_material,
            alignment=ft.alignment.center,
            # on_change=self.material_func,
            bgcolor=ft.colors.WHITE,
        )
        self.print_quality = ft.Dropdown(
            label="Качество печати",
            options=[],
            value=None,
            alignment=ft.alignment.center,
            visible=False,
            bgcolor=ft.colors.WHITE,
        )
        self.color_material = ft.TextField(
            label="Цвет плёнки",
            visible=False
        )
        self.card_material = card('Материал', [self.material, self.print_quality, self.color_material])
        return self.card_material
        
    def create_elements_processing(self):
        lamination_choices = list(DATA['Плёнка']['Обработка']['Ламинация'].keys())
    
        self.lamination = ft.Dropdown(
            label="Ламинация",
            options=[
                ft.dropdown.Option(choice) for choice in lamination_choices
            ],
            value=lamination_choices[0],
            alignment=ft.alignment.center,
            # on_change=self.processing_func,
            bgcolor=ft.colors.WHITE,
        )
        self.lamination_divider = ft.Divider()
    
        processing_choices = list(DATA['Плёнка']['Обработка']['Вид обработки'].keys())
        self.processing = ft.Dropdown(
            label="Вид обработки",
            options=[
                ft.dropdown.Option(choice) for choice in processing_choices
            ],
            value=processing_choices[0],
            alignment=ft.alignment.center,
            # on_change=self.processing_func,
            bgcolor=ft.colors.WHITE,
        )
        self.sampling_method = ft.Dropdown(
            label="Вид выборки",
            options=[],
            value=None,
            alignment=ft.alignment.center,
            # on_change=self.sampling_func,
            bgcolor=ft.colors.WHITE,
            visible=False
        )
        self.sampling_complexity = ft.Dropdown(
            label="Сложность выборки",
            options=[],
            value=None,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            visible=False
        )
        mounting_choices = list(
            DATA['Плёнка']['Обработка']['Вид обработки']['Плоттер']['Монтажная пленка'].keys()
        )
        self.mounting_plastic = ft.Dropdown(
            label="Монтажная пленка",
            options=[
                ft.dropdown.Option(choice) for choice in mounting_choices
            ],
            value=mounting_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            visible=False
        )
        self.card_process = card(
            'Обработка',
            [
                self.processing,
                self.sampling_method,
                self.sampling_complexity,
                self.mounting_plastic,
                self.lamination_divider,
                self.lamination
            ]
        )
        return self.card_process
        
    def visible_processing_fields(self):
        fields_data = DATA['Плёнка']['Обработка']['Вид обработки'][self.processing.value]
        self.sampling_method.visible = False
        self.sampling_complexity.visible = False
        self.mounting_plastic.visible = False
        if 'Вид выборки' in fields_data:
            data_sampling = fields_data['Вид выборки']
            options_sampling = list(data_sampling.keys())
            self.sampling_method.options = [
                ft.dropdown.Option(choice) for choice in options_sampling
            ]
            self.sampling_method.value = options_sampling[0]
            self.sampling_method.visible = True
            data_complexity = data_sampling[options_sampling[0]]
            if "Сложность выборки" in data_complexity:
                options_complexity = list(data_complexity["Сложность выборки"].keys())
                self.sampling_complexity.options = [
                    ft.dropdown.Option(choice) for choice in options_complexity
                ]
                self.sampling_complexity.value = options_complexity[0]
                self.sampling_complexity.visible = True
        if 'Монтажная пленка' in fields_data:
            self.mounting_plastic.visible = True
            
    def visible_sampling_func(self, event):
        self.sampling_complexity.visible = False
        sampling = DATA['Плёнка']['Обработка']['Вид обработки'][self.processing.value].get('Вид выборки')
        if sampling:
            if "Сложность выборки" in sampling[event.control.value]:
                options_complexity = list(sampling[event.control.value]["Сложность выборки"].keys())
                self.sampling_complexity.options = [
                    ft.dropdown.Option(choice) for choice in options_complexity
                ]
                self.sampling_complexity.value = options_complexity[0]
                self.sampling_complexity.visible = True
                
    def checking_values_elems(self):
        checked_var = True
        if self.color_material.visible:
            if not self.color_material.value:
                if not self.color_material.error_text:
                    self.color_material.error_text = 'Введите цвет композита'
                checked_var = False
        return checked_var
    
    def visible_elems(self, check):
        for elem in (self.divider_top, self.divider_down, self.name, self.card_material, self.card_process):
            if elem:
                elem.visible = check
                
    def create_data_elems(self) -> dict:
        attributes_to_check = {
            self.color_material: 'color_material',
            self.lamination: 'lamination',
            self.sampling_method: 'sampling_method',
            self.sampling_complexity: 'sampling_complexity',
            self.mounting_plastic: 'mounting_plastic',
            self.print_quality: 'print_quality'
        }
        add_data = {}
        for attribute, key in attributes_to_check.items():
            if not attribute.visible:
                add_data[key] = None
            else:
                add_data[key] = attribute.value
        return {
            'material': {
                'name': self.material.value,
                'print_quality': add_data['print_quality'],
                'color_material': add_data['color_material'],
            },
            'processing': {
                'lamination': add_data['lamination'],
                'processing': self.processing.value,
                'sampling_method': add_data['sampling_method'],
                'sampling_complexity': add_data['sampling_complexity'],
                'mounting_plastic': add_data['mounting_plastic']
            }
        }
                

class PlasticGUI(ft.UserControl, PlasticElements):
    
    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.height_plastic = None
        self.width_plastic = None
        self.quantity = None
        self.button_send = None

        self.load_file_btn = None
        self.load_file_text = None
        self.pick_files_dialog = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        self.upload_files = []
        
    def material_func(self, _event):
        self.visible_material_fields()
        self.update()
        
    def load_file(self, e: ft.FilePickerResultEvent):
        if not e.files:
            self.load_file_text.value = ''
            self.upload_files = []
        else:
            self.load_file_text.value = ", ".join(map(lambda f: f.name, e.files))
            # todo реализация только для пк, потом переделать
            for num, file in enumerate(e.files):
                self.upload_files.append(
                    [f"Макет_Пленки_{num}.{file.name.split('.')[-1]}", file.path]
                )
        self.update()
        
    def color_material_func(self, _event):
        if self.color_material and self.color_material.value:
            self.color_material.error_text = ''
        self.update()
    
    def material_card(self):
        card_material = self.create_elements_material()
        self.material.on_change = self.material_func
        self.color_material.on_change = self.color_material_func
        return card_material
    
    def processing_func(self, _event):
        self.visible_processing_fields()
        self.update()
    
    def sampling_func(self, event):
        self.visible_sampling_func(event)
        self.update()
    
    def processing_card(self):
        card_process = self.create_elements_processing()
        self.lamination.on_change = self.processing_func
        self.processing.on_change = self.processing_func
        self.sampling_method.on_change = self.sampling_func
        return card_process

    def checking_size(self, event):
        checking_size(event)
        self.update()

    def checking_quantity(self, event):
        checking_quantity(event)
        self.update()
     
    def create_fields(self):
        column_controls = [
            ft.Row(
                [ft.Text('Плёнка', size=25)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            self.material_card(),
            self.processing_card()
        ]
        
        self.width_plastic = ft.TextField(
            label="Ширина",
            suffix_text="мм",
            on_change=self.checking_size,
        )
        self.height_plastic = ft.TextField(
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
            alignment=ft.MainAxisAlignment.CENTER

        )
        
        column_controls.append(
            card(
                'Общие параметры',
                [self.width_plastic, self.height_plastic, self.quantity, ft.Divider(), content_files]
            )
        )
        
        # todo не доделана
        self.button_send = ft.ElevatedButton(
            'Рассчитать',
            # 'Расчет не сделан',
            style=ft.ButtonStyle(
                padding={ft.MaterialState.DEFAULT: 20}, bgcolor=ft.colors.AMBER, color=ft.colors.BLACK
                # padding={ft.MaterialState.DEFAULT: 20}, bgcolor=ft.colors.RED_500, color=ft.colors.WHITE
            ),
            on_click=self.checking_entered_values
        )
        column_controls.append(self.button_send)
        
        self.visible_material_fields()
        self.visible_processing_fields()
        return column_controls
    
    def create_data(self):
        data = self.create_data_elems()
        if isinstance(data, dict):
            data.update(
                {
                    'height': self.height_plastic.value,
                    'width': self.width_plastic.value,
                    'quantity': self.quantity.value
                }
            )
        else:
            raise TypeError()
        return data

    def checking_entered_values(self, _event):
        checked_var = self.checking_values_elems()
        if self.height_plastic.error_text or self.width_plastic.error_text or self.quantity.error_text:
            checked_var = False
        else:
            for elem in [self.height_plastic, self.width_plastic, self.quantity]:
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
            ORDERS[f'Плёнка - {datetime.now().strftime("%d.%m.%Y (%H:%M:%S)")}'] = data
            data['result_content'] = 'plastic'
            self.page.dialog.open = True
            self.page.update()
        self.update()

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
        
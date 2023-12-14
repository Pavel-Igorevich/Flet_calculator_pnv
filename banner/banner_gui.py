import flet as ft
from datetime import datetime
from banner.result_gui import result_content
from data import DATA
from calculations.banner_calc import main_calc
from list_orders import ORDERS
from other_func import card, checking_size, checking_quantity
# from icecream import ic


class BannerGUI(ft.UserControl):
    
    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.material = None
        self.processing = None
        self.print_quality = None
        self.height_banner = None
        self.width_banner = None
        self.quantity = None
        self.button_send = None
        self.welding_step = None
        self.sides_processing = None
        self.left_side = None
        self.right_side = None
        self.top_side = None
        self.bottom_side = None
        self.all_sides = None
        self.corners = None
        self.text_side = None
        self.error_message_sides = None
        self.result_modal = None
        
        self.load_file_btn = None
        self.load_file_text = None
        self.pick_files_dialog = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        self.upload_files = []
        
        self.sides_icons = {
            'Левая': ft.icons.BORDER_LEFT,
            'Правая': ft.icons.BORDER_RIGHT,
            'Верх': ft.icons.BORDER_TOP,
            'Низ': ft.icons.BORDER_BOTTOM,
            'Все стороны': ft.icons.BORDER_OUTER,
            'По углам': ft.icons.ALL_OUT,
        }
        
    def load_file(self, e: ft.FilePickerResultEvent):
        if not e.files:
            self.load_file_text.value = ''
            self.upload_files = []
        else:
            self.load_file_text.value = ", ".join(map(lambda f: f.name, e.files))
            # todo реализация только для пк, потом переделать
            for num, file in enumerate(e.files):
                self.upload_files.append(
                    [f"Макет_Баннера_{num}.{file.name.split('.')[-1]}", file.path]
                )
        self.update()
    
    def visible_welding_step(self):
        if DATA['Баннер']['Обработка'][self.processing.value].get('Шаг сварки'):
            steps = list(DATA['Баннер']['Обработка'][self.processing.value]['Шаг сварки'].keys())
            self.welding_step.options = [ft.dropdown.Option(step) for step in steps]
            self.welding_step.value = steps[0]
            self.welding_step.visible = True
        
        else:
            self.welding_step.visible = False
    
    def visible_sides(self):
        side_mapping = self.generate_side_mapping()
        if self.processing:
            sides = DATA['Баннер']['Обработка'][self.processing.value].get('Сторона')
        else:
            sides = None
        
        if sides:
            self.text_side.visible = True
            for name_side in self.sides_icons.keys():
                check = False
                if name_side in sides:
                    check = True
                if name_side in side_mapping:
                    side_mapping[name_side].visible = check
        else:
            for side in side_mapping.values():
                side.visible = False
            self.text_side.visible = False
            self.error_message_sides.visible = False
    
    def processing_func(self, _event):
        self.visible_welding_step()
        self.visible_sides()
        self.update()
    
    def material_func(self, event):
        list_choices = list(DATA['Баннер']['Материал'][event.control.value]['Качество печати'].keys())
        self.print_quality.options = [ft.dropdown.Option(quality) for quality in list_choices]
        self.print_quality.value = list_choices[0]
        self.update()
    
    def create_sides_processing(self):
        side_attributes = {
            'Левая': 'left_side',
            'Правая': 'right_side',
            'Верх': 'top_side',
            'Низ': 'bottom_side',
            'Все стороны': 'all_sides',
            'По углам': 'corners',
        }
        
        elems = []
        
        for name_side, icon in self.sides_icons.items():
            side = ft.Chip(
                label=ft.Icon(icon, size=20),
                selected_color=ft.colors.GREEN_200,
                col={"xs": 6, 'sm': 2},
                on_select=self.chip_event_func,
                tooltip=name_side,
                visible=False
            )
            setattr(self, side_attributes.get(name_side, name_side), side)
            elems.append(side)
        return ft.ResponsiveRow(elems, alignment=ft.MainAxisAlignment.CENTER)
    
    def chip_event_func(self, event):
        side_mapping = self.generate_side_mapping()
        if event.control.tooltip in ('Все стороны', 'По углам'):
            for side, var_side in side_mapping.items():
                if side != event.control.tooltip and var_side.selected:
                    var_side.selected = False
        else:
            list_sides = ['Левая', 'Правая', 'Верх', 'Низ']
            if all([side_mapping[side].selected for side in list_sides]):
                for side in list_sides:
                    side_mapping[side].selected = False
                self.all_sides.selected = True
            else:
                for side in ('Все стороны', 'По углам'):
                    if side_mapping[side].selected:
                        side_mapping[side].selected = False
        if any([side_mapping[name_side].selected for name_side in side_mapping]):
            self.error_message_sides.visible = False
        self.update()
        
    def generate_side_mapping(self) -> dict:
        return {
            'Левая': self.left_side,
            'Правая': self.right_side,
            'Верх': self.top_side,
            'Низ': self.bottom_side,
            'Все стороны': self.all_sides,
            'По углам': self.corners,
        }
    
    def checking_size(self, event):
        checking_size(event)
        self.update()
    
    def checking_quantity(self, event):
        checking_quantity(event)
        self.update()
    
    def create_fields(self):
        column_controls = []
        material_choices = list(DATA['Баннер']['Материал'].keys())
        processing_choices = list(DATA['Баннер']['Обработка'].keys())
        default_material = material_choices[0]
        print_quality_choices = list(DATA['Баннер']['Материал'][default_material]['Качество печати'].keys())
        
        column_controls.append(
            ft.Row(
                [ft.Text('Баннер', size=25)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        )
        
        self.material = ft.Dropdown(
            label="Материал баннера",
            options=[
                ft.dropdown.Option(material) for material in material_choices
            ],
            value=material_choices[0],
            alignment=ft.alignment.center,
            on_change=self.material_func,
            bgcolor=ft.colors.WHITE,
        )
        self.print_quality = ft.Dropdown(
            label="Качество печати",
            options=[
                ft.dropdown.Option(quality) for quality in print_quality_choices
            ],
            value=print_quality_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
        column_controls.append(card('Материал', [self.material, self.print_quality]))
        
        self.processing = ft.Dropdown(
            label="Обработка",
            options=[
                ft.dropdown.Option(processing) for processing in processing_choices
            ],
            value=processing_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            on_change=self.processing_func,
        )
        self.welding_step = ft.Dropdown(
            label="Шаг сварки",
            options=[],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
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

        column_controls.append(
            card(
                'Обработка',
                [
                    self.processing,
                    self.welding_step,
                    self.text_side,
                    self.error_message_sides,
                    self.create_sides_processing()
                ]
            )
        )
        self.width_banner = ft.TextField(
            label="Ширина",
            suffix_text="мм",
            on_change=self.checking_size,
        )
        self.height_banner = ft.TextField(
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
                [self.width_banner, self.height_banner, self.quantity, ft.Divider(), content_files]))
        
        self.button_send = ft.ElevatedButton(
            'Рассчитать',
            style=ft.ButtonStyle(
                padding={ft.MaterialState.DEFAULT: 20}, bgcolor=ft.colors.AMBER, color=ft.colors.BLACK
            ),
            on_click=self.checking_entered_values
        )
        column_controls.append(self.button_send)
        self.visible_sides()
        self.visible_welding_step()
        return column_controls
    
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
            'files': self.upload_files
        }
        if DATA['Баннер']['Обработка'][self.processing.value].get('Сторона'):
            data_sides = self.generate_side_mapping()
            processing_sides = [side for side, value in data_sides.items() if value.selected]
            data['processing']['sides'] = ', '.join(processing_sides)
        else:
            data['processing']['sides'] = None
            
        if DATA['Баннер']['Обработка'][self.processing.value].get('Шаг сварки'):
            data['processing']['welding_step'] = self.welding_step.value
        else:
            data['processing']['welding_step'] = None
        
        material = DATA['Баннер']['Обработка'][self.processing.value].get('Материал')
        data['processing']['material'] = material

        return data
    
    def checking_entered_values(self, _event):
        checked_var = True
        if self.page.banner:
            self.page.banner.open = False
            self.page.update()
            
        if self.text_side.visible:
            side_mapping = self.generate_side_mapping()
            if not any([side_mapping[name_side].selected for name_side in side_mapping]):
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

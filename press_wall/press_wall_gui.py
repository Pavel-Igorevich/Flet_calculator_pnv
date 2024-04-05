import flet as ft

from data import MAIN_DATA
from other_func import card, checking_size, checking_quantity, load_files


class PressWallGUI(ft.UserControl):

    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.skeleton = None
        self.overhead_elements = None
        self.second_side = None
        self.print_quality = None
        self.height_p_w = None
        self.width_p_w = None
        self.depth_p_w = None
        self.quantity = None
        self.exploitation = None

        self.load_file_btn = None
        self.load_file_text = None
        self.pick_files_dialog = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        self.upload_files = []

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

    def visible_material(self):
        skeleton_data = MAIN_DATA['Пресс-Волл']['Вид каркаса']
        if self.skeleton.value in skeleton_data:
            overhead_data = skeleton_data[self.skeleton.value]["Накладные элементы"]
            if overhead_data:
                self.overhead_elements.options = [ft.dropdown.Option(choice) for choice in overhead_data]
                self.overhead_elements.visible = True
                self.overhead_elements.value = overhead_data[0]
            else:
                self.overhead_elements.options = []
                self.overhead_elements.visible = False
                self.overhead_elements.value = ''

            depth = skeleton_data[self.skeleton.value]["Глубина"]
            if depth:
                self.depth_p_w.options = [ft.dropdown.Option(choice) for choice in depth]
                self.depth_p_w.value = depth[0]
                self.depth_p_w.visible = True
            else:
                self.depth_p_w.options = []
                self.depth_p_w.visible = False
                self.depth_p_w.value = ''

    def material_func(self, _event):
        self.visible_material()
        self.update()

    def create_fields(self):
        skeleton_choices = list(MAIN_DATA['Пресс-Волл']['Вид каркаса'].keys())

        self.skeleton = ft.Dropdown(
            label="Каркас",
            options=[
                ft.dropdown.Option(choice) for choice in skeleton_choices
            ],
            value=skeleton_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            on_change=self.material_func
        )

        self.overhead_elements = ft.Dropdown(
            label="Накладные элементы",
            options=[],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            visible=False
        )

        side_choices = MAIN_DATA['Пресс-Волл']['Вторая сторона']
        self.second_side = ft.Dropdown(
            label="Вторая сторона",
            options=[
                ft.dropdown.Option(choice) for choice in side_choices
            ],
            value=side_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )

        print_choices = MAIN_DATA['Пресс-Волл']['Качество печати']
        self.print_quality = ft.Dropdown(
            label="Качество печати",
            options=[
                ft.dropdown.Option(choice) for choice in print_choices
            ],
            value=print_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )

        column_controls = [
            ft.Row(
                [ft.Text('Пресс-Волл', size=25)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            card(
                "Материал",
                [
                    self.skeleton,
                    self.print_quality,
                    self.overhead_elements,
                    self.second_side,
                ]
            ),
        ]

        exploitation_choices = list(MAIN_DATA['Пресс-Волл']['Место эксплуатации'].keys())
        self.exploitation = ft.Dropdown(
            label="Место эксплуатации",
            options=[
                ft.dropdown.Option(choice) for choice in exploitation_choices
            ],
            value=exploitation_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )

        self.depth_p_w = ft.Dropdown(
            label="Глубина",
            options=[],
            visible=False,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
        self.width_p_w = ft.TextField(
            label="Ширина",
            suffix_text="мм",
            on_change=self.checking_size,
        )
        self.height_p_w = ft.TextField(
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

        column_controls.append(
            card(
                'Общие параметры',
                [
                    self.exploitation,
                    self.depth_p_w,
                    self.width_p_w,
                    self.height_p_w,
                    self.quantity,
                    ft.Divider(),
                    content_files
                ]
            )
        )

        # todo не доделана
        self.button_send = ft.ElevatedButton(
            # 'Рассчитать',
            'Расчет не сделан',
            style=ft.ButtonStyle(
                # padding={ft.MaterialState.DEFAULT: 20}, bgcolor=ft.colors.AMBER, color=ft.colors.BLACK
                padding={ft.MaterialState.DEFAULT: 20}, bgcolor=ft.colors.RED_500, color=ft.colors.WHITE
            ),
            # on_click=self.checking_entered_values
        )
        column_controls.append(self.button_send)
        self.visible_material()
        return column_controls

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

import flet as ft

from data import MAIN_DATA
from other_func import card, checking_size, checking_quantity, load_files, create_general_params, \
    create_comments_and_layout_files_fields


class PressWallGUI(ft.UserControl):

    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.data = MAIN_DATA['Пресс-Волл']
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

    def visible_material(self):
        skeleton_data = self.data['Вид каркаса']
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

    def create_general_fields(self):
        exploitation_choices = list(self.data['Место эксплуатации'].keys())
        self.exploitation = ft.Dropdown(
            label="Место эксплуатации",
            options=[
                ft.dropdown.Option(choice) for choice in exploitation_choices
            ],
            value=exploitation_choices[0],
            alignment=ft.alignment.center,
        )

        self.depth_p_w = ft.TextField(
            label="Глубина",
            suffix_text="мм",
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.width_p_w, self.height_p_w, self.quantity = (
            create_general_params()
        )
        self.depth_p_w.on_change = self.checking_size
        self.width_p_w.on_change = self.checking_size
        self.height_p_w.on_change = self.checking_size
        self.quantity.on_change = self.checking_quantity
        card_params = card(
            'Общие параметры',
            [
                self.exploitation,
                self.width_p_w,
                self.height_p_w,
                self.depth_p_w,
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
        skeleton_choices = list(self.data['Вид каркаса'].keys())

        self.skeleton = ft.Dropdown(
            label="Каркас",
            options=[
                ft.dropdown.Option(choice) for choice in skeleton_choices
            ],
            value=skeleton_choices[0],
            alignment=ft.alignment.center,
            on_change=self.material_func
        )

        self.overhead_elements = ft.Dropdown(
            label="Накладные элементы",
            options=[],
            alignment=ft.alignment.center,
            visible=False
        )

        side_choices = self.data['Вторая сторона']
        self.second_side = ft.Dropdown(
            label="Вторая сторона",
            options=[
                ft.dropdown.Option(choice) for choice in side_choices
            ],
            value=side_choices[0],
            alignment=ft.alignment.center,
        )

        print_choices = self.data['Качество печати']
        self.print_quality = ft.Dropdown(
            label="Качество печати",
            options=[
                ft.dropdown.Option(choice) for choice in print_choices
            ],
            value=print_choices[0],
            alignment=ft.alignment.center,
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
        column_controls.extend(self.create_general_fields())

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

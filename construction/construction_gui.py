import flet as ft
from data import MAIN_DATA
from other_func import card, checking_size, checking_quantity, create_general_params
from sheet_materials.sheet_materials_gui import SheetMaterials
from banner.banner_gui import Banner


class ConstructionsGUI(ft.UserControl):

    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient
        self.data = MAIN_DATA['Конструкции']
        self.skeleton = None
        self.add_sheet_materials = None
        self.container_add_sh_m = None
        self.profile_size = None
        self.color_divider = ft.Divider(visible=False)
        self.color_format = None
        self.color = None
        self.color_list = None
        self.overlays = None
        self.overlays_divider = ft.Divider(visible=False)
        self.cladding_material = None
        self.sheet_materials = SheetMaterials()
        self.banner = Banner()

        self.height_cnst = None
        self.width_cnst = None
        self.depth_cnst = None
        self.quantity = None
        self.exploitation = None

        self.load_file_btn = None
        self.load_file_text = None
        self.pick_files_dialog = ft.FilePicker(on_result=self.load_file)
        self.page.overlay.append(self.pick_files_dialog)
        self.page.update()
        self.upload_files = []
        self.container_sheet_materials = None
        self.container_banner = None
        self.button_send = None

    def checking_size(self, event):
        checking_size(event)
        self.update()

    def checking_quantity(self, event):
        checking_quantity(event)
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
                    [f"Макет_Холста_{num}.{file.name.split('.')[-1]}", file.path]
                )
        self.update()

    def visible_skeleton(self):
        skeleton_data = self.data["Вид каркаса"][self.skeleton.value]
        show_profile_size = skeleton_data.get('Размер профиля')
        if show_profile_size:
            self.profile_size.visible = True
            self.profile_size.options = [ft.dropdown.Option(choice) for choice in show_profile_size]
            self.profile_size.value = show_profile_size[0]
        else:
            self.profile_size.visible = False

        show_color = skeleton_data.get('Цвет')
        if show_color:
            if isinstance(show_color, list):
                self.color_list.visible = True
                self.color_list.options = [ft.dropdown.Option(choice) for choice in show_color]
                self.color_list.value = show_color[0]
                self.color.visible = False
                self.color_format.visible = False
                self.color_divider.visible = False
            else:
                self.color.visible = True
                self.color_format.visible = True
                self.color_divider.visible = True
                self.color_list.visible = False
        else:
            self.color.visible = False
            self.color_divider.visible = False
            self.color_format.visible = False
            self.color_list.visible = False

    def visible_sheet_materials(self):
        self.container_sheet_materials.visible = False
        if self.skeleton.value == 'Листовые материалы':
            self.container_sheet_materials.visible = True

    def visible_type_banner(self):
        material_choices = list(self.banner.data_material.keys())
        self.banner.material.options = [
                ft.dropdown.Option(material) for material in material_choices
            ]
        self.banner.material.value = material_choices[0]
        if self.skeleton.value in ('Брус', 'Металл'):
            self.banner.material.options = [
                ft.dropdown.Option("Black back")
            ]
            self.banner.material.value = "Black back"
        self.banner.material_events()

    def visible_overlays(self):
        data_overlays = self.data['Вид каркаса'][self.skeleton.value]['ПВХ накладки на торцы']
        if isinstance(data_overlays, bool):
            self.overlays.visible = False
            self.overlays_divider.visible = False
        else:
            self.overlays.visible = True
            self.overlays_divider.visible = True
            self.overlays.options = [
                ft.dropdown.Option(choice) for choice in data_overlays
            ]
            self.overlays.value = data_overlays[0]

    def visible_add_sheet_materials(self):
        key = self.data["Вид каркаса"][self.skeleton.value].get('Добавить листовые материалы')
        if key:
            self.container_add_sh_m.visible = True
            self.add_sheet_materials.visible = True
        else:
            self.container_add_sh_m.visible = False
            self.add_sheet_materials.visible = False
        self.add_sheet_materials.selected = False

    def skeleton_func(self, _event):
        self.visible_skeleton()
        self.visible_add_sheet_materials()
        self.visible_sheet_materials()
        self.visible_type_banner()
        self.visible_color_constructions()
        self.visible_overlays()
        self.visible_color_format()
        self.update()

    def cladding_material_func(self, _event):
        self.container_banner.visible = False
        if self.cladding_material.value == 'Баннер':
            self.container_banner.visible = True
            self.visible_color_constructions()
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
            bgcolor=ft.colors.WHITE,
        )

        self.depth_cnst = ft.Dropdown(
            label="Глубина",
            options=[],
            visible=False,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
        self.width_cnst, self.height_cnst, self.quantity, self.load_file_text, self.load_file_btn = (
            create_general_params()
        )
        self.width_cnst.on_change = self.checking_size,
        self.height_cnst.on_change = self.checking_size,
        self.quantity.on_change = self.checking_quantity,

        self.load_file_btn.on_click = lambda _: self.pick_files_dialog.pick_files(
                allow_multiple=True
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
            [
                self.exploitation,
                self.depth_cnst,
                self.width_cnst,
                self.height_cnst,
                self.quantity,
                ft.Divider(),
                content_files
            ]
        )

    def amenity_selected(self, _event):
        self.container_sheet_materials.visible = False
        if self.add_sheet_materials.selected:
            self.container_sheet_materials.visible = True
        self.update()

    def visible_color_format(self):
        if self.color_format.value == 'RAL':
            self.color.icon = ft.icons.COLOR_LENS
            self.color.helper_text = "Формат RAL"
            self.color.prefix_text = '#'
            self.color.input_filter = ft.NumbersOnlyInputFilter()
        else:
            self.color.icon = ft.icons.FORMAT_SIZE
            self.color.helper_text = "Формат текст"
            self.color.prefix_text = ''
            self.color.input_filter = ft.TextOnlyInputFilter()

    def change_color_format(self, _event):
        self.visible_color_format()
        self.update()

    def create_skeleton_fields(self):
        skeleton_choices = list(self.data['Вид каркаса'].keys())

        self.skeleton = ft.Dropdown(
            label="Каркас",
            options=[
                ft.dropdown.Option(choice) for choice in skeleton_choices
            ],
            value=skeleton_choices[0],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            on_change=self.skeleton_func
        )
        self.add_sheet_materials = ft.Chip(
            label=ft.Text('Добавить листовые материалы'),
            on_select=self.amenity_selected,
            selected_color=ft.colors.AMBER,
            bgcolor=ft.colors.GREY_200,
            visible=False,
        )
        self.container_add_sh_m = ft.Row(
            [self.add_sheet_materials, ],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False
        )

        self.profile_size = ft.Dropdown(
            label="Размер профиля",
            options=[],
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
        )
        self.color_format = ft.Dropdown(
            label="Задать цвет в формате",
            value='Текст',
            options=[ft.dropdown.Option(choice) for choice in ['RAL', 'Текст']],
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            on_change=self.change_color_format
        )

        self.color = ft.TextField(
            label="Цвет покраски",
            icon=ft.icons.FORMAT_SIZE,
            helper_text="Формат текст",
            input_filter=ft.TextOnlyInputFilter()
        )
        self.color_list = ft.Dropdown(
            label="Цвет",
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
        )
        self.cladding_material = ft.Dropdown(
            label="Материал обшивки",
            options=[
                ft.dropdown.Option(choice) for choice in ["Без обшивки", "Баннер"]
            ],
            value="Без обшивки",
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            on_change=self.cladding_material_func
        )
        self.overlays = ft.Dropdown(
            label="ПВХ накладки на торцы",
            options=[],
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            visible=False
        )
        return card(
                "Основа конструкции",
                [
                    self.skeleton,
                    self.container_add_sh_m,
                    self.profile_size,
                    self.color_divider,
                    self.color_format,
                    self.color,
                    self.color_list,
                    ft.Divider(),
                    self.cladding_material,
                    self.overlays_divider,
                    self.overlays
                ]
            )

    def create_main_fields(self):
        self.create_sheet_materials_container()
        self.create_banner_container()
        column_controls = [
            ft.Row(
                [ft.Text('Конструкции', size=25)],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )

        ]

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
        column_controls.append(self.create_skeleton_fields())
        column_controls.append(self.container_sheet_materials)
        column_controls.append(self.container_banner)
        column_controls.append(self.create_general_fields())
        column_controls.append(self.button_send)
        self.visible_skeleton()
        self.visible_add_sheet_materials()
        self.visible_type_banner()
        self.visible_overlays()
        self.visible_color_format()
        self.shm_create_on_change_events()
        self.bnr_create_on_change_events()
        return column_controls

    def create_banner_container(self):
        banner_fields = self.banner.create_fields(btn_send=False)
        banner_fields.append(ft.Divider())
        self.container_banner = ft.Container(
            content=ft.Column(banner_fields),
            visible=False
        )

    def create_sheet_materials_container(self):
        sheet_materials_fields = self.sheet_materials.create_fields(btn_send=False)
        sheet_materials_fields.insert(0, ft.Divider())
        sheet_materials_fields.append(ft.Divider())
        self.container_sheet_materials = ft.Container(
            content=ft.Column(sheet_materials_fields),
            visible=False
        )

    def shm_material_func(self, _event):
        self.sheet_materials.material_events()
        self.visible_color_constructions()
        self.update()

    def shm_type_mat_func(self, _event):
        self.sheet_materials.type_mat_events()
        self.update()

    def shm_color_mat_func(self, _event):
        self.sheet_materials.color_mat_events()
        self.update()

    def shm_plastic_func(self, _event):
        self.sheet_materials.plastic_events()
        self.sheet_materials.plastic_class.divider_down.visible = False
        self.update()

    def shm_backlighting_func(self, _event):
        self.sheet_materials.backlighting_events()
        self.update()

    def shm_checking_thickness_func(self, _event):
        self.sheet_materials.checking_thickness()
        self.update()

    def shm_checking_cable_func(self, _event):
        self.sheet_materials.checking_cable()
        self.update()

    def visible_color_constructions(self):
        if self.container_sheet_materials.visible:
            if self.sheet_materials.material.value not in ('ДСП', 'Фанера', 'МДФ', 'ПВХ'):
                self.color.visible = False
                self.color_format.visible = False
                self.color_divider.visible = False
            else:
                self.color.visible = True
                self.color_format.visible = True
                self.color_divider.visible = True

    def shm_plastic_material_func(self, _event):
        self.sheet_materials.plastic_material_events()
        self.update()

    def shm_plastic_color_material_func(self, _event):
        self.sheet_materials.plastic_color_material_events()
        self.update()

    def shm_plastic_processing_func(self, _event):
        self.sheet_materials.plastic_processing_events()
        self.update()

    def shm_plastic_sampling_func(self, event):
        self.sheet_materials.plastic_sampling_events(event)
        self.update()

    def shm_create_on_change_material_events(self):
        self.sheet_materials.material.on_change = self.shm_material_func
        self.sheet_materials.material_type.on_change = self.shm_type_mat_func
        self.sheet_materials.material_color.on_change = self.shm_color_mat_func

    def shm_create_on_change_backlighting_events(self):
        self.sheet_materials.backlighting.on_change = self.shm_backlighting_func
        self.sheet_materials.backlighting_lightbox_thickness.on_change = self.shm_checking_thickness_func
        self.sheet_materials.backlighting_cable.on_change = self.shm_checking_cable_func

    def shm_create_on_change_plastic_events(self):
        self.sheet_materials.plastic_class.material.on_change = self.shm_plastic_material_func
        self.sheet_materials.plastic_class.color_material.on_change = self.shm_plastic_color_material_func
        self.sheet_materials.plastic_class.lamination.on_change = self.shm_plastic_processing_func
        self.sheet_materials.plastic_class.processing.on_change = self.shm_plastic_processing_func
        self.sheet_materials.plastic_class.sampling_method.on_change = self.shm_plastic_sampling_func

    def shm_create_on_change_events(self):
        self.shm_create_on_change_material_events()
        self.shm_create_on_change_backlighting_events()
        self.shm_create_on_change_plastic_events()

        self.sheet_materials.proces_rolling_film.on_change = self.shm_plastic_func

    def bnr_material_func(self, _event):
        self.banner.material_events()
        self.update()

    def bnr_processing_func(self, _event):
        self.banner.processing_events()
        self.update()

    def bnr_chip_event_func(self, event):
        self.banner.chip_event_events(event)
        self.update()

    def bnr_create_on_change_events(self):
        self.banner.material.on_change = self.bnr_material_func
        self.banner.processing.on_change = self.bnr_processing_func
        for data in self.banner.side_data.values():
            data['obj'].on_select = self.bnr_chip_event_func

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=self.create_main_fields(),
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            ),
            padding=20,
            margin=10,
            width=500
        )

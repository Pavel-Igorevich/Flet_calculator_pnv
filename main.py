import flet as ft

from banner.banner_gui import BannerGUI
from canvas.canvas_gui import CanvasGUI
from orders.orders_gui import OrdersGUI
from plastic.plastic_gui import PlasticGUI
from construction.construction_gui import ConstructionsGUI
from sheet_materials.sheet_materials_gui import SheetMaterialsGUI


class MainMenu:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.main_price, self.main_sale_price, self.coefficient = None, None, None
        self.result_modal = None
        self.main_content = None
        self.enable_user_control = None

    def close_banner(self, _event):
        self.page.banner.open = False
        self.page.update()

    def settings(self):
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.colors.YELLOW,
        )
        self.page.banner = ft.Banner(
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.RED_500, size=40),
            content=ft.Text(
                "Исправьте выделенные поля чтобы произошел расчет!",
                color=ft.colors.RED_500
            ),
            actions=[
                ft.TextButton(
                    "Понятно",
                    on_click=self.close_banner,
                    style=ft.ButtonStyle(
                        color={ft.MaterialState.DEFAULT: ft.colors.WHITE},
                        bgcolor={ft.MaterialState.DEFAULT: ft.colors.RED_500}
                    )
                )
            ],
        )

        self.main_price = ft.TextSpan('', ft.TextStyle(weight=ft.FontWeight.W_700))
        self.main_sale_price = ft.TextSpan('', ft.TextStyle(weight=ft.FontWeight.W_700))
        self.coefficient = ft.TextSpan('', ft.TextStyle(weight=ft.FontWeight.W_700))

        def close_dlg(_event):
            self.result_modal.open = False
            self.page.update()

        style_btn_modal = ft.ButtonStyle(
            bgcolor=ft.colors.AMBER, color=ft.colors.BLACK, padding={ft.MaterialState.DEFAULT: 10}
        )
        self.result_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Результат расчета", text_align=ft.TextAlign.CENTER),
            content_padding=ft.padding.symmetric(vertical=20, horizontal=10),
            actions=[
                ft.ResponsiveRow(
                    [
                        ft.Text(
                            text_align=ft.TextAlign.CENTER,
                            spans=[
                                ft.TextSpan('Общая себестоимость: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                                self.main_price
                            ],
                            col={'xs': 12, 'sm': 4}
                        ),
                        ft.Text(
                            text_align=ft.TextAlign.CENTER,
                            spans=[
                                ft.TextSpan('Коэффициент: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                                self.coefficient
                            ],
                            col={'xs': 12, 'sm': 4}
                        ),
                        ft.Text(
                            text_align=ft.TextAlign.CENTER,
                            spans=[
                                ft.TextSpan('Общая стоимость: ', ft.TextStyle(weight=ft.FontWeight.W_200)),
                                self.main_sale_price
                            ],
                            col={'xs': 12, 'sm': 4}
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(),
                ft.Container(
                    ft.ResponsiveRow(
                        [
                            ft.TextButton(
                                "Сохранить в файл", on_click=close_dlg, col={'xs': 12, 'sm': 6}, style=style_btn_modal
                            ),
                            ft.TextButton(
                                "Закрыть", on_click=close_dlg, col={'xs': 12, 'sm': 6}, style=style_btn_modal
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    margin=ft.margin.only(top=10)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.dialog = self.result_modal

    def show_drawer(self, _event):
        self.page.drawer.open = True
        self.page.drawer.update()

    def test(self, _event):
        index = self.page.drawer.selected_index
        self.page.remove(self.enable_user_control)
        if index == 0:
            self.enable_user_control = OrdersGUI(
                self.page,
                self.main_price,
                self.main_sale_price,
                self.coefficient
            )
        elif index == 1:
            self.enable_user_control = BannerGUI(
                self.page,
                self.main_price,
                self.main_sale_price,
                self.coefficient
            )
        elif index == 2:
            self.enable_user_control = SheetMaterialsGUI(
                self.page,
                self.main_price,
                self.main_sale_price,
                self.coefficient
            )
        elif index == 3:
            self.enable_user_control = PlasticGUI(
                self.page,
                self.main_price,
                self.main_sale_price,
                self.coefficient
            )
        elif index == 4:
            self.enable_user_control = CanvasGUI(
                self.page,
                self.main_price,
                self.main_sale_price,
                self.coefficient
            )
        elif index == 5:
            self.enable_user_control = ConstructionsGUI(
                self.page,
                self.main_price,
                self.main_sale_price,
                self.coefficient
            )
        else:
            self.enable_user_control = self.main_content

        self.page.drawer.open = False
        self.page.add(self.enable_user_control)

    def create_window(self):
        self.main_content = OrdersGUI(
            self.page,
            self.main_price,
            self.main_sale_price,
            self.coefficient
        )
        menu_button = ft.IconButton(
            icon=ft.icons.MENU,
            icon_size=30,
            tooltip="Выбор материала",
            on_click=self.show_drawer,
        )
        self.page.drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(padding=12),
                ft.NavigationDrawerDestination(
                    icon=ft.icons.ARCHIVE_ROUNDED,
                    label='Список расчетов'
                ),
                ft.Divider(),
                ft.NavigationDrawerDestination(
                    label="Баннер",
                ),
                ft.NavigationDrawerDestination(
                    label="Листовые материалы",
                ),
                ft.NavigationDrawerDestination(
                    label="Плёнка",
                ),
                ft.NavigationDrawerDestination(
                    label="Холст",
                ),
                ft.NavigationDrawerDestination(
                    label="Конструкции",
                ),
            ],
            on_change=self.test,
        )

        self.page.appbar = ft.AppBar(
            leading=menu_button,
            title=ft.Text("Калькулятор материалов"),
            center_title=True,
        )
        self.enable_user_control = self.main_content
        self.page.add(self.enable_user_control)

    def run_main_menu(self):
        self.create_window()
        self.settings()
        self.page.add()


def run_app(page: ft.Page):
    menu = MainMenu(page)
    menu.run_main_menu()


if __name__ == '__main__':
    # ft.app(run_app, view=ft.AppView.WEB_BROWSER, port=8080)
    ft.app(run_app, upload_dir="files")

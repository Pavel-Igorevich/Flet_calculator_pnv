import flet as ft

from data import DATA
from other_func import card, checking_size, checking_quantity


class ConstructionsGUI:

    def __init__(self, page, main_price, main_sale_price, coefficient):
        super().__init__()
        self.page = page
        self.main_price, self.main_sale_price, self.coefficient = main_price, main_sale_price, coefficient


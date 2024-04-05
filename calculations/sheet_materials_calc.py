from calculations.default_calc_func import square_calc, find_coefficient, amount_str
from data import MAIN_DATA

DATA = MAIN_DATA['Листовые материалы']


def material_calc(data):
    name_mat = data['material']['name']
    type_mat = data['material']['type']
    thickness_mat = data['material']['thickness']
    material_name = DATA['Материал']
    if material_name[name_mat]['Вид'].get(type_mat):
        prices = material_name[name_mat]['Вид'][type_mat]['Толщина'][thickness_mat]
    else:
        prices = material_name[name_mat]['Вид'][None]['Толщина'][thickness_mat]
    price = prices['Себестоимость']
    sale_price = prices['Продажа']
    if name_mat == 'ЛДСП' and data['material']['edge'] == 'Добавить':
        sale_price *= 2
        price *= 2
    return price, sale_price


def processing_calc(data):
    processing_name = DATA['Обработка']
    prices_type_cut = processing_name['Вид резки'][data['processing']['type_cut']]
    price_cut = prices_type_cut['Себестоимость']
    sale_price_cut = prices_type_cut['Продажа']

    prices_holder = processing_name['Держатель'][data['processing']['holder']]
    price_holder = prices_holder['Себестоимость']
    sale_price_holder = prices_holder['Продажа']

    if data['processing']['rolling_film'] == "Не требуется" or not data['processing']['rolling_film']:
        coefficient_film = 1
    else:
        coefficient_film = 0.9

    price = price_cut
    sale_price = sale_price_cut

    if price_holder and sale_price_holder:
        price += price_holder
        sale_price += sale_price_holder
    if data['processing']['rolling_film']:
        prices_film = DATA['Обработка']['Накатка пленки'][data['processing']['rolling_film']]
        price_film = prices_film['Себестоимость']
        sale_price_film = prices_film['Продажа']
        price += price_film
        sale_price += sale_price_film

    return price, sale_price, coefficient_film


def backlighting_calc(data):
    light_data = DATA['Световое исполнение']
    backlighting_type = data['backlighting']['type']
    if backlighting_type == 'Не требуется':
        return 0, 0
    prices_type = light_data['Вид подсветки'][backlighting_type]
    price_type = prices_type['Себестоимость']
    sale_price_type = prices_type['Продажа']
    price, sale_price = price_type, sale_price_type

    prices_color = light_data['Цвет света'][data['backlighting']['color']]
    price_color = prices_color['Себестоимость']
    sale_price_color = prices_color['Продажа']
    price += price_color
    sale_price += sale_price_color

    prices_type_light = light_data['Вид света'][data['backlighting']['type_light']]
    price_type_light = prices_type_light['Себестоимость']
    sale_price_type_light = prices_type_light['Продажа']
    price += price_type_light
    sale_price += sale_price_type_light

    if data['backlighting']['cable']:
        prices_cable = light_data['Дополнительный провод']
        price += prices_cable['Себестоимость'] * int(data['backlighting']['cable'])
        sale_price += prices_cable['Продажа'] * int(data['backlighting']['cable'])

    return price, sale_price


def main_calc(data):
    height = float(data['height'])
    width = float(data['width'])
    quantity = int(data['quantity'])
    square = square_calc(height, width)
    price_material, sale_price_material = material_calc(data)
    price_processing, sale_price_processing, coefficient_processing = processing_calc(data)
    price_backlighting, sale_price_backlighting = backlighting_calc(data)

    if DATA['Коэффициент']:
        coefficient = find_coefficient(square, DATA['Коэффициент'])
    else:
        coefficient = 1
    main_price = round(
        (price_material + price_processing + price_backlighting)
        * coefficient_processing * square * quantity
    )
    main_sale_price = round(
        (sale_price_material + sale_price_processing + sale_price_backlighting)
        * coefficient_processing * square * quantity * coefficient
    )
    data['material']['price'] = amount_str(price_material)
    data['material']['sale_price'] = amount_str(sale_price_material)

    data['processing']['price'] = amount_str(price_processing)
    data['processing']['sale_price'] = amount_str(sale_price_processing)

    data['height'] = height
    data['width'] = width
    data['size'] = square
    data['coefficient'] = coefficient
    data['sheet_main_price'] = amount_str(main_price)
    data['sheet_main_sale_price'] = amount_str(main_sale_price)
    if data.get('plastic'):
        data['main_price'] = amount_str(main_price + data['plastic']['float_main_price'])
        data['main_sale_price'] = amount_str(main_sale_price + data['plastic']['float_main_sale_price'])
    else:
        data['main_price'] = data['sheet_main_price']
        data['main_sale_price'] = data['sheet_main_sale_price']

    return data

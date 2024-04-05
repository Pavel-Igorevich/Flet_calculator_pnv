from calculations.default_calc_func import perimeter_calc, square_calc, find_coefficient, amount_str
from data import MAIN_DATA

DATA_PLASTIC = MAIN_DATA['Плёнка']


def material_calc(material):
    name = material['name']
    quality = material['print_quality']
    if name != 'Oracal цветная':
        print_quality_data = DATA_PLASTIC['Материал'][name]['Качество печати']
        if 'Без печати' == quality:
            price_material = print_quality_data[quality]
            sale_price_material = price_material
        else:
            price_material = print_quality_data[quality]['Себестоимость']
            sale_price_material = print_quality_data[quality]['Продажа']
    else:
        oracal_data = DATA_PLASTIC['Материал'][name]
        price_material, sale_price_material = oracal_data['Себестоимость'], oracal_data['Продажа']

    return price_material, sale_price_material


def processing_calc(processing):
    process_name = processing['processing']
    data_process = DATA_PLASTIC['Обработка']['Вид обработки'][process_name]
    size_label = 'Площадь'
    if "Плоттер" == process_name:
        if processing['sampling_method'] == 'Без выборки':
            sampling_price = data_process['Вид выборки']['Без выборки']['Себестоимость']
            sampling_sale_price = data_process['Вид выборки']['Без выборки']['Продажа']
        else:
            sampling_complexity = data_process['Вид выборки'][processing['sampling_method']]['Сложность выборки']
            prices_sampling_complexity = sampling_complexity[processing['sampling_complexity']]
            sampling_price = prices_sampling_complexity['Себестоимость']
            sampling_sale_price = prices_sampling_complexity['Продажа']
        mounting_plastic = DATA_PLASTIC['Обработка']['Вид обработки'][process_name]['Монтажная пленка']
        prices_mounting_plastic = mounting_plastic[processing['mounting_plastic']]
        mounting_price = prices_mounting_plastic['Себестоимость']
        mounting_sale_price = prices_mounting_plastic['Продажа']
        price_process, sale_price_process = sampling_price + mounting_price, sampling_sale_price + mounting_sale_price
    else:
        if process_name == 'Резка с запасом':
            size_label = 'Периметр'
        price_process, sale_price_process = data_process['Себестоимость'], data_process['Продажа']

    if processing['lamination']:
        lamination_prices = DATA_PLASTIC['Обработка']['Ламинация'][processing['lamination']]
        lamination_price, lamination_sale_price = lamination_prices['Себестоимость'], lamination_prices['Продажа']
    else:
        lamination_price, lamination_sale_price = 0, 0
    return price_process, sale_price_process, lamination_price, lamination_sale_price, size_label


def main_calc(data):
    height = float(data['height'])
    width = float(data['width'])
    quantity = int(data['quantity'])
    square = square_calc(height, width)
    price_material, sale_price_material = material_calc(data['material'])
    data_process = processing_calc(data['processing'])
    price_processing, sale_price_processing, lamination_price, lamination_sale_price, size_label = data_process
    if DATA_PLASTIC['Коэффициент']:
        coefficient = find_coefficient(square, DATA_PLASTIC['Коэффициент'])
    else:
        coefficient = 1

    if size_label == 'Периметр':
        multiplier_process = perimeter_calc(height, width)
    else:
        multiplier_process = square

    main_price = round(
        ((lamination_price + price_material) * square)
        + (price_processing * multiplier_process) * quantity
    )
    main_sale_price = round(
        (((lamination_sale_price + sale_price_material) * square)
         + (sale_price_processing * multiplier_process) * quantity) * coefficient
    )
    data['material']['price'] = amount_str(price_material)
    data['material']['sale_price'] = amount_str(sale_price_material)

    data['processing']['price'] = amount_str(price_processing)
    data['processing']['sale_price'] = amount_str(sale_price_processing)
    data['processing']['lamination_price'] = amount_str(lamination_price)
    data['processing']['lamination_sale_price'] = amount_str(lamination_sale_price)

    data['height'] = height
    data['width'] = width
    data['size'] = square
    data['coefficient'] = coefficient
    data['main_price'] = amount_str(main_price)
    data['main_sale_price'] = amount_str(main_sale_price)
    data['float_main_price'] = main_price
    data['float_main_sale_price'] = main_sale_price

    return data

from data import DATA
from calculations.default_calc_func import perimeter_calc, square_calc, find_coefficient, amount_str

DATA_BANNER = DATA['Баннер']


def material_calc(quality, material):
    print_quality_data = DATA_BANNER['Материал'][material]['Качество печати']
    if 'Без печати' == quality:
        price_material = print_quality_data[quality]
        sale_price_material = price_material
    else:
        price_material = print_quality_data[quality]['Себестоимость']
        sale_price_material = print_quality_data[quality]['Продажа']
    material_name = DATA_BANNER['Материал'][material]['Материал']
    return price_material, sale_price_material, material_name


def processing_calc(welding_step, processing, height, width, sides):
    processing_data = DATA_BANNER['Обработка'][processing]
    perimeter = perimeter_calc(height, width)
    if welding_step:
        price_processing = processing_data["Шаг сварки"][welding_step]['Себестоимость']
        sale_price_processing = processing_data["Шаг сварки"][welding_step]['Продажа']
    else:
        price_processing = processing_data['Себестоимость']
        sale_price_processing = processing_data['Продажа']
    process_material = processing_data.get('Материал') or None
    len_processing_sides = 0
    if sides:
        values_to_check = ['Правая', 'Левая', 'Верх', 'Низ', 'Все стороны', 'По углам']
        for value in values_to_check:
            if value in sides:
                if value in ['Правая', 'Левая']:
                    len_processing_sides += float(height) / 1000
                elif value in ['Все стороны', 'По углам']:
                    len_processing_sides += perimeter
                else:
                    len_processing_sides += float(width) / 1000
        len_processing_sides = len_processing_sides
        price_processing = round(price_processing * len_processing_sides, 2)
        sale_price_processing = round(sale_price_processing * len_processing_sides, 2)
    else:
        price_processing = price_processing * perimeter
        sale_price_processing = sale_price_processing * perimeter
    return price_processing, sale_price_processing, process_material, len_processing_sides


def main_calc(data):
    height = float(data['height'])
    width = float(data['width'])
    quantity = int(data['quantity'])
    perimeter = perimeter_calc(height, width)
    square = square_calc(height, width)
    
    price_material, sale_price_material, material_name = material_calc(
        quality=data['material']['print_quality'],
        material=data['material']['name'],
    )
    
    material_consumption = round(square * quantity, 2)
    
    price_processing, sale_price_processing, process_material, len_processing_sides = processing_calc(
        welding_step=data['processing']['welding_step'],
        processing=data['processing']['type'],
        height=height,
        width=width,
        sides=data['processing']['sides'],
    )
    if DATA_BANNER['Коэффициент']:
        coefficient = find_coefficient(square, DATA_BANNER['Коэффициент'])
    else:
        coefficient = 1
    main_price = round((price_material + price_processing) * square * quantity, 2)
    main_sale_price = (sale_price_material + sale_price_processing) * square * quantity
    main_sale_price = round(main_sale_price * coefficient, 2)
    if data['processing']['sides']:
        if 'Установка люверса с проваркой' == data['processing']:
            process_consumption = round(
                (len_processing_sides / float(data['processing']['welding_step'].split(' ')[0]))
                * quantity,
                2
            )
        else:
            process_consumption = round(len_processing_sides * quantity, 2)
    else:
        if data['processing'] == 'Натяжка на подрамник 27мм*12мм':
            process_consumption = round(perimeter * quantity, 2)
        else:
            process_consumption = None
            
    data['material']['full_name'] = material_name
    data['material']['price'] = amount_str(price_material)
    data['material']['sale_price'] = amount_str(sale_price_material)
    data['material']['consumption'] = material_consumption

    data['processing']['price'] = amount_str(price_processing)
    data['processing']['sale_price'] = amount_str(sale_price_processing)
    data['processing']['consumption'] = process_consumption
    
    data['height'] = height
    data['width'] = width
    data['size'] = square
    data['coefficient'] = coefficient
    data['main_price'] = amount_str(main_price)
    data['main_sale_price'] = amount_str(main_sale_price)
    
    return data

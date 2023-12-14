from data import DATA
from calculations.default_calc_func import perimeter_calc, square_calc, find_coefficient, amount_str

DATA_CANVAS = DATA['Холст']


def main_calc(data):
    height = float(data['height'])
    width = float(data['width'])
    quantity = int(data['quantity'])
    square = square_calc(height, width)
    perimeter = perimeter_calc(height, width)

    coefficient = find_coefficient(square, DATA_CANVAS['Коэффициент'])
    
    data_material = data['material']['name']
    price_material = DATA_CANVAS['Материал'][data_material]['Себестоимость'] * square
    sale_price_material = DATA_CANVAS['Материал'][data_material]['Продажа'] * square
    price_material *= quantity
    sale_price_material *= quantity
    
    data_processing = data['processing']['type']
    price_processing = DATA_CANVAS['Обработка'][data_processing]['Себестоимость'] * perimeter
    sale_price_processing = DATA_CANVAS['Обработка'][data_processing]['Продажа'] * perimeter
    price_processing *= quantity
    sale_price_processing *= quantity
    
    main_price = round(price_material + price_processing, 2)
    main_sale_price = sale_price_material + sale_price_processing
    main_sale_price = round(main_sale_price * coefficient, 2)
    material_name = DATA_CANVAS['Материал'][data_material]['Материал']
    material_consumption = round(square * quantity, 2)
    process_material = DATA_CANVAS['Обработка'][data_processing].get('Материал') or None
    process_consumption = None
    if process_material:
        process_consumption = round(perimeter * quantity, 2)

    material = DATA['Холст']['Обработка'][data_processing].get('Материал')
    data['processing']['material'] = material
    
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

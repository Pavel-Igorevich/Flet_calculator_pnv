def perimeter_calc(length, width):
    return round((length / 1000 + width / 1000) * 2, 2)


def square_calc(length, width):
    square = (length / 1000) * (width / 1000)
    if square < 0.1:
        square = 0.1
    return round(square, 2)


def find_coefficient(value, coefficient_dict):
    for coefficient, (lower_bound, upper_bound) in coefficient_dict.items():
        if lower_bound <= value < upper_bound if upper_bound is not None else True:
            return coefficient
    return None


def amount_str(value):
    return "{:,.2f}".format(value).replace(',', '\xa0')


# if __name__ == '__main__':
#     area_square_meters = (12 * 12) / 1000000
#     print(area_square_meters)
#     print(square_calc(12, 12))

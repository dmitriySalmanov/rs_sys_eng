g = 9.80665
ib_const = 2.20462
kgf = 453.59237


def kN(value=1, unit_key='кг'):

    """
    Описание: Функция переводит единицы измерения сил в килоньютон
    Принимает: value - int, float; unit_key - str(кг, Н, Т, МН, мН, даН, фунт, кип)
    Возвращает: float (переведенные в кН значения)
    """

    if unit_key == 'кг':
        return (value * g) / 1000
    elif unit_key == 'Н':
        return value / 1000
    elif unit_key == 'Т':
        return (value * 1000 * g) / 1000
    elif unit_key == 'МН':
        return (value * (10 ** 6)) / 1000
    elif unit_key == 'мН':
        return (value / 1000) / 1000
    elif unit_key == 'даН':
        return (value * 10) / 1000
    elif unit_key == 'фунт':
        return ((value / ib_const) * g) / 1000
    elif unit_key == 'кип':
        return ((value * kgf) * g) / 1000
    else:
        return 1


def N(value=1, unit_key='кг'):

    """
    Описание: Функция переводит единицы измерения сил в ньютон
    Принимает: value - int, float; unit_key - str(кг, Н, Т, МН, мН, даН, фунт, кип)
    Возвращает: float (переведенные в Н значения)
    """

    if unit_key == 'кг':
        return value * g
    elif unit_key == 'кН':
        return value * 1000
    elif unit_key == 'Т':
        return value * 1000 * g
    elif unit_key == 'МН':
        return value * (10 ** 6)
    elif unit_key == 'мН':
        return value / 1000
    elif unit_key == 'даН':
        return value * 10
    elif unit_key == 'фунт':
        return (value / ib_const) * g
    elif unit_key == 'кип':
        return (value * kgf) * g
    else:
        return 1

'''
print('кг - Н ',N(500.56, 'кг'))
print('кН - Н ',N(28.71, 'кН'))
print('Т - Н ',N(1.65, 'Т'))
print('МН - Н ',N(5000.68, 'МН'))
print('мН - Н ',N(612.5, 'мН'))
print('даН - Н ',N(6621.19, 'даН'))
print('фунт - Н ',N(311.9, 'фунт'))
print('кип - Н ',N(12.38, 'кип'))
'''
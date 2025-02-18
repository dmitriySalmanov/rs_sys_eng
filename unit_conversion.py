g = 9.80665
ib_const = 2.20462
kgf = 453.59237
ibn_const = 4.44822
import math


def convert(value=1, unit='kg', to_unit='kN'):
    # Силы
    if to_unit == 'kN':
        if unit == 'kg':
            return (value * g) / 1000
        elif unit == 'N':
            return value / 1000
        elif unit == 'T':
            return (value * 1000 * g) / 1000
        elif unit == 'MN':
            return (value * (10 ** 6)) / 1000
        elif unit == 'mN':
            return (value / 1000) / 1000
        elif unit == 'daN':
            return (value * 10) / 1000
        elif unit == 'ib':
            return ((value / ib_const) * g) / 1000
        elif unit == 'kip':
            return ((value * kgf) * g) / 1000
        else:
            return value

    if to_unit == 'N':
        if unit == 'kg':
            return value * g
        elif unit == 'kN':
            return value * 1000
        elif unit == 'T':
            return value * 1000 * g
        elif unit == 'MN':
            return value * (10 ** 6)
        elif unit == 'mN':
            return value / 1000
        elif unit == 'daN':
            return value * 10
        elif unit == 'ib':
            return (value / ib_const) * g
        elif unit == 'kip':
            return (value * kgf) * g
        else:
            return value

    if to_unit == 'kg':
        if unit == 'N':
            return value / g
        elif unit == 'kN':
            return (value * 1000) / g
        elif unit == 'T':
            return value * 1000
        elif unit == 'MN':
            return (value * (10 ** 6)) / g
        elif unit == 'mN':
            return (value / 1000) / g
        elif unit == 'daN':
            return (value * 10) / g
        elif unit == 'ib':
            return value / ib_const
        elif unit == 'kip':
            return value * kgf
        else:
            return value

    if to_unit == 'mN':
        if unit == 'N':
            return value * 1000
        elif unit == 'kN':
            return value * 1000 * 1000
        elif unit == 'T':
            return ((value * 1000) * g) * 1000
        elif unit == 'MN':
            return (value * 10 ** 6) * 1000
        elif unit == 'kg':
            return value * g * 1000
        elif unit == 'daN':
            return (value * 10) * 1000
        elif unit == 'ib':
            return (value / ib_const) * g * 1000
        elif unit == 'kip':
            return value * kgf * g * 1000
        else:
            return value

    if to_unit == 'MN':
        if unit == 'N':
            return value / 10 ** 6
        elif unit == 'kN':
            return (value * 1000) / 10 **6
        elif unit == 'T':
            return (value * 1000 * g) / 10 ** 6
        elif unit == 'mN':
            return (value / 1000) / 10 ** 6
        elif unit == 'kg':
            return (value * g) / 10 ** 6
        elif unit == 'daN':
            return (value * 10) / 10 ** 6
        elif unit == 'ib':
            return ((value / ib_const) * g) / 10 ** 6
        elif unit == 'kip':
            return (value * kgf * g) / 10 ** 6
        else:
            return value

    if to_unit == 'daN':
        if unit == 'N':
            return value / 10
        elif unit == 'kN':
            return (value * 1000) / 10
        elif unit == 'kg':
            return (value * g) / 10
        elif unit == 'T':
            return (value * 1000 * g) / 10
        elif unit == 'mN':
            return (value / 1000) / 10
        elif unit == 'MN':
            return (value * (10 ** 6)) / 10
        elif unit == 'ib':
            return ((value / ib_const) * g) / 10
        elif unit == 'kip':
            return (value * kgf * g) / 10
        else:
            return value

    if to_unit == 'ib':
        if unit == 'N':
            return (value / g) * ib_const
        elif unit == 'kN':
            return ((value * 1000) / g) * ib_const
        elif unit == 'kg':
            return value * ib_const
        elif unit == 'T':
            return value * 1000 * ib_const
        elif unit == 'mN':
            return ((value / 1000) / g) * ib_const
        elif unit == 'MN':
            return ((value * (10 ** 6)) / g) * ib_const
        elif unit == 'daN':
            return ((value * 10) / g) * ib_const
        elif unit == 'kip':
            return value * kgf * ib_const
        else:
            return value

    if to_unit == 'kip':
        if unit == 'N':
            return (value / g) / kgf
        elif unit == 'kN':
            return ((value * 1000) / g) / kgf
        elif unit == 'kg':
            return value / kgf
        elif unit == 'T':
            return (value * 1000) / kgf
        elif unit == 'mN':
            return ((value / 1000) / g) / kgf
        elif unit == 'MN':
            return ((value * (10 ** 6)) / g) / kgf
        elif unit == 'daN':
            return ((value * 10) / g) / kgf
        elif unit == 'ib':
            return (value / ib_const) / kgf
        else:
            return value

    if to_unit == 'T':
        if unit == 'N':
            return (value / g) / 1000
        elif unit == 'kN':
            return ((value * 1000) / g) / 1000
        elif unit == 'kg':
            return value / 1000
        elif unit == 'mN':
            return ((value / 1000) / g) / 1000
        elif unit == 'MN':
            return ((value * (10 ** 6)) / g) / 1000
        elif unit == 'daN':
            return ((value * 10) / g) / 1000
        elif unit == 'ib':
            return (value / ib_const) / 1000
        elif unit == 'kip':
            return (value * kgf) / 1000
        else:
            return value

    # Линейные размеры
    if to_unit == 'mm':
        if unit == 'cm':
            return value * 10
        elif unit == 'm':
            return value * 1000
        elif unit == 'inch':
            return value * 25.4
        elif unit == 'foot':
            return value * 304.8
        else:
            return value

    if to_unit == 'cm':
        if unit == 'mm':
            return value * 0.1
        elif unit == 'm':
            return value * 100
        elif unit == 'inch':
            return value * 2.54
        elif unit == 'foot':
            return value * 30.48
        else:
            return value

    if to_unit == 'm':
        if unit == 'mm':
            return value * 0.001
        elif unit == 'cm':
            return value * 0.01
        elif unit == 'inch':
            return value * 0.0254
        elif unit == 'foot':
            return value * 0.3048
        else:
            return value

    if to_unit == 'inch':
        if unit == 'mm':
            return value * 0.03937
        elif unit == 'cm':
            return value * 0.3937
        elif unit == 'm':
            return value * 39.37008
        elif unit == 'foot':
            return value * 12
        else:
            return value

    if to_unit == 'foot':
        if unit == 'mm':
            return value * 0.00328
        elif unit == 'cm':
            return value * 0.03281
        elif unit == 'm':
            return value * 3.28084
        elif unit == 'inch':
            return value * 0.08333
        else:
            return value

    # Углы
    if to_unit == 'degrees':
        if unit == 'radians':
            return value * (180/math.pi)
        else:
            return value

    if to_unit == 'radians':
        if unit == 'degrees':
            return value * (math.pi/180)
        else:
            return value

    # Моменты инерции
    if to_unit == 'mm4':
        if unit == 'cm4':
            return value * (10**4)
        elif unit == 'm4':
            return value * (10**12)
        else:
            return value

    if to_unit == 'cm4':
        if unit == 'mm4':
            return value / (10**4)
        elif unit == 'm4':
            return value * (10**8)
        else:
            return value

    if to_unit == 'm4':
        if unit == 'mm4':
            return value / (10**12)
        elif unit == 'cm4':
            return value / (10**8)
        else:
            return value

    # Моменты сопротивления
    if to_unit == 'mm3':
        if unit == 'cm3':
            return value * (10**3)
        elif unit == 'm3':
            return value * (10**9)
        else:
            return value

    if to_unit == 'cm3':
        if unit == 'mm3':
            return value / (10**3)
        elif unit == 'm3':
            return value * (10**6)
        else:
            return value

    if to_unit == 'm3':
        if unit == 'mm3':
            return value / (10**9)
        elif unit == 'cm3':
            return value / (10**6)
        else:
            return value
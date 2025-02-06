g = 9.80665
ib_const = 2.20462
kgf = 453.59237
ibn_const = 4.44822


def convert(value=1, unit='kg', to_unit='kN'):

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
            return 1

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
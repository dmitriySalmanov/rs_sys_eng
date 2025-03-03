import pandas as pd
import numpy as np
from unit_conversion import *


def clear_and_calculate(df, console_length=0.1, sensors_distance=100):
    '''
    -Описание: Функция для очистки и математических преобразований данных полученых из испытательной машины. Структура
                данных очень конкретизирована и должна соблюдать определенный порядок (смотри df.columns)
    -Принимает: df - dataFrame, console_length - float значение  длины консоли, sensors_distance - float/int значение
                расстояния между датчиками
    -Возвращает: df
    '''

    # Проверка console_length и sensors_distance на равенство 0
    try:
        if console_length == 0:
            raise ValueError("Ошибка: Длина консоли не должен быть равен 0!")
        if sensors_distance == 0:
            raise ValueError("Ошибка: Расстояние между датчиками не должен быть равен 0!")
    except ValueError as e:
        print(e)
        return None

    # Удаление первых 3-х столбцов (лишние в этом пакете данных) и переименование столбцов
    df = df.drop(df.columns[:3], axis=1)
    df.columns = ['Усилия, N', 'Время, sec', 'Перемещения цилиндра, mm', 'Перемещения цилиндра 1, mm',
                  'Перемещения цилиндра 2, mm', 'Перемещения цилиндра 3, mm', 'Перемещения цилиндра 4, mm',
                  'Перемещения цилиндра 5, mm', 'Перемещения цилиндра 6, mm', 'Перемещения цилиндра 7, mm',
                  'Перемещения цилиндра 8, mm',]

    df['Усилия, N'] = (df['Усилия, N'] * -1).apply(convert, unit='N', to_unit='kN')
    df['Усилия, N'] = df['Усилия, N'].round(10)

    df['Моменты сил, kN * m'] = df['Усилия, N'] * console_length

    df['Среднее значение перемещения верхних датчиков, mm'] = ((df['Перемещения цилиндра 2, mm'] +
                                                               df['Перемещения цилиндра 4, mm']) / 2)

    df['Среднее значение перемещения нижних датчиков, mm'] = ((df['Перемещения цилиндра 3, mm'] +
                                                               df['Перемещения цилиндра 5, mm']) / 2)

    df['Угол наклона, rad'] = ((df['Среднее значение перемещения верхних датчиков, mm'] -
                               df['Среднее значение перемещения нижних датчиков, mm']) / sensors_distance) * -1
    df['Угол наклона, rad'] = df['Угол наклона, rad'].round(6)
    return df


df = pd.read_excel('D:/Projects/Calculation and analysis of RS/12_22_2023_Испытание 2_СИ90_20+ТН_120_40_15.xlsm')
df = clear_and_calculate(df, 0.4, 132)
print(df.head(10))



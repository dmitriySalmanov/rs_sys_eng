import pandas as pd
import ast
import re
import numpy as np
from unit_conversion import smart_convert
from typing import Tuple, Optional

# Константы
Q_PH = 50.9684  # кг — Нагрузка на балку при размещении груза
KB_V = 100  # Жесткость соединения траверсы со стойкой в горизонтальной плоскости


def format_section_name(row) -> str:
    """
    Формирует строку-название сечения из колонок:
    Производитель + (Спецификация если есть) + Серия + Высота × Ширина × Толщина
    """
    manufacturer = row.get('Производитель', '')
    specification = row.get('Спецификация', '')
    series = row.get('Серия', '')
    height = int(row.get('Высота (mm)', ''))
    width = int(row.get('Ширина (mm)', ''))
    thickness = int(row.get('Толщина стали (mm*10)', ''))

    spec_part = f"{specification}" if str(specification).strip().lower() not in ('нет', '0', 'nan', '', '0.0') else ''
    return f"{spec_part} {series}.{height}.{width}.{thickness}".strip()


def extract_base_stiffness(value, steel, load) -> float:
    """
    Возвращает значение жёсткости подпятника по заданной марке стали и нагрузке.
    Может принимать строку словаря, словарь или просто число.
    """
    try:
        if isinstance(value, str) and value.strip().startswith("{"):
            parsed = ast.literal_eval(value)
        elif isinstance(value, dict):
            parsed = value
        else:
            return float(value)

        if not isinstance(parsed, dict):
            return 0

        return parsed.get(steel, {}).get(load, 0)
    except Exception:
        return 0


def check_result(value: float, limit: float, check_type: str = 'Прочность') -> Tuple[str, bool]:
    """
    Проверка результатов расчета на соответствие предельному значению.
    Возвращает текстовое описание и булевый флаг (True/False).
    """
    diff = abs(value - limit)
    average = (value + limit) / 2
    percentage = int((diff / average) * 100)

    if check_type.lower() == 'прогиб':
        passed = value <= limit
    else:
        passed = (value / limit) <= 1

    status = f"Проходит на {percentage}%" if passed else f"Не проходит на {percentage}%"
    return status, passed


def check_flexibility(height_mm: float, width_mm: float, length_mm: float) -> bool:
    """
    Проверяет, находится ли сечение в безопасной зоне гибкости согласно приложению L.
    """
    if width_mm == 0:
        return False
    h_by_b = height_mm / width_mm
    if length_mm <= 3000:
        return h_by_b <= 3.5
    elif 3000 < length_mm <= 5000:
        max_ratio = 3.5 - (1.5 / 2000) * (length_mm - 3000)
        return h_by_b <= max_ratio
    return False


def extract_column_moment_inertia(node_support: str, df_all: pd.DataFrame) -> float:
    """
    Извлекает момент инерции стойки (Iz) по названию типа узла (например, 'Стойка ТВ.60.15')
    """
    try:
        match = re.match(r"Стойка (\S+)\.(\d+)\.(\d+)", node_support)
        if match:
            series, width, thickness = match.groups()
            width = int(width)
            thickness = int(thickness)
            row = df_all[
                (df_all["Тип сечения"].astype(str).str.lower().str.strip() == "стойка") &
                (df_all["Серия"].astype(str).str.strip() == series) &
                (pd.to_numeric(df_all["Ширина (mm)"], errors="coerce") == width) &
                (pd.to_numeric(df_all["Толщина стали (mm*10)"], errors="coerce") == thickness)
                ].iloc[0]
            return float(row.get("Iz", 0))
    except Exception:
        pass
    return 0


def check_beam_section(m_sdy, m_rdy, delta_max, delta_limit) -> Tuple[str, str, bool, bool]:
    """
    Объединенная проверка прочности и прогиба для вывода в таблицу.
    """
    durability = check_result(m_sdy, m_rdy, 'Прочность')
    deflection = check_result(smart_convert(delta_max, 'cm', 'mm'), delta_limit, 'Прогиб')
    return durability[0], deflection[0], durability[1], deflection[1]


def build_result_row(row, section_name, m_sdy, m_rdy, delta_max, weight, durability_str, deflection_str,
                     is_flexible_ok):
    """
    Сбор финальной строки с результатами расчета для одной балки
    """
    return {
        "Сечение": section_name,
        "Момент Msd (кг*м)": round(m_sdy, 2),
        "Расчётная прочность MRdy (кг*м)": round(m_rdy, 2),
        "Прогиб (мм)": round(smart_convert(delta_max, 'cm', 'mm'), 2),
        "Вес балки (кг)": round(weight, 2),
        "Проверка прочности": durability_str,
        "Проверка прогиба": deflection_str,
        "Проверка гибкости": "Проходит" if is_flexible_ok else "Не проходит"
    }


def _point_loads(length, Iy_cm4, E_kg_cm2, positions, forces):  #================================================
    """
    Возвращает (Mmax_kg, delta_max) для набора сосредоточенных сил опёртой балке.
    Аналитика через Маколая + граничные условия y(0)=y(L)=0, численный поиск максимумов на сетке.
    1) Определяем реакции опор:
        Балка лежит на двух опорах (слева и справа). Чтобы балка была в равновесии, программа сначала считает,
        какие силы "принимают на себя" левая и правая опоры (reaction_a и reaction_b).
        Это обычные уравнения статики:
        сумма сил = 0,
        сумма моментов = 0.
        Так мы знаем, как распределяется нагрузка между опорами
    2) Разбиваем балку на точки:
        Балка делится на мелкие шаги (примерно 2000 точек). В каждой точке программа будет считать момент и прогиб.
        Это нужно, чтобы найти где именно будет максимум.
    3) Строим моментную эпюру:
        Изгибающий момент в балке вычисляется по формулам через метод Маколая:
        M(x)=RA * x−∑Pk *⋅(x−xk)+
        В итоге программа получает кривую изгибающего момента вдоль балки и находит максимальное значение
    4) Вычисляем прогиб балки по формулам сопромата:
        EIy′′(x)=M(x)
        Прогиб считается интегрированием дважды.
        Чтобы уравнение имело смысл, вводятся две "константы интегрирования", которые подбираются так,
        чтобы прогиб на концах балки был равен нулю (балка ведь опирается на шарниры).
        Получаем кривую прогиба и ищем максимальное отклонение.
    """
    import numpy as np
    # Подготовка входных данных
    beam_length = float(length)
    points_positions = np.asarray(positions, dtype=float)
    points_forces = np.asarray(forces, dtype=float)
    if points_positions.size == 0:
        return 0.0, 0.0

    # Опорные реакции
    reaction_b = np.sum(points_forces * points_positions) / beam_length
    reaction_a = np.sum(points_forces) - reaction_b

    # Построение сетки вдоль балки, 3001 узел
    grid_points = np.linspace(0.0, beam_length, 3001)

    # Скобка Маколая для нагрузки P в точке x
    macaulay_terms = np.clip(grid_points[:, None] - points_positions[None, :], 0.0, None)

    # Изгибающий момент: M(x) = RA*x - Σ Pk ⟨x - xk⟩   (кг*см)
    Mx = reaction_a * grid_points - (macaulay_terms @ points_forces)  # массив значений изгибающего момента
    Mmax = float(np.max(np.abs(Mx)))

    # Прогиб (см): y'' = M / (E I)
    # Интегрирование (аналитические интегралы Маколая) + C1,C2 по y(0)=0, y(L)=0
    # theta = 1/(E I) * ( RA x^2/2 - (1/2) Σ Pk ⟨x - xk⟩^2 ) + C1
    # y     = 1/(E I) * ( RA x^3/6 - (1/6) Σ Pk ⟨x - xk⟩^3 ) + C1 x + C2
    squared_terms = (macaulay_terms ** 2) @ points_forces
    cubed_terms = (macaulay_terms ** 3) @ points_forces

    # Константы:
    # при x=0: y(0)=0 => C2=0
    # константа интегрирования по условию y(0)=0
    C2 = 0.0
    # при x=L: y(L)=0 => C1 = [ Σ Pk (L - xk)^3 - RA L^3 ] / (6 E I L)
    # константа интегрирования по условию y(L)=0
    C1 = (np.sum(points_forces * (beam_length - points_positions) ** 3) - reaction_a * beam_length ** 3) / (6.0 * E_kg_cm2 * Iy_cm4 * beam_length)
    # прогиб по классической схеме Эйлера–Бернулли с методом Маколая
    deflection_curve = (reaction_a * grid_points ** 3 / 6.0 - cubed_terms / 6.0) / (E_kg_cm2 * Iy_cm4) + C1 * grid_points + C2
    delta_max = float(np.max(np.abs(deflection_curve)))

    return Mmax, delta_max


def calculate_all_beams(
        df_sections: pd.DataFrame,
        df_all: pd.DataFrame,
        material_props: dict,
        length: float,
        load: float,
        gamma_g: float,
        gamma_q_omega: float,
        gamma_q_f: float,
        reduction_factor_i: float,
        reduction_factor_w: float,
        gamma_mb: float,
        load_factor: float,
        modulus_elasticity: float,
        node_support,
        section_rotation: bool,
        coefficient_n: float,
        height: float,
        beta_m: float,
        beta_teta: float,
        beta_delta: float,
        n_forces,
        deflection_check: int,
        point_loads: Optional[list] = None
) -> pd.DataFrame:
    """
    Основная функция расчета всех балок.
    Принимает геометрию, нагрузки, параметры расчета, возвращает датафрейм с результатами.

    df_sections - фильтрованная база данных сечений
    df_all - вся база данных сечений
    material_props - характеристики материалов
    length - длина балки
    load - нагрузка
    gamma_g - Коэффициент надёжности по нагрузке для собственного веса
    gamma_q_omega - Коэффициент надёжности по нагрузке при расчёте по прочности
    gamma_q_f - Коэффициент надёжности по нагрузке при расчёте по прогибу
    reduction_factor_i - Коэффициент уменьшающий момент инерции траверсы
    reduction_factor_w - Коэффициент уменьшающий момент сопротивления траверсы
    gamma_mb - Коэффициент надёжности по материалу стали
    load_factor - Учет веса балки
    modulus_elasticity - Модуль упругости стали
    node_support - Узлы закрепления
    section_rotation - Поворот сечения на 90град
    coefficient_n - изменение упругих характеристик в зависимости от моментов на торцах балки/траверсы
    height - Высота до первого уровня
    beta_m - коэффициент для расчета моментов
    beta_teta - коэффициент для расчета моментов
    beta_delta - коэффициент для расчета моментов
    n_forces - Кол-во точек приложения силы (и флаг для собственных типов нагружения)
    deflection_check - Макс допустимый прогиб
    point_loads - массив расстояний и нагрузок для своих типов нагружения
    """
    results = []
    # Преобразование характеристик материала
    fy = float(material_props['Расчетное сопротивление стали (Ry), МПа'])  # Предел текучести стали траверсы (МПа)
    fy = smart_convert(fy, 'MPa', 'kg/cm2') * gamma_mb
    poisson_ratio = float(material_props['Коєффициент Пуассона (v)'])  # Коєффициент Пуассона
    modulus_elasticity = smart_convert(modulus_elasticity * 1000, 'N/mm2', 'kg/cm2')  # Модуль Юнга

    # Геометрические преобразования
    length_cm = smart_convert(length, 'm', 'cm')  # Длина балки
    height_cm = smart_convert(height, 'm', 'cm')  # Высота первого уровня
    delta_limit = smart_convert(length, 'm', 'mm') / deflection_check  # Предельный прогиб
    column_moment_inertia = extract_column_moment_inertia(node_support, df_all) if node_support != 'Шарнир' else 0

    # Фильтрация только балок
    df_sections = df_sections[df_sections["Классификация"].astype(str).str.lower().str.strip() == "балка"]

    for _, row in df_sections.iterrows():
        try:
            # Геометрические характеристики
            Iy = float(row.get("Iz" if section_rotation else "Iy", 0)) / reduction_factor_i
            Wy = float(row.get("Wz,макс." if section_rotation else "Wy,макс.", 0)) / reduction_factor_w
            G = float(row.get("G", 0))  # вес балки кг/м

            # Приведение нагрузок
            wd_omega = load * gamma_q_omega + (load_factor * G * length)  # для расчета прочности
            wd_f = load * gamma_q_f + (load_factor * G * length * gamma_g)  # для расчета прогиба

            # Проверка гибкости
            section_height_mm = float(row.get("Высота (mm)", 0))  # Высота профиля
            section_width_mm = float(row.get("Ширина (mm)", 0))  # Ширина профиля
            length_mm = smart_convert(length, 'm', 'mm')
            is_flexible_ok = check_flexibility(section_height_mm, section_width_mm, length_mm)
            section_name = format_section_name(row)

            if node_support == 'Шарнир' and n_forces != "own":
                # Расчёт прогиба и прочности при шарнире

                # Расчет макс прогиба в см
                delta_max = ((5 / 384) * (wd_f * length_cm ** 3) / (modulus_elasticity * Iy)) * beta_m

                # Расчёт макс момента в середине пролета кг * м
                m_sdy = (wd_omega * length_cm / 8) * beta_m
                m_sdy = smart_convert(m_sdy, 'cm', 'm')

                # Расчётная прочность балки кг * м
                m_rdy = Wy * smart_convert(fy, 'cm', 'm')
            elif node_support != 'Шарнир' and n_forces != "own":
                # Расчёт жёсткости и прогиба при упругом соединении

                # Жесткость соединения траверсы со стойкой в вертикальной плоскости
                kb = smart_convert(row.get(node_support, 0), 'kN', 'kg')
                kb = smart_convert(kb, 'm', 'cm') / (coefficient_n or 1)

                # Коэффициент влияния жесткости стойки на защемление траверсы
                ke = kb / (1 + (kb * height_cm / (
                            3 * modulus_elasticity * column_moment_inertia))) if column_moment_inertia else 0

                # Расчет макс прогиба в см
                delta_max = ((5 / 384) * (wd_f * length_cm ** 3) / (modulus_elasticity * Iy)) * beta_delta * (
                        1 - ((0.8 * beta_teta) / (beta_delta * (1 + 2 * modulus_elasticity * Iy / (ke * length_cm)))))

                # Расчёт макс момента в середине пролета кг * м
                m_sdy = (wd_omega * length_cm / 8) * beta_m * (
                        1 - ((2 / 3) * beta_teta) / (beta_m * (1 + 2 * modulus_elasticity * Iy / (ke * length_cm))))
                m_sdy = smart_convert(m_sdy, 'cm', 'm') * coefficient_n

                # Расчётная прочность балки кг * м
                m_rdy = Wy * smart_convert(fy, 'cm', 'm')

            elif node_support == 'Шарнир' and n_forces == "own":
                # Подготовка точек
                point_load_pairs  = point_loads or []
                if not point_load_pairs :
                    # нет нагрузок — пропускаем расчёт
                    continue

                # координаты сил (в см)
                load_positions_cm = np.array([smart_convert(xm, 'm', 'cm') for xm, _ in point_load_pairs ], dtype=float)
                # нагрузка (кг)
                load_forces_kg = np.array([float(Pkg) for _, Pkg in point_load_pairs ], dtype=float)

                # изгибающий момент
                max_bending_moment_cm = 0.0
                if load_forces_kg.size:
                    max_bending_moment_cm, _ = _point_loads(
                        length=smart_convert(length, 'm', 'cm'),
                        Iy_cm4=Iy,
                        E_kg_cm2=modulus_elasticity,
                        positions=load_positions_cm,
                        forces=load_forces_kg * gamma_q_omega + (load_factor * G * length)
                    )

                # Прогиб
                _, delta_max = _point_loads(
                    length=smart_convert(length, 'm', 'cm'),
                    Iy_cm4=Iy,
                    E_kg_cm2=modulus_elasticity,
                    positions=load_positions_cm,
                    forces=load_forces_kg * gamma_q_f + (load_factor * G * length * gamma_g)
                )

                # Расчёт макс момента в середине пролета кг * м
                m_sdy = smart_convert(max_bending_moment_cm , 'cm', 'm')

                # Расчётная прочность (кг*м)
                m_rdy = Wy * smart_convert(fy, 'cm', 'm')

            elif node_support != 'Шарнир' and n_forces == "own":
                # Подготовка точек
                point_load_pairs = point_loads or []
                if not point_load_pairs:
                    continue
                # координаты сил (в см)
                load_positions_cm = np.array([smart_convert(xm, 'm', 'cm') for xm, _ in point_load_pairs], dtype=float)
                # нагрузка (кг)
                load_forces_kg = np.array([float(Pkg) for _, Pkg in point_load_pairs], dtype=float)
                # Жесткость соединения траверсы со стойкой в вертикальной плоскости
                kb = smart_convert(row.get(node_support, 0), 'kN', 'kg')
                kb = smart_convert(kb, 'm', 'cm') / (coefficient_n or 1)
                # Коэффициент влияния жесткости стойки на защемление траверсы
                if column_moment_inertia:
                    ke = kb / (1 + (kb * height_cm / (3 * modulus_elasticity * column_moment_inertia)))
                else:
                    ke = 0.0
                # изгибающий момент
                max_bending_moment_cm = 0.0
                if load_forces_kg.size:
                    max_bending_moment_cm, _ = _point_loads(
                        length=length_cm,
                        Iy_cm4=Iy,
                        E_kg_cm2=modulus_elasticity,
                        positions=load_positions_cm,
                        forces=load_forces_kg * gamma_q_omega + (load_factor * G * length)
                    )
                # Прогиб
                _, delta_classic = _point_loads(
                    length=length_cm,
                    Iy_cm4=Iy,
                    E_kg_cm2=modulus_elasticity,
                    positions=load_positions_cm,
                    forces=load_forces_kg * gamma_q_f + (load_factor * G * length * gamma_g)
                )
                denom = (1 + 2 * modulus_elasticity * Iy / (ke * length_cm))
                # факторы жесткости для прогибов и моментов
                delta_factor = beta_delta * (1 - ((0.8 * beta_teta) / (beta_delta * denom)))
                moment_factor = beta_m * (1 - (((2.0 / 3.0) * beta_teta) / (beta_m * denom)))
                # макс прогиб
                delta_max = delta_classic * delta_factor
                # макс момент
                max_bending_moment_cm *= moment_factor

                m_sdy = smart_convert(max_bending_moment_cm, 'cm', 'm')
                m_rdy = Wy * smart_convert(fy, 'cm', 'm')

            # Проверка прочности и прогиба
            durability_str, deflection_str, passed_dur, passed_def = check_beam_section(m_sdy, m_rdy, delta_max,
                                                                                        delta_limit)

            if passed_dur or passed_def:
                results.append(build_result_row(row, section_name, m_sdy, m_rdy, delta_max, G * length, durability_str,
                                                deflection_str, is_flexible_ok))

        except Exception:
            continue

    # Обработка пустого результата
    if not results:
        return pd.DataFrame([{
            "Сечение": "Нет подходящих граничных условий",
            "Момент Msd (кг*м)": "",
            "Расчётная прочность MRdy (кг*м)": "",
            "Прогиб (мм)": "",
            "Вес балки (кг)": "",
            "Проверка прочности": "",
            "Проверка прогиба": "",
            "Проверка гибкости": ""
        }])

    df_result = pd.DataFrame(results)
    df_result.fillna("", inplace=True)
    df_result.sort_values(by="Вес балки (кг)", inplace=True)
    return df_result

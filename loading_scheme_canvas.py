from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QPixmap, QColor, QTransform
from PyQt5.QtCore import Qt, QPointF


class LoadingSchemeCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scheme = "Равномерно распределённая"
        self.support = "Шарнир"
        self.beam_length_m = 1.0
        self.load_kg = 0.0
        self.standart = ""
        self.column_height_m = 1.0
        self.point_loads = []

    def set_point_loads(self, points):
        self.point_loads = list(points or [])
        self.update()

    def set_support(self, support_text):
        self.support = support_text
        self.update()

    def set_beam_length(self, length_m):
        self.beam_length_m = length_m
        self.update()

    def set_beam_load(self, load_kg):
        self.load_kg = load_kg
        self.update()

    def set_scheme(self, scheme_name):
        self.scheme = scheme_name
        self.update()

    def set_standart(self, standart_name):
        self.standart = standart_name
        self.update()

    def set_column_height(self, height_m):
        self.column_height_m = height_m
        self.update()

    def paintEvent(self, event):
        '''
        -Описание: Метод для прорисовки геометрии в зависимости от выбранного итема в baseConBoundaryComboBox
        -Принимает: Событие
        -Возвращает: Ничего
        '''

        def draw_dimension(point_a, point_b, label):
            """
            -Описание: Вложенная функция для отрисовки размеров
            -Принимает: point_a - первая точка, point_b - вторая точка, label - текст (например, L/2)
            -Возвращает: Ничего
            """
            mid = (point_a + point_b) // 2
            y_offset = y_beam - 50  # ← первая строка над балкой
            spacing = 12  # расстояние между строками

            # Вертикальные засечки
            painter.drawLine(point_a, y_beam - 20, point_a, y_offset)
            painter.drawLine(point_b, y_beam - 20, point_b, y_offset)

            # Горизонтальная линия между засечками
            painter.drawLine(point_a, y_offset, point_b, y_offset)

            # Подпись дробной длины (L/2 и т.д.)
            text_width = painter.fontMetrics().width(label)
            painter.drawText(mid - text_width // 2, y_offset - 5, label)

            # Расчёт фактического расстояния в метрах
            beam_px = x_end - x_start
            beam_m = self.beam_length_m
            dist_px = abs(point_b - point_a)
            dist_m = dist_px / beam_px * beam_m

            # Вторая подпись — в метрах (под первой)
            metric_label = f"{dist_m:.2f} м"
            metric_width = painter.fontMetrics().width(metric_label)
            painter.drawText(mid - metric_width // 2, y_offset + spacing, metric_label)

        if self.width() < 10 or self.height() < 10:
            return  # холст еще не отмасштабирован, выходим

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()
        margin = 20

        # Рисуем балку
        y_beam = height // 2
        x_start = margin
        x_end = width - margin
        beam_length = x_end - x_start
        painter.setPen(QPen(Qt.black, 3))
        painter.drawLine(x_start, y_beam, x_end, y_beam)

        # Рисуем опоры
        painter.setBrush(QBrush(Qt.gray))
        if self.standart in ("FEM", "FEM полки"):
            painter.drawEllipse(x_start, y_beam, 20, 20)
            painter.drawEllipse(x_end - 20, y_beam, 20, 20)
        else:
            painter.drawEllipse(x_start - 10, y_beam, 20, 20)
            painter.drawEllipse(x_end - 10, y_beam, 20, 20)

        # Нагрузки
        painter.setPen(QPen(Qt.red, 2))
        painter.setBrush(Qt.red)

        def xm_to_px(x_m):
            if self.beam_length_m <= 0:
                return x_start
            t = max(0.0, min(1.0, x_m / self.beam_length_m))
            return int(round(x_start + t * (x_end - x_start)))

        def draw_arrow(x, force_kg=None):
            arrow_top = y_beam - 60
            arrow_tip = y_beam - 20

            if force_kg is not None:
                text = f"{force_kg:.0f} кг"
                text_width = painter.fontMetrics().width(text)
                painter.setPen(Qt.black)
                painter.drawText(x - text_width // 2, arrow_top - 10, text)

            painter.setPen(QPen(Qt.red, 2))
            painter.drawLine(x, arrow_top, x, arrow_tip)
            triangle = [QPointF(x, arrow_tip),
                        QPointF(x - 6, arrow_tip - 10),
                        QPointF(x + 6, arrow_tip - 10)]
            painter.drawPolygon(*triangle)

        def draw_segment_dim(xa, xb, label_top, value_m):
            y_offset = y_beam - 50
            spacing = 12
            painter.setPen(QPen(Qt.black, 1))

            # вертикальные риски
            painter.drawLine(xa, y_beam - 20, xa, y_offset)
            painter.drawLine(xb, y_beam - 20, xb, y_offset)

            # горизонтальная линия
            painter.drawLine(xa, y_offset, xb, y_offset)

            # подписи
            mid = (xa + xb) // 2
            if label_top:
                w = painter.fontMetrics().width(label_top)
                painter.drawText(mid - w // 2, y_offset - 5, label_top)

            metric_label = f"{value_m:.2f} м"
            mw = painter.fontMetrics().width(metric_label)
            painter.drawText(mid - mw // 2, y_offset + spacing, metric_label)

        if self.scheme.strip().lower() == "свой тип нагружения":
            # Если нет длины или нет валидных точек — просто показываем балку/опоры и общие размеры
            valid_points = [(x, p) for (x, p) in self.point_loads
                            if (self.beam_length_m > 0 and 0.0 <= x <= self.beam_length_m and p > 0)]
            valid_points.sort(key=lambda t: t[0])

            # Стрелки с подписями
            for x_m, p_kg in valid_points:
                x_px = xm_to_px(x_m)
                draw_arrow(x_px, p_kg)

            # Верхние размерные отрезки: 0 → x1 → x2 → ... → L
            ticks_m = [0.0] + [t[0] for t in valid_points] + ([self.beam_length_m] if self.beam_length_m > 0 else [])
            # Рисуем размеры между последовательными «тиками»
            for seg_idx in range(len(ticks_m) - 1):
                xa_px = xm_to_px(ticks_m[seg_idx])
                xb_px = xm_to_px(ticks_m[seg_idx + 1])
                seg_len_m = max(0.0, ticks_m[seg_idx + 1] - ticks_m[seg_idx])
                label_top = f"L{seg_idx + 1}"
                if xb_px - xa_px >= 10:  # чтобы подписи не налезали
                    draw_segment_dim(xa_px, xb_px, label_top, seg_len_m)

        elif self.scheme == "Равномерно распределённая":
            arrow_top = y_beam - 60  # вершина всех стрелок
            painter.setPen(QPen(Qt.red, 2))
            # Горизонтальная линия, соединяющая вершины стрелок
            painter.drawLine(x_start, arrow_top, x_end, arrow_top)

            for i in range(11):
                x = x_start + i * beam_length // 10
                draw_arrow(x)
        elif self.scheme == "Сосредоточенная сила L/2":
            x1 = x_start + beam_length // 2
            draw_arrow(x1, self.load_kg)
            draw_dimension(x_start, x1, "L/2")
            draw_dimension(x1, x_end, "L/2")
        elif self.scheme == "Две сосредоточенные силы L/4-L/2-L/4":
            p = self.load_kg / 2
            x1 = x_start + beam_length // 4
            x2 = x_start + beam_length * 3 // 4
            draw_arrow(x1, p)
            draw_arrow(x2, p)
            draw_dimension(x_start, x1, "L/4")
            draw_dimension(x1, x2, "L/2")
            draw_dimension(x2, x_end, "L/4")
        elif self.scheme == "Две сосредоточенные силы L/3-L/3-L/3":
            p = self.load_kg / 2
            x1 = x_start + beam_length // 3
            x2 = x_start + beam_length * 2 // 3
            draw_arrow(x1, p)
            draw_arrow(x2, p)
            draw_dimension(x_start, x1, "L/3")
            draw_dimension(x1, x2, "L/3")
            draw_dimension(x2, x_end, "L/3")
        elif self.scheme == "Три сосредоточенные силы L/6-L/3-L/3-L/6":
            p = self.load_kg / 3
            x1 = x_start + beam_length // 6
            x2 = x_start + beam_length // 2
            x3 = x_start + beam_length * 5 // 6
            draw_arrow(x1, p)
            draw_arrow(x2, p)
            draw_arrow(x3, p)
            draw_dimension(x_start, x1, "L/6")
            draw_dimension(x1, x2, "L/3")
            draw_dimension(x2, x3, "L/3")
            draw_dimension(x3, x_end, "L/6")
        elif self.scheme == "Три сосредоточенные силы L/4-L/4-L/4-L/4":
            p = self.load_kg / 3
            x1 = x_start + beam_length // 4
            x2 = x_start + beam_length // 2
            x3 = x_start + beam_length * 3 // 4
            draw_arrow(x1, p)
            draw_arrow(x2, p)
            draw_arrow(x3, p)
            draw_dimension(x_start, x1, "L/4")
            draw_dimension(x1, x2, "L/4")
            draw_dimension(x2, x3, "L/4")
            draw_dimension(x3, x_end, "L/4")

        elif self.scheme == "Четыре сосредоточенные силы L/8-L/4-L/4-L/4-L/8":
            p = self.load_kg / 4
            x1 = x_start + beam_length // 8
            x2 = x_start + beam_length * 3 // 8
            x3 = x_start + beam_length * 5 // 8
            x4 = x_start + beam_length * 7 // 8
            draw_arrow(x1, p)
            draw_arrow(x2, p)
            draw_arrow(x3, p)
            draw_arrow(x4, p)
            draw_dimension(x_start, x1, "L/8")
            draw_dimension(x1, x2, "L/4")
            draw_dimension(x2, x3, "L/4")
            draw_dimension(x3, x4, "L/4")
            draw_dimension(x4, x_end, "L/8")

        elif self.scheme == "Четыре сосредоточенные силы L/5-L/5-L/5-L/5-L/5":
            p = self.load_kg / 4
            x1 = x_start + beam_length * 1 // 5
            x2 = x_start + beam_length * 2 // 5
            x3 = x_start + beam_length * 3 // 5
            x4 = x_start + beam_length * 4 // 5
            draw_arrow(x1, p)
            draw_arrow(x2, p)
            draw_arrow(x3, p)
            draw_arrow(x4, p)
            draw_dimension(x_start, x1, "L/5")
            draw_dimension(x1, x2, "L/5")
            draw_dimension(x2, x3, "L/5")
            draw_dimension(x3, x4, "L/5")
            draw_dimension(x4, x_end, "L/5")

        # Дополнительная отрисовка стоек и верхней связи для FEM
        if self.standart in ("FEM", "FEM полки") and self.support != "Шарнир":
            # Геометрия стоек
            h = height // 2.2
            y_top = y_beam
            y_bot = y_beam + int(h)
            x_col1 = x_start
            x_col2 = x_end

            # Вертикальные стойки под концами балки
            pen_setting = QPen(Qt.black, 3)  # толщина 4 пикселя
            painter.setPen(pen_setting)
            painter.drawLine(x_col1, y_top, x_col1, y_bot)
            painter.drawLine(x_col2, y_top, x_col2, y_bot)
            if self.column_height_m > 0:
                text = f"H = {self.column_height_m:.2f} м"
                painter.setPen(Qt.black)
                font_metrics = painter.fontMetrics()
                text_width = font_metrics.width(text)

                # Координаты около правой стойки (x_col2)
                x_text = x_col2 + 10  # сместим немного вправо от стойки
                y_text = (y_top + y_bot) // 2 + font_metrics.height() // 2  # по центру стойки

                # Проверка, влезает ли текст — если не влезает, выравниваем влево
                if x_text + text_width > self.width():
                    x_text = x_col2 - text_width - 10  # разместить слева от стойки

                painter.drawText(x_text, y_text, text)

            # Горизонтальная связь слева от балки
            painter.setPen(QPen(Qt.black, 2))
            # Опоры снизу
            radius_node = 6
            radius_beam = 2
            painter.setBrush(Qt.white)
            painter.drawEllipse(x_col1 - radius_node, y_bot - radius_node, radius_node * 2, radius_node * 2)
            painter.drawEllipse(x_col2 - radius_node, y_bot - radius_node, radius_node * 2, radius_node * 2)

            # Горизонтальная база (линия земли)
            ground_y = y_bot + 6
            painter.setPen(QPen(Qt.black, 1))
            ground_start = x_col1 - 40
            ground_end = x_col2 + 40
            painter.drawLine(ground_start, ground_y, ground_end, ground_y)

            # Штриховка по всей длине "земли"
            hatch_spacing = 8  # расстояние между штрихами
            hatch_length = 10  # длина каждого штриха

            x = ground_start
            while x < ground_end:
                x1 = x
                y1 = ground_y
                x2 = x - hatch_length
                y2 = ground_y + hatch_length
                painter.drawLine(x1, y1, x2, y2)
                x += hatch_spacing

        # Подпись нагрузки q (если задана)
        if self.load_kg > 0 and self.scheme == "Равномерно распределённая":
            painter.setPen(Qt.black)
            painter.drawText(x_end - 60, y_beam - 70, f"q = {self.load_kg:.0f} кг")

        # Размерная линия и подпись длины балки
        if self.beam_length_m > 0:
            # Стрелки на концах
            painter.drawLine(x_start, y_beam + 25, x_start, y_beam + 35)
            painter.drawLine(x_end, y_beam + 25, x_end, y_beam + 35)
            # Линия между стрелками
            painter.drawLine(x_start, y_beam + 30, x_end, y_beam + 30)
            # Подпись посередине
            text = f"L = {self.beam_length_m:.2f} м"
            text_width = painter.fontMetrics().width(text)
            painter.drawText((x_start + x_end) // 2 - text_width // 2, y_beam + 50, text)

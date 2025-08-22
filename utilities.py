import os
import re
import pandas as pd
import sys
from io import BytesIO
from typing import Optional, Callable

PROJECT_ROOT = os.getcwd()

STANDARDS = {
    "Beam loads": {
        "gamma_g": 1,
        "gamma_q_omega": 1,
        "gamma_q_f": 1,
        "reduction_factor_i": 1.03,
        "reduction_factor_w": 1.12,
        "gamma_mb": 0.953191488,
        "load_factor": 0,
        "modulus_elasticity": 196.133,
    },
    "ДБН": {
        "gamma_g": 1.05,
        "gamma_q_omega": 1.4,
        "gamma_q_f": 1,
        "reduction_factor_i": 1,
        "reduction_factor_w": 1,
        "gamma_mb": 0.958,
        "load_factor": 1,
        "modulus_elasticity": 205.939650,
    },
    "FEM": {
        "gamma_g": 1.3,
        "gamma_q_omega": 1.4,
        "gamma_q_f": 1,
        "reduction_factor_i": 1,
        "reduction_factor_w": 1,
        "gamma_mb": 1,
        "load_factor": 1,
        "modulus_elasticity": 210,
    },
    "FEM полки": {
        "gamma_g": 1.3,
        "gamma_q_omega": 1.5,
        "gamma_q_f": 1,
        "reduction_factor_i": 1,
        "reduction_factor_w": 1,
        "gamma_mb": 1,
        "load_factor": 1,
        "modulus_elasticity": 210,
    },
    "1-1-1": {
        "gamma_g": 1,
        "gamma_q_omega": 1,
        "gamma_q_f": 1,
        "reduction_factor_i": 1,
        "reduction_factor_w": 1,
        "gamma_mb": 1,
        "load_factor": 1,
        "modulus_elasticity": 210,
    }
}

LOAD_CONDITIONS = {
    "Равномерно распределённая": {
        "beta_m": 1,
        "beta_teta": 1,
        "beta_delta": 1,
        "n_forces": 1,
    },
    "Сосредоточенная сила L/2": {
        "beta_m": 2,
        "beta_teta": 1.5,
        "beta_delta": 1.6,
        "n_forces": 1,
    },
    "Две сосредоточенные силы L/4-L/2-L/4": {
        "beta_m": 1,
        "beta_teta": 1.12,
        "beta_delta": 1.1,
        "n_forces": 2,
    },
    "Две сосредоточенные силы L/3-L/3-L/3": {
        "beta_m": 1.33,
        "beta_teta": 1.33,
        "beta_delta": 1.36,
        "n_forces": 2,
    },
    "Три сосредоточенные силы L/6-L/3-L/3-L/6": {
        "beta_m": 1.11,
        "beta_teta": 1.06,
        "beta_delta": 1.05,
        "n_forces": 3,
    },
    "Три сосредоточенные силы L/4-L/4-L/4-L/4": {
        "beta_m": 1.33,
        "beta_teta": 1.25,
        "beta_delta": 1.27,
        "n_forces": 3,
    },
    "Четыре сосредоточенные силы L/8-L/4-L/4-L/4-L/8": {
        "beta_m": 1,
        "beta_teta": 1.03,
        "beta_delta": 1.02,
        "n_forces": 4,
    },
    "Четыре сосредоточенные силы L/5-L/5-L/5-L/5-L/5": {
        "beta_m": 1.2,
        "beta_teta": 1.2,
        "beta_delta": 1.21,
        "n_forces": 4,
    },
    "Свой тип нагружения": {
        "beta_m": 1,
        "beta_teta": 1,
        "beta_delta": 1,
        "n_forces": "own",
    }
}

DEFLECTIONS = {
    "L / 200": 200,
    "L / 300": 300
}

COLUMN_TOOLTIPS = {
    "Классификация": "",
    "Производитель": "",
    "Тип сечения": "",
    "Спецификация": "",
    "Серия": "",
    "Высота (mm)": "",
    "Ширина (mm)": "",
    "Толщина стали (mm*10)": "",
    "Изображение": "",
    "Комментарий": "",
    "Aeff": "cм2", "y0": "", "ys": "", "ybr": "", "А": "cм2", "Ageom": "cм2", "Ay": "cм2",
    "Az": "cм2", "Au": "cм2", "Av": "cм2", "yC,0": "cм", "zC,0": "cм", "Iy": "cм4", "Iz": "cм4",
    "Iyz": "cм4", "a": "°", "Iu": "cм4", "Iv": "cм4", "Ip": "cм4", "Ip,M": "cм4", "iy": "cм",
    "iz": "cм", "iyz": "cм", "iu": "cм", "iv": "cм", "ip": "cм", "rp,M": "cм", "i@v,M": "cм",
    "G": "kг/м", "U": "cм", "Uo": "cм", "Ui": "cм", "It": "cм4", "It,St.Ven.": "cм4", "It,Bredt": "cм4",
    "It,s": "cм4", "yM,0": "cм", "zM,0": "cм", "yM": "cм", "zM": "cм", "I@v,C": "cм6", "I@v,M": "cм6",
    "r@v,M": "", "Wu,макс.": "cм3", "Wu,мин.": "cм3", "Wv,макс.": "cм3", "Wv,мин.": "cм3", "Wy,макс.": "cм3",
    "Wy,мин.": "cм3", "Wz,макс.": "cм3", "Wz,мин.": "cм3", "W@v,M,макс.": "cм4", "W@v,M,мин.": "cм4", "Wt": "cм3",
    "ru": "cм", "rM,v": "cм", "lM": "1/cм", "Mpl,y,d": "kНм", "Mpl,z,d": "kНм", "Mpl,u,d": "kНм", "Mpl,v,d": "kНм",
    "Wpl,y": "cм3", "Wpl,z": "cм3", "Wpl,u": "cм3", "Wpl,v": "cм3", "Apl,y": "cм2", "Apl,z": "cм2", "Apl,u": "cм2",
    "Apl,v": "cм2", "fy,0": "cм", "fz,0": "cм", "fu": "cм", "fv": "cм", "Vpl,y,d": "kН", "Vpl,z,d": "kН",
    "Vpl,u,d": "kН", "Vpl,v,d": "kН", "Npl,d": "kН", "КПУy/u": "", "КПУz/v": "",
}


def auto_fill_from_filename(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    """
    Метод автоматически заполняет некоторые ячейки в DataFrame на основе имени Excel-файла или изображения при импорте
    """
    # Словарь соответствий серии (Производитель, Тип сечения)
    series_meta_map = {
        "ТВ": {"Классификация": "Балка", "Производитель": "Иприс-профиль", "Тип сечения": "Траверса"},
        "СИ": {"Классификация": "Колонна", "Производитель": "Иприс-профиль", "Тип сечения": "Стойка"},
        "Z": {"Классификация": "Балка", "Производитель": "Иприс-профиль", "Тип сечения": "Траверса"},
        "СИБП": {"Классификация": "Колонна", "Производитель": "Иприс-профиль", "Тип сечения": "Стойка"},
        "ТВУ": {"Классификация": "Балка", "Производитель": "Иприс-профиль", "Тип сечения": "Траверса"},
        # "ХХ": {"Производитель": "B", "Тип сечения": "Колонна"},
    }
    # Словарь для определения, какие колонки нужно заполнить для каждой серии
    series_column_map = {
        "ТВ": ["Высота (mm)", "Ширина (mm)", "Толщина стали (mm*10)"],
        "ТВУ": ["Высота (mm)", "Ширина (mm)", "Толщина стали (mm*10)"],
        "СИ": ["Высота (mm)", "Ширина (mm)", "Толщина стали (mm*10)"],
        "Z": ["Высота (mm)", "Ширина (mm)", "Толщина стали (mm*10)"],
        "СИБП": ["Высота (mm)", "Ширина (mm)", "Толщина стали (mm*10)"],
    }

    basename = os.path.splitext(os.path.basename(filename))[0]  # Получаем имя файла без пути и расширения
    # Извлекаем префикс серии (например, ТВ) — он определяет тип сечения
    parts = basename.split('.')
    series_key = parts[0] if len(parts) >= 4 else None

    # Проверяем, есть ли такая серия
    if series_key not in series_column_map:
        return df

    target_columns = series_column_map[series_key]
    # Заполнение геометрических данных
    for i, col in enumerate(target_columns):
        if i + 1 < len(parts):
            value = parts[i + 1]
            if col in df.columns:
                df[col] = df[col].replace(r'^\s*$', pd.NA, regex=True)  # Заменяем все пустые строки на NA
                df[col] = df[col].fillna(value)  # Заполняем пустые значения в этой колонке value из имени файла
    # Заполнение излбражений
    if "Изображение" in df.columns:
        image_path = os.path.join("..", "resources", f"{basename}.PNG")
        df["Изображение"] = df["Изображение"].replace(r'^\s*$', pd.NA, regex=True)
        df["Изображение"] = df["Изображение"].fillna(image_path)
    # Заполнение производителя и типа сечения
    if series_key in series_meta_map:
        for col_name, fill_value in series_meta_map[series_key].items():
            if col_name in df.columns:
                df[col_name] = df[col_name].replace(r'^\s*$', pd.NA, regex=True)
                df[col_name] = df[col_name].fillna(fill_value)

    return df


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Метод выполняет заполнение пустых (Nan) ячеек нулями и плейсхолдером для ячейки изображений
    """
    if "Изображение" in df.columns:
        df["Изображение"] = df["Изображение"].replace(r'^\s*$', pd.NA, regex=True)
        df["Изображение"] = df["Изображение"].fillna("resources/placeholder.png")

    df = df.replace(r'^\s*$', pd.NA, regex=True).infer_objects(copy=False)
    df = df.fillna(0).infer_objects(copy=False)
    return df


def cast_value(value, expected_type):
    """
    Метод — универсальный преобразователь типов данных
    """
    try:
        # Приводим к строке и убираем лишние пробелы
        value = str(value).strip()

        # Универсальная замена запятой на точку для чисел с плавающей точкой
        if pd.api.types.is_float_dtype(expected_type):
            return float(value.replace(',', '.'))

        if pd.api.types.is_integer_dtype(expected_type):
            # Для целых чисел сначала отрезаем дробную часть, если была введена через запятую или точку
            return int(float(value.replace(',', '.')))

        if pd.api.types.is_bool_dtype(expected_type):
            return value.lower() in ['1', 'true', 'yes', 'да']

        return value  # Строка или object

    except Exception:
        return None


# ======================================================================
# Кэш пароля на время работы процесса (чтобы не спрашивать каждый раз)
_CACHED_PASSWORD: Optional[str] = None


def resource_path(*parts: str) -> str:
    """
    Поддержка PyInstaller onefile: берём путь из _MEIPASS, иначе — PROJECT_ROOT.
    """
    base = getattr(sys, "_MEIPASS", PROJECT_ROOT)
    return os.path.join(base, *parts)


def data_path(*parts: str) -> str:
    """
    Ищем файл сначала среди запакованных ресурсов (data/), затем рядом с проектом.
    """
    p_bundle = resource_path("data", *parts)
    if os.path.exists(p_bundle):
        return p_bundle
    return os.path.join(PROJECT_ROOT, "data", *parts)


def _get_decrypter():
    """
    Ленивая загрузка decrypt_excel_bytesio из encrypter.py (лежит рядом с приложением).
    """
    try:
        from encrypter import decrypt_excel_bytesio
    except Exception as e:
        raise ImportError(
            "Не найден encrypter.py или пакет недоступен. "
            "Положите файл рядом с .exe / entrypoint-скриптом или добавьте в PYTHONPATH."
        ) from e
    return decrypt_excel_bytesio


def open_sections_excel_bytes(
        password: Optional[str] = None,
        ask_password_callback: Optional[Callable[[], Optional[str]]] = None,
        xlsx_name: str = "sections_base.xlsx",
        enc_name: str = "sections_base.xlsx.enc",
) -> BytesIO:
    """
    Возвращает BytesIO с байтами исходного Excel (даже если он был зашифрован).
    Порядок:
      1) Если существует data/sections_base.xlsx — читаем и отдаём BytesIO.
      2) Иначе, если существует data/sections_base.xlsx.enc — спрашиваем/используем пароль, расшифровываем в памяти.
      3) Иначе — FileNotFoundError.
    """
    xlsx_path = data_path(xlsx_name)
    enc_path = data_path(enc_name)

    # 1) Нефинкционированный Excel найден
    if os.path.exists(xlsx_path):
        with open(xlsx_path, "rb") as f:
            return BytesIO(f.read())

    # 2) Есть только зашифрованный
    if os.path.exists(enc_path):
        decrypt_excel_bytesio = _get_decrypter()

        global _CACHED_PASSWORD
        pwd = password or _CACHED_PASSWORD
        if not pwd and callable(ask_password_callback):
            pwd = ask_password_callback()
        if not pwd:
            raise RuntimeError("Пароль не задан и не получен у пользователя.")

        with open(enc_path, "rb") as f:
            blob = f.read()

        # Первая попытка
        try:
            dec_io = decrypt_excel_bytesio(pwd, BytesIO(blob))
            _CACHED_PASSWORD = pwd
            return dec_io
        except Exception:
            # Разрешаем одну повторную попытку с повторным вводом
            if callable(ask_password_callback):
                retry = ask_password_callback()
                if retry:
                    dec_io = decrypt_excel_bytesio(retry, BytesIO(blob))  # пробуем второй пароль
                    _CACHED_PASSWORD = retry
                    return dec_io
            raise  # если нечем помочь — пробрасываем ошибку наверх

    # 3) Не нашли ни .xlsx, ни .enc
    raise FileNotFoundError(
        f"Не найден файл базы данных:\n- {xlsx_path}\n- {enc_path}"
    )


def read_sections_excel(
        sheet: str = "Сечения",
        password: Optional[str] = None,
        ask_password_callback: Optional[Callable[[], Optional[str]]] = None,
        **pd_kwargs,
) -> pd.DataFrame:
    """
    Удобная обёртка: открывает (xlsx|enc) и сразу читает нужный лист в DataFrame.
    """
    bio = open_sections_excel_bytes(password, ask_password_callback)
    return pd.read_excel(bio, sheet_name=sheet, **pd_kwargs)



# ===== Remote API support (non-breaking) ======================================
import json
import time
from typing import Dict, Any
import requests

# Включить удалённый режим можно флагом env или константой:
USE_REMOTE = os.getenv("SECTIONS_USE_REMOTE", "1") == "1"

# Базовый URL API: переопределяйте через переменную окружения
SECTIONS_API_BASE = os.getenv("SECTIONS_API_BASE", "https://example.com/api")

# Кэш короткоживущего токена в процессе
_CACHED_API_TOKEN: Optional[str] = None


def _default_backoff(retry: int) -> None:
    time.sleep(min(0.5 * (2 ** retry), 5.0))


def fetch_sections_df_remote(
    sheet: str = "Сечения",
    api_token: Optional[str] = None,
    ask_token_callback: Optional[Callable[[], Optional[str]]] = None,
    timeout: float = 10.0,
    query: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Тянет данные с удалённого API и возвращает DataFrame.
    Ожидается, что сервер вернёт JSON-массив записей (records) либо application/parquet.
    Безопасно падает в исключение, которое можно перехватить с фолбэком на локальный путь.
    """
    global _CACHED_API_TOKEN
    token = api_token or _CACHED_API_TOKEN
    if not token and callable(ask_token_callback):
        token = ask_token_callback()
    if not token:
        raise RuntimeError("Не задан токен API для удалённой базы.")

    url = f"{SECTIONS_API_BASE}/sections"
    params = {"sheet": sheet}
    if query:
        params.update(query)

    headers = {"Authorization": f"Bearer {token}"}

    # Попробуем сперва Parquet (если сервер так умеет), затем JSON
    for attempt in range(3):
        try:
            # 1) Parquet
            r = requests.get(url, headers=headers, params={**params, "format": "parquet"}, timeout=timeout)
            if r.status_code == 200 and r.headers.get("Content-Type", "").startswith("application/octet-stream"):
                bio = BytesIO(r.content)
                df = pd.read_parquet(bio)
                _CACHED_API_TOKEN = token
                return df

            # 2) JSON (records)
            r = requests.get(url, headers=headers, params={**params, "format": "json"}, timeout=timeout)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, dict) and "records" in data:
                    data = data["records"]
                df = pd.DataFrame(data)
                _CACHED_API_TOKEN = token
                return df

            # Неподходящий ответ — кидаем
            raise RuntimeError(f"API error {r.status_code}: {r.text[:200]}")

        except Exception as e:
            if attempt < 2:
                _default_backoff(attempt)
                continue
            raise

def read_sections_remote_or_local(
    sheet: str = "Сечения",
    ask_token_callback: Optional[Callable[[], Optional[str]]] = None,
    ask_password_callback: Optional[Callable[[], Optional[str]]] = None,
    **pd_kwargs,
) -> pd.DataFrame:
    """
    Унифицированная точка входа: если USE_REMOTE == True — тянем с API,
    иначе — старый локальный путь. При сетевых сбоях автоматически
    фолбэчим на локальный Excel/enc.
    """
    if USE_REMOTE:
        try:
            df = fetch_sections_df_remote(sheet=sheet, ask_token_callback=ask_token_callback)
            # Совместимость с локальной нормализацией
            df = normalize_dataframe(df)
            return df
        except Exception:
            # Фолбэк на локальную базу (xlsx/enc) — старая реализация
            pass

    # Старый локальный путь (как и раньше)
    return read_sections_excel(sheet=sheet, ask_password_callback=ask_password_callback, **pd_kwargs)

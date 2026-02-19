from aiogram.fsm.state import State, StatesGroup

class FieldForm(StatesGroup):
    language    = State()  # выбор языка
    name        = State()  # название поля
    location    = State()  # геолокация или координаты
    area        = State()  # площадь
    soil_type   = State()  # тип почвы
    soil_ph     = State()  # pH
    soil_organic= State()  # органика %
    soil_clay   = State()  # глина %
    soil_sand   = State()  # песок %
    soil_notes  = State()  # заметки
    analyzing   = State()  # идёт анализ

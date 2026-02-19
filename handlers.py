import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command

from states import FieldForm
from texts import t, TEXTS
from keyboards import (
    lang_keyboard, soil_type_keyboard, skip_keyboard,
    location_keyboard, remove_keyboard, result_keyboard
)
from agro import analyze_field, area_to_ha, parse_area

router = Router()
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# /start
# ──────────────────────────────────────────────
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FieldForm.language)
    await message.answer(
        TEXTS["ru"]["welcome"],
        parse_mode="Markdown",
        reply_markup=lang_keyboard()
    )

@router.message(Command("newfield"))
async def cmd_newfield(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.clear()
    await state.update_data(lang=lang)
    await state.set_state(FieldForm.name)
    await message.answer(t(lang, "ask_name"), parse_mode="Markdown")

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    help_text = (
        "🌱 *AgroBot — Помощник агронома*\n\n"
        "/start — начать заново\n"
        "/newfield — добавить новое поле\n"
        "/help — эта справка\n\n"
        "Бот задаёт вопросы о вашем поле и генерирует план посева на основе ИИ."
    ) if lang == "ru" else (
        "🌱 *AgroBot — Agronomist Assistant*\n\n"
        "/start — restart\n"
        "/newfield — add new field\n"
        "/help — this help\n\n"
        "The bot asks questions about your field and generates an AI-powered planting plan."
    )
    await message.answer(help_text, parse_mode="Markdown")

# ──────────────────────────────────────────────
# Выбор языка
# ──────────────────────────────────────────────
@router.callback_query(FieldForm.language, F.data.in_({"lang_ru", "lang_en"}))
async def cb_language(callback: CallbackQuery, state: FSMContext):
    lang = "ru" if callback.data == "lang_ru" else "en"
    await state.update_data(lang=lang)
    await state.set_state(FieldForm.name)
    await callback.message.edit_text(t(lang, "lang_set"), parse_mode="Markdown")
    await callback.answer()

# ──────────────────────────────────────────────
# Название поля
# ──────────────────────────────────────────────
@router.message(FieldForm.name)
async def step_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(name=message.text.strip())
    await state.set_state(FieldForm.location)
    await message.answer(
        t(lang, "ask_location"),
        parse_mode="Markdown",
        reply_markup=location_keyboard(lang)
    )

# ──────────────────────────────────────────────
# Геолокация (кнопка)
# ──────────────────────────────────────────────
@router.message(FieldForm.location, F.content_type == ContentType.LOCATION)
async def step_location_geo(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    lat = message.location.latitude
    lon = message.location.longitude
    await state.update_data(latitude=lat, longitude=lon)
    await state.set_state(FieldForm.area)
    await message.answer(
        f"✅ {lat:.4f}, {lon:.4f}\n\n" + t(lang, "ask_area"),
        parse_mode="Markdown",
        reply_markup=remove_keyboard()
    )

# ──────────────────────────────────────────────
# Координаты текстом
# ──────────────────────────────────────────────
@router.message(FieldForm.location)
async def step_location_text(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    try:
        parts = message.text.replace(" ", "").split(",")
        lat, lon = float(parts[0]), float(parts[1])
        await state.update_data(latitude=lat, longitude=lon)
        await state.set_state(FieldForm.area)
        await message.answer(
            f"✅ {lat:.4f}, {lon:.4f}\n\n" + t(lang, "ask_area"),
            parse_mode="Markdown",
            reply_markup=remove_keyboard()
        )
    except Exception:
        await message.answer(t(lang, "invalid_coords"), parse_mode="Markdown")

# ──────────────────────────────────────────────
# Площадь
# ──────────────────────────────────────────────
@router.message(FieldForm.area)
async def step_area(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    try:
        value, unit = parse_area(message.text)
        area_ha = area_to_ha(value, unit)
        await state.update_data(area_ha=area_ha)
        await state.set_state(FieldForm.soil_type)
        await message.answer(
            f"✅ {area_ha:.2f} га\n\n" + t(lang, "ask_soil_type"),
            parse_mode="Markdown",
            reply_markup=soil_type_keyboard(lang)
        )
    except Exception:
        await message.answer(t(lang, "invalid_area"), parse_mode="Markdown")

# ──────────────────────────────────────────────
# Тип почвы (inline кнопки)
# ──────────────────────────────────────────────
@router.callback_query(FieldForm.soil_type, F.data.startswith("soil_"))
async def cb_soil_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    soil = callback.data.replace("soil_", "")
    soil_label = TEXTS[lang]["soil_types"].get(soil, soil)
    await state.update_data(soil_type=soil)
    await state.set_state(FieldForm.soil_ph)
    await callback.message.edit_text(
        f"✅ {soil_label}\n\n" + t(lang, "ask_ph"),
        parse_mode="Markdown",
        reply_markup=skip_keyboard(lang)
    )
    await callback.answer()

# ──────────────────────────────────────────────
# pH почвы
# ──────────────────────────────────────────────
@router.callback_query(FieldForm.soil_ph, F.data == "skip")
async def cb_skip_ph(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(soil_ph=None)
    await state.set_state(FieldForm.soil_organic)
    await callback.message.edit_text(
        t(lang, "ask_organic"), parse_mode="Markdown",
        reply_markup=skip_keyboard(lang)
    )
    await callback.answer()

@router.message(FieldForm.soil_ph)
async def step_ph(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    try:
        ph = float(message.text.replace(",", "."))
        await state.update_data(soil_ph=ph)
        await state.set_state(FieldForm.soil_organic)
        await message.answer(
            f"✅ pH: {ph}\n\n" + t(lang, "ask_organic"),
            parse_mode="Markdown",
            reply_markup=skip_keyboard(lang)
        )
    except ValueError:
        await message.answer(t(lang, "invalid_number"), parse_mode="Markdown")

# ──────────────────────────────────────────────
# Органика
# ──────────────────────────────────────────────
@router.callback_query(FieldForm.soil_organic, F.data == "skip")
async def cb_skip_organic(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(soil_organic=None)
    await state.set_state(FieldForm.soil_clay)
    await callback.message.edit_text(
        t(lang, "ask_clay"), parse_mode="Markdown",
        reply_markup=skip_keyboard(lang)
    )
    await callback.answer()

@router.message(FieldForm.soil_organic)
async def step_organic(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    try:
        val = float(message.text.replace(",", "."))
        await state.update_data(soil_organic=val)
        await state.set_state(FieldForm.soil_clay)
        await message.answer(
            f"✅ Органика: {val}%\n\n" + t(lang, "ask_clay"),
            parse_mode="Markdown",
            reply_markup=skip_keyboard(lang)
        )
    except ValueError:
        await message.answer(t(lang, "invalid_number"), parse_mode="Markdown")

# ──────────────────────────────────────────────
# Глина
# ──────────────────────────────────────────────
@router.callback_query(FieldForm.soil_clay, F.data == "skip")
async def cb_skip_clay(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(soil_clay=None)
    await state.set_state(FieldForm.soil_sand)
    await callback.message.edit_text(
        t(lang, "ask_sand"), parse_mode="Markdown",
        reply_markup=skip_keyboard(lang)
    )
    await callback.answer()

@router.message(FieldForm.soil_clay)
async def step_clay(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    try:
        val = float(message.text.replace(",", "."))
        await state.update_data(soil_clay=val)
        await state.set_state(FieldForm.soil_sand)
        await message.answer(
            f"✅ Глина: {val}%\n\n" + t(lang, "ask_sand"),
            parse_mode="Markdown",
            reply_markup=skip_keyboard(lang)
        )
    except ValueError:
        await message.answer(t(lang, "invalid_number"), parse_mode="Markdown")

# ──────────────────────────────────────────────
# Песок
# ──────────────────────────────────────────────
@router.callback_query(FieldForm.soil_sand, F.data == "skip")
async def cb_skip_sand(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.update_data(soil_sand=None)
    await state.set_state(FieldForm.soil_notes)
    await callback.message.edit_text(
        t(lang, "ask_notes"), parse_mode="Markdown",
        reply_markup=skip_keyboard(lang)
    )
    await callback.answer()

@router.message(FieldForm.soil_sand)
async def step_sand(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    try:
        val = float(message.text.replace(",", "."))
        await state.update_data(soil_sand=val)
        await state.set_state(FieldForm.soil_notes)
        await message.answer(
            f"✅ Песок: {val}%\n\n" + t(lang, "ask_notes"),
            parse_mode="Markdown",
            reply_markup=skip_keyboard(lang)
        )
    except ValueError:
        await message.answer(t(lang, "invalid_number"), parse_mode="Markdown")

# ──────────────────────────────────────────────
# Заметки → запуск анализа
# ──────────────────────────────────────────────
@router.callback_query(FieldForm.soil_notes, F.data == "skip")
async def cb_skip_notes(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(soil_notes="")
    await run_analysis(callback.message, state, bot, edit=True)
    await callback.answer()

@router.message(FieldForm.soil_notes)
async def step_notes(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(soil_notes=message.text.strip())
    await run_analysis(message, state, bot, edit=False)

# ──────────────────────────────────────────────
# Анализ и результат
# ──────────────────────────────────────────────
async def run_analysis(message: Message, state: FSMContext, bot: Bot, edit: bool = False):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    # Сообщение "анализирую..."
    if edit:
        analyzing_msg = await message.edit_text(
            t(lang, "analyzing"), parse_mode="Markdown"
        )
    else:
        analyzing_msg = await message.answer(
            t(lang, "analyzing"), parse_mode="Markdown"
        )

    await state.set_state(FieldForm.analyzing)

    try:
        # Запускаем анализ в отдельном потоке чтобы не блокировать event loop
        loop = asyncio.get_event_loop()
        plan = await loop.run_in_executor(None, analyze_field, data, lang)

        result = format_result(plan, data, lang)

        await analyzing_msg.edit_text(
            result,
            parse_mode="Markdown",
            reply_markup=result_keyboard(lang)
        )

    except Exception as e:
        log.error(f"Analysis error: {e}")
        await analyzing_msg.edit_text(
            t(lang, "error"), parse_mode="Markdown"
        )

    await state.clear()
    await state.update_data(lang=lang)

def format_result(plan: dict, data: dict, lang: str) -> str:
    name = data.get("name", "Field")
    lines = [f"🌱 *ПЛАН ПОСЕВА — {name}*\n" if lang == "ru" else f"🌱 *PLANTING PLAN — {name}*\n"]
    lines.append("─" * 28 + "\n")

    # Рекомендации
    lines.append(t(lang, "recommendations_title"))
    for i, rec in enumerate(plan.get("recommendations", []), 1):
        lines.append(f"{i}. {rec}\n")

    # Сроки посева
    windows = plan.get("planting_windows", {})
    if windows:
        lines.append(t(lang, "windows_title"))
        for crop, months in windows.items():
            lines.append(f"🗓 *{crop}*: {months}\n")

    # Советы
    tips = plan.get("tips", {})
    if tips:
        lines.append(t(lang, "tips_title"))
        for crop, tip in tips.items():
            lines.append(f"💡 *{crop}*: {tip}\n")

    # Риски
    risks = plan.get("risks", [])
    if risks:
        lines.append(t(lang, "risks_title"))
        for risk in risks:
            lines.append(f"⚠️ {risk}\n")

    return "".join(lines)

# ──────────────────────────────────────────────
# Кнопка "Новое поле"
# ──────────────────────────────────────────────
@router.callback_query(F.data == "new_field")
async def cb_new_field(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")
    await state.clear()
    await state.update_data(lang=lang)
    await state.set_state(FieldForm.name)
    await callback.message.answer(t(lang, "ask_name"), parse_mode="Markdown")
    await callback.answer()

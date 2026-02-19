TEXTS = {
    "ru": {
        "welcome": (
            "🌱 *Добро пожаловать в AgroBot!*\n\n"
            "Я помогу составить план посева для вашего поля.\n"
            "Просто отвечайте на мои вопросы — всё остальное я сделаю сам.\n\n"
            "Выберите язык / Choose language:"
        ),
        "lang_set": "✅ Язык установлен: Русский\n\nНачнём! Введите *название вашего поля*:",
        "ask_name": "📋 Введите *название поля* (например: «Северный участок»):",
        "ask_location": (
            "📍 Отправьте *геолокацию* поля (кнопка ниже)\n"
            "или введите координаты вручную:\n"
            "`широта, долгота` — например: `40.8046, 44.4939`"
        ),
        "ask_area": (
            "📐 Введите *площадь поля*:\n"
            "Поддерживаемые единицы: `ha`, `m2`, `ac`\n"
            "Например: `0.5 ha` или `5000 m2`"
        ),
        "ask_soil_type": "🌍 Выберите *тип почвы*:",
        "ask_ph": (
            "🧪 Введите *pH почвы* (обычно 4.0–9.0)\n"
            "или нажмите «Пропустить»"
        ),
        "ask_organic": (
            "🌿 Введите *содержание органики* в % (обычно 1–5%)\n"
            "или нажмите «Пропустить»"
        ),
        "ask_clay": (
            "🪨 Введите *содержание глины* в % (0–100)\n"
            "или нажмите «Пропустить»"
        ),
        "ask_sand": (
            "🏖 Введите *содержание песка* в % (0–100)\n"
            "или нажмите «Пропустить»"
        ),
        "ask_notes": (
            "📝 Добавьте *заметки о поле* (необязательно)\n"
            "Например: «Поливная зона, склон на юг»\n"
            "или нажмите «Пропустить»"
        ),
        "analyzing": "⏳ *Анализирую ваше поле...*\n\nЭто займёт 10–20 секунд. Пожалуйста, подождите 🌾",
        "result_header": "🌱 *ПЛАН ПОСЕВА — {name}*\n{'─'*30}\n",
        "recommendations_title": "✅ *Рекомендуемые культуры:*\n",
        "windows_title": "\n📅 *Сроки посева:*\n",
        "tips_title": "\n💡 *Советы по уходу:*\n",
        "risks_title": "\n⚠️ *Риски:*\n",
        "error": "❌ Произошла ошибка при анализе. Попробуйте ещё раз: /newfield",
        "invalid_coords": "❌ Неверный формат координат. Попробуйте: `40.8046, 44.4939`",
        "invalid_area": "❌ Неверный формат площади. Попробуйте: `0.5 ha` или `5000 m2`",
        "invalid_number": "❌ Введите число. Например: `6.5`",
        "skip": "Пропустить",
        "send_location": "📍 Отправить геолокацию",
        "new_field": "🌱 Новое поле",
        "done": "✅ Готово",
        "field_summary": (
            "📋 *Сводка по полю:*\n"
            "• Название: {name}\n"
            "• Координаты: {lat}, {lon}\n"
            "• Площадь: {area_ha:.2f} га\n"
            "• Тип почвы: {soil_type}\n"
            "• pH: {ph}\n"
            "• Органика: {organic}\n"
        ),
        "soil_types": {
            "loamy": "🟫 Суглинистая",
            "sandy": "🟡 Песчаная",
            "clay": "🔴 Глинистая",
            "silty": "⚫ Илистая",
            "peaty": "🟤 Торфяная",
            "chalky": "⚪ Меловая",
        },
    },
    "en": {
        "welcome": (
            "🌱 *Welcome to AgroBot!*\n\n"
            "I'll help you create a crop planting plan for your field.\n"
            "Just answer my questions — I'll do the rest.\n\n"
            "Выберите язык / Choose language:"
        ),
        "lang_set": "✅ Language set: English\n\nLet's start! Enter your *field name*:",
        "ask_name": "📋 Enter your *field name* (e.g. «North plot»):",
        "ask_location": (
            "📍 Send your field *location* (button below)\n"
            "or enter coordinates manually:\n"
            "`latitude, longitude` — e.g.: `40.8046, 44.4939`"
        ),
        "ask_area": (
            "📐 Enter the *field area*:\n"
            "Supported units: `ha`, `m2`, `ac`\n"
            "Example: `0.5 ha` or `5000 m2`"
        ),
        "ask_soil_type": "🌍 Select *soil type*:",
        "ask_ph": (
            "🧪 Enter *soil pH* (usually 4.0–9.0)\n"
            "or press «Skip»"
        ),
        "ask_organic": (
            "🌿 Enter *organic matter* content in % (usually 1–5%)\n"
            "or press «Skip»"
        ),
        "ask_clay": (
            "🪨 Enter *clay content* in % (0–100)\n"
            "or press «Skip»"
        ),
        "ask_sand": (
            "🏖 Enter *sand content* in % (0–100)\n"
            "or press «Skip»"
        ),
        "ask_notes": (
            "📝 Add *field notes* (optional)\n"
            "E.g.: «Irrigated zone, south-facing slope»\n"
            "or press «Skip»"
        ),
        "analyzing": "⏳ *Analyzing your field...*\n\nThis will take 10–20 seconds. Please wait 🌾",
        "result_header": "🌱 *PLANTING PLAN — {name}*\n{'─'*30}\n",
        "recommendations_title": "✅ *Recommended crops:*\n",
        "windows_title": "\n📅 *Planting windows:*\n",
        "tips_title": "\n💡 *Management tips:*\n",
        "risks_title": "\n⚠️ *Risks:*\n",
        "error": "❌ Analysis error. Please try again: /newfield",
        "invalid_coords": "❌ Invalid coordinates format. Try: `40.8046, 44.4939`",
        "invalid_area": "❌ Invalid area format. Try: `0.5 ha` or `5000 m2`",
        "invalid_number": "❌ Please enter a number. Example: `6.5`",
        "skip": "Skip",
        "send_location": "📍 Send location",
        "new_field": "🌱 New field",
        "done": "✅ Done",
        "field_summary": (
            "📋 *Field summary:*\n"
            "• Name: {name}\n"
            "• Coordinates: {lat}, {lon}\n"
            "• Area: {area_ha:.2f} ha\n"
            "• Soil type: {soil_type}\n"
            "• pH: {ph}\n"
            "• Organic: {organic}\n"
        ),
        "soil_types": {
            "loamy": "🟫 Loamy",
            "sandy": "🟡 Sandy",
            "clay": "🔴 Clay",
            "silty": "⚫ Silty",
            "peaty": "🟤 Peaty",
            "chalky": "⚪ Chalky",
        },
    },
}

def t(lang: str, key: str) -> str:
    return TEXTS.get(lang, TEXTS["ru"]).get(key, key)

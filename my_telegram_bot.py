import os
from aiohttp import web
import random
from datetime import datetime
import asyncio
from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_data = {}
awaiting_reply = {}

# === Словарь переводов ===
TEXTS = {
    "choose_lang": {
        "en": "Please select language / Будь ласка, оберіть мову / Proszę wybrać język / Пожалуйста, выберите язык",
        "ua": "Будь ласка, оберіть мову / Please select language / Proszę wybrać język / Пожалуйста, выберите язык",
        "pl": "Proszę wybrać język / Please select language / Будь ласка, оберіть мову / Пожалуйста, выберите язык",
        "ru": "Пожалуйста, выберите язык / Please select language / Будь ласка, оберіть мову / Proszę wybrać język"
    },
    "captcha_question": {
        "en": "🤖 To prove you're human, answer the question:\nWhat is {a} + {b}?",
        "ua": "🤖 Щоб довести, що ви людина, дайте відповідь на запитання:\nСкільки буде {a} + {b}?",
        "pl": "🤖 Aby udowodnić, że jesteś człowiekiem, odpowiedz na pytanie:\nIle to będzie {a} + {b}?",
        "ru": "🤖 Чтобы доказать, что вы человек, ответьте на вопрос:\nСколько будет {a} + {b}?"
    },
    "captcha_wrong": {
        "en": "❌ Wrong answer. Please try again.\nWhat is {a} + {b}?",
        "ua": "❌ Невірно. Спробуйте ще раз.\nСкільки буде {a} + {b}?",
        "pl": "❌ Błędna odpowiedź. Spróbuj ponownie.\nIle to będzie {a} + {b}?",
        "ru": "❌ Неверно. Попробуйте снова.\nСколько будет {a} + {b}?"
    },
    "captcha_enter_number": {
        "en": "Please enter a number.",
        "ua": "Будь ласка, введіть число.",
        "pl": "Proszę wprowadzić liczbę.",
        "ru": "Пожалуйста, введите число."
    },
    "hello_human": {
        "en": "✅ Great, you're human!\nWhat's your name?",
        "ua": "✅ Чудово, ви людина!\nЯк вас звати?",
        "pl": "✅ Świetnie, jesteś człowiekiem!\nJak masz na imię?",
        "ru": "✅ Отлично, вы человек!\nКак вас зовут?"
    },
    "ask_reason": {
        "en": "Great 👌\nNow please write why you want to contact us (e.g. 'Discuss project').",
        "ua": "Чудово 👌\nТепер напишіть, навіщо ви хочете зв’язатися (наприклад: 'Обговорити проєкт').",
        "pl": "Świetnie 👌\nTeraz napisz, dlaczego chcesz się skontaktować (na przykład: 'Omówić projekt').",
        "ru": "Отлично 👌\nТеперь напишите, зачем вы хотите связаться (например: 'Обсудить проект')."
    },
    "ask_message": {
        "en": "Got it 👍\nNow please write the message I will forward to the developer:",
        "ua": "Зрозуміло 👍\nТепер напишіть повідомлення, яке я передам розробнику:",
        "pl": "Zrozumiałem 👍\nTeraz napisz wiadomość, którą przekażę deweloperowi:",
        "ru": "Понял 👍\nТеперь напишите сообщение, которое я передам разработчику:"
    },
    "confirm_message": {
        "en": "Here's what I got:\n👤 Name: {name}\n💬 Reason: {reason}\n📝 Message: {message}\n\nPress the button to send it to the developer:",
        "ua": "Ось що я запам’ятав:\n👤 Ім’я: {name}\n💬 Тема: {reason}\n📝 Повідомлення: {message}\n\nНатисніть кнопку, щоб відправити розробнику:",
        "pl": "Oto co zapamiętałem:\n👤 Imię: {name}\n💬 Temat: {reason}\n📝 Wiadomość: {message}\n\nNaciśnij przycisk, aby wysłać do dewelopera:",
        "ru": "Вот что я запомнил:\n👤 Имя: {name}\n💬 Тема: {reason}\n📝 Сообщение: {message}\n\nНажмите кнопку, чтобы отправить разработчику:"
    },
    "send_to_admin": {
        "en": "📨 Send to developer",
        "ua": "📨 Надіслати розробнику",
        "pl": "📨 Wyślij do dewelopera",
        "ru": "📨 Отправить разработчику"
    },
    "restart_form": {
        "en": "🔁 Start over",
        "ua": "🔁 Почати знову",
        "pl": "🔁 Wypełnij ponownie",
        "ru": "🔁 Заполнить заново"
    },
    "msg_sent_admin": {
        "en": "✅ Message sent to developer! They will contact you soon 👌",
        "ua": "✅ Повідомлення надіслано розробнику! Він зв’яжеться з вами пізніше 👌",
        "pl": "✅ Wiadomość wysłana do dewelopera! Skontaktuje się z tobą później 👌",
        "ru": "✅ Сообщение отправлено разработчику! Он свяжется с вами позже 👌"
    },
    "msg_ask_reply": {
        "en": "✍️ Enter message for user (id: {user_id}):",
        "ua": "✍️ Введіть повідомлення для користувача (id: {user_id}):",
        "pl": "✍️ Wpisz wiadomość dla użytkownika (id: {user_id}):",
        "ru": "✍️ Введите сообщение для пользователя (id: {user_id}):"
    },
    "msg_sent_user": {
        "en": "✅ Message sent to user.",
        "ua": "✅ Повідомлення відправлено користувачу.",
        "pl": "✅ Wiadomość wysłana do użytkownika.",
        "ru": "✅ Сообщение отправлено пользователю."
    },
    "nothing_to_send": {
        "en": "Nothing to send!",
        "ua": "Нічого надсилати!",
        "pl": "Nie ma czego wysłać!",
        "ru": "Нечего отправлять!"
    },
    "start_again": {
        "en": "Type /start to begin again.",
        "ua": "Напишіть /start щоб почати знову.",
        "pl": "Napisz /start, aby zacząć od nowa.",
        "ru": "Напишите /start чтобы начать заново."
    },
    "msg_reply_from_admin": {
        "en": "💬 Reply from developer:\n\n{message}",
        "ua": "💬 Відповідь від розробника:\n\n{message}",
        "pl": "💬 Odpowiedź od dewelopera:\n\n{message}",
        "ru": "💬 Ответ от разработчика:\n\n{message}"
    },
        "msg_no_reply": {
        "en": "❗ There is no user to reply to. Use /start to reset.",
        "ua": "❗ Немає користувача для відповіді. Використайте /start, щоб почати заново.",
        "pl": "❗ Brak użytkownika do odpowiedzi. Użyj /start, aby rozpocząć od nowa.",
        "ru": "❗ Нет пользователя для ответа. Напишите /start, чтобы начать заново."
    }

}

LANGS = {"en": "Eng 🇬🇧", "ua": "Укр 🇺🇦","pl": "Pol 🇵🇱", "ru": "Рус 🇷🇺"}


def get_text(uid, key, **kwargs):
    lang = user_data.get(uid, {}).get("lang", "en")
    text = TEXTS.get(key, {}).get(lang, "")
    return text.format(**kwargs)


# === /start - выбор языка ===
@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    buttons = [InlineKeyboardButton(text=label, callback_data=f"lang_{code}") for code, label in LANGS.items()]
    keyboard_rows = [buttons[i:i+4] for i in range(0, len(buttons), 4)]
    kb = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

    user_data[user_id] = {"stage": "choose_lang"}
    await message.answer(TEXTS["choose_lang"]["en"], reply_markup=kb)


# === Обработка выбора языка ===
@dp.callback_query(lambda c: c.data.startswith("lang_"))
async def lang_chosen(callback: CallbackQuery):
    user_id = callback.from_user.id
    lang_code = callback.data.split("_")[1]
    user_data[user_id]["lang"] = lang_code
    user_data[user_id]["stage"] = "captcha"

    a, b = random.randint(1, 5), random.randint(1, 5)
    user_data[user_id]["captcha"] = a + b

    await callback.message.edit_text(get_text(user_id, "captcha_question", a=a, b=b))


# === Обработка сообщений пользователя ===
@dp.message(lambda m: m.from_user.id != ADMIN_ID)
async def handle_user(message: Message):
    if not message.text or not message.text.strip():
        return
    
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id not in user_data:
        await message.answer("Напишите /start чтобы начать.")
        return

    stage = user_data[user_id].get("stage", "")

    if stage == "captcha":
        try:
            if int(text) == user_data[user_id]["captcha"]:
                user_data[user_id]["stage"] = "name"
                await message.answer(get_text(user_id, "hello_human"))
            else:
                a, b = random.randint(1, 5), random.randint(1, 5)
                user_data[user_id]["captcha"] = a + b
                await message.answer(get_text(user_id, "captcha_wrong", a=a, b=b))
        except ValueError:
            await message.answer(get_text(user_id, "captcha_enter_number"))
        return

    if stage == "name":
        user_data[user_id]["name"] = text
        user_data[user_id]["stage"] = "reason"
        await message.answer(get_text(user_id, "ask_reason"))

    elif stage == "reason":
        user_data[user_id]["reason"] = text
        user_data[user_id]["stage"] = "message"
        await message.answer(get_text(user_id, "ask_message"))

    elif stage == "message":
        user_data[user_id]["message"] = text
        user_data[user_id]["stage"] = "done"
        lang = user_data[user_id]["lang"]

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS["send_to_admin"][lang], callback_data="send_to_admin")],
            [InlineKeyboardButton(text=TEXTS["restart_form"][lang], callback_data="restart")]
        ])

        await message.answer(
            get_text(user_id, "confirm_message",
                     name=user_data[user_id]["name"],
                     reason=user_data[user_id]["reason"],
                     message=user_data[user_id]["message"]),
            reply_markup=kb
        )
    else:
        await message.answer(get_text(user_id, "start_again"))


# === Отправка админу ===
@dp.callback_query(lambda c: c.data == "send_to_admin")
async def send_to_admin(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = user_data.get(user_id, {})
    lang = data.get("lang", "en")

    if data.get("stage") != "done":
        await callback.answer(TEXTS["nothing_to_send"][lang], show_alert=True)
        return

    user = callback.from_user  # информация о пользователе

    msg = (
        f"📨 Нове повідомлення від користувача:\n\n"
        f"👤 Ім’я профілю: {user.first_name or '-'} {user.last_name or ''}\n"
        f"🔗 Username: @{user.username or 'без_username'}\n"
        f"📱 Telegram ID: {user.id}\n"
        f"🌐 Мова клієнта Telegram: {user.language_code or 'невідомо'}\n"
        f"⭐ Premium: {'Так' if user.is_premium else 'Ні'}\n"
        f"👤 Вказане ім'я: {data.get('name')}\n"
        f"💬 Тема: {data.get('reason')}\n"
        f"📝 Повідомлення:\n{data.get('message')}\n\n"
        f"🕓 Час звернення: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    )

    # Кнопка для ответа админу
    reply_btn = InlineKeyboardButton(
        text="💬 Відповісти користувачу",
        callback_data=f"reply_{user_id}"
    )
    kb_admin = InlineKeyboardMarkup(inline_keyboard=[[reply_btn]])

    await bot.send_message(ADMIN_ID, msg, reply_markup=kb_admin)

    user_data[user_id]["stage"] = "sent"
    await callback.message.answer(TEXTS["msg_sent_admin"][lang])
    await callback.message.delete()



# === Обработка нажатия "Ответить пользователю" ===
@dp.callback_query(lambda c: c.data.startswith("reply_"))
async def reply_to_user(callback: CallbackQuery):
    target_user_id = int(callback.data.split("_")[1])
    admin_id = callback.from_user.id
    awaiting_reply[admin_id] = target_user_id
    await callback.message.answer(get_text(admin_id, "msg_ask_reply", user_id=target_user_id))


# === Ответ администратора пользователю ===
@dp.message(lambda m: m.from_user.id == ADMIN_ID)
async def admin_reply(message: Message):
    if not message.text or not message.text.strip():
        return
    
    admin_id = message.from_user.id
    if admin_id in awaiting_reply:
        target_id = awaiting_reply[admin_id]
        # Получаем язык пользователя
        lang = user_data.get(target_id, {}).get("lang", "en")

        # Формируем сообщение на нужном языке
        reply_text = get_text(target_id, "msg_reply_from_admin", message=message.text)

        await bot.send_message(target_id, reply_text)
        await message.answer(get_text(admin_id, "msg_sent_user"))
        del awaiting_reply[admin_id]
    else:
        await message.answer(get_text(admin_id, "msg_no_reply"))


# === Перезапуск диалога ===
@dp.callback_query(lambda c: c.data == "restart")
async def restart(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data[user_id] = {"stage": "choose_lang"}
    buttons = [InlineKeyboardButton(text=label, callback_data=f"lang_{code}") for code, label in LANGS.items()]
    keyboard_rows = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    kb = InlineKeyboardMarkup(inline_keyboard=keyboard_rows)
    await callback.message.edit_text(TEXTS["choose_lang"]["en"], reply_markup=kb)


# === Обработка webhook ===
async def handle(request):
    try:
        # Логируем тело запроса
        body = await request.text()
        print(f"Request body: {body}")

        # Пробуем распарсить JSON
        data = await request.json()

        # 👇 Логируем тип апдейта (например: ['message'], ['callback_query'] и т.д.)
        print("Update type:", list(data.keys()))

    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return web.Response(status=400, text="Bad Request - Invalid JSON")

    try:
        # Отдаём апдейт в aiogram
        update = types.Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        print(f"Error handling webhook: {e}")
        # Можно залогировать ошибку, но возвращаем 200, чтобы Telegram не ретраил
        return web.Response(status=200, text=f"Error handled: {e}")

    # ✅ Telegram считает это успешным ответом — больше не будет ретраить
    return web.Response(status=200, text="OK")

    
app = web.Application()
app.router.add_post("/webhook", handle)

async def on_startup(app):
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook set: {webhook_url}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()
    print("🛑 Webhook removed and bot stopped.")

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))



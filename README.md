Telegram Bot на Python з Webhook (Deploy на Railway)

Опис

Цей репозиторій містить вихідний код Telegram-бота, написаного на Python з використанням бібліотеки aiogram. Бот використовує webhook для прийому оновлень і розгортається на платформі Railway.com.

---

Можливості

- Робота через webhook (швидка реакція та економія ресурсів)
- Проста настройка і деплой на Railway
- Обробка повідомлень і callback_query
- CAPTCHA з генерацією випадкових цифр і запитом суми для підтвердження, що користувач — людина
- Мультимовна підтримка: англійська, українська, польська та російська мови, з можливістю вибору користувачем
- Збір та отримання всіх необхідних даних про акаунт користувача при взаємодії з ботом

---

Вимоги

- Python 3.11+
- Залежності з requirements.txt (aiogram, aiohttp та інші)

---

Швидкий старт

1. Клонування репозиторію

git clone https://github.com/yourusername/your-telegram-bot.git
cd your-telegram-bot

2. Встановлення залежностей

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

3. Налаштування змінних оточення

Налаштуйте змінні оточення або через файл .env, або в налаштуваннях Railway.

Змінна                  | Опис
------------------------|-----------------------------------------------------------
BOT_TOKEN               | Токен вашого Telegram-бота
RENDER_EXTERNAL_HOSTNAME | Домен застосунку на Railway, наприклад my-telegram-bot.up.railway.app
PORT                    | Порт для запуску застосунку (обрати в налаштуваннях, наприклад 10000)

---

Локальний запуск

python my_telegram_bot.py

---

Розгортання на Railway

1. Створіть новий проєкт і сервіс на Railway з типом Python.
2. В налаштуваннях сервісу вкажіть команду запуску:

python my_telegram_bot.py

3. Додайте необхідні змінні оточення через інтерфейс Railway (наприклад, BOT_TOKEN, RENDER_EXTERNAL_HOSTNAME — замініть на домен Railway).
4. Переконайтеся, що в коді порт береться зі змінної оточення PORT за допомогою os.getenv("PORT", 10000).
5. Згенеруйте публічний домен сервісу через розділ Networking → Generate Domain і використовуйте цей домен для встановлення webhook.
6. Webhook буде автоматично встановлено при старті застосунку, якщо в коді правильно використовується домен із змінних оточення.

---

Структура проєкту

├── my_telegram_bot.py   # Основний скрипт бота
├── requirements.txt     # Список залежностей
├── README.md            # Цей файл
└── .env                 # Локальні змінні оточення (не включати в репозиторій)

---

Важливі моменти

- Використовуйте змінну RENDER_EXTERNAL_HOSTNAME для коректного встановлення webhook.
- В коді в on_startup використовуйте саме цей домен для встановлення webhook.
- При зупинці застосунку рекомендується видаляти webhook (за потреби).

---

Корисні команди

- Перевірити статус webhook:

curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"

- Встановити webhook вручну (якщо потрібно):

curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" -d "url=https://yourdomain.com/webhook"

---

Контакти

Якщо виникнуть питання, пишіть: "SergioManiani.dev@outlook.com" або створюйте issue в репозиторії.

---

Дякую за використання бота!

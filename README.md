Telegram Bot на Python с Webhook (Deploy на Render)

Описание

Этот репозиторий содержит исходный код Telegram-бота, написанного на Python с использованием библиотеки aiogram. Бот использует webhook для приёма обновлений и развертывается на платформе Render.com.

---

Возможности

- Работа через webhook (быстрый отклик и экономия ресурсов)
- Простая настройка и деплой на Render
- Обработка сообщений и callback_query
- CAPTCHA с генерацией случайных цифр и запросом суммы для подтверждения, что пользователь — человек
- Мультиязычная поддержка: английский, украинский, польский и русский языки, с возможностью выбора пользователем
- Сбор и получение всех необходимых данных о аккаунте пользователя при взаимодействии с ботом

---

Требования

- Python 3.11+
- Зависимости из requirements.txt (aiogram, aiohttp и другие)

---

Быстрый старт

1. Клонирование репозитория

git clone https://github.com/yourusername/your-telegram-bot.git
cd your-telegram-bot

2. Установка зависимостей

python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

3. Настройка переменных окружения

Настройте переменные окружения либо через файл .env, либо в настройках Render.

Переменная               | Описание
-------------------------|-----------------------------------------------------------
BOT_TOKEN                | Токен вашего Telegram-бота
RENDER_EXTERNAL_HOSTNAME | Домен приложения на Render, например my-telegram-bot-6bpe.onrender.com
PORT                     | Порт для запуска приложения (обычно 10000)

---

Локальный запуск

python my_telegram_bot.py

---

Развёртывание на Render

1. Создайте новый Web Service на Render.
2. В команду запуска укажите:

python my_telegram_bot.py

3. Добавьте переменные окружения (см. выше).
4. Render автоматически назначит порт, используйте его в коде через os.getenv("PORT").
5. Webhook будет установлен автоматически при старте.

---

Структура проекта

├── my_telegram_bot.py   # Основной скрипт бота
├── requirements.txt     # Список зависимостей
├── README.md            # Этот файл
└── .env                 # Локальные переменные окружения (не включать в репозиторий)

---

Важные моменты

- Используйте переменную RENDER_EXTERNAL_HOSTNAME для корректной установки webhook.
- В коде в on_startup используйте именно этот домен для установки webhook.
- При остановке приложения рекомендуется удалять webhook (если нужно).

---

Полезные команды

- Проверить статус webhook:

curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"

- Установить webhook вручную (если понадобится):

curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" -d "url=https://yourdomain.com/webhook"

---

Контакты

Если возникнут вопросы, пишите: your_email@example.com или создавайте issue в репозитории.

---

Спасибо за использование бота!

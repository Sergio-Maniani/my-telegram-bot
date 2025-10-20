# 🤖 Telegram Bot на Python з Webhook (Deploy на Railway)

## 📝 Опис

Цей репозиторій містить вихідний код **Telegram-бота**, написаного на **Python** з використанням бібліотеки **aiogram**.  
Бот працює через **webhook** для прийому оновлень і розгортається на платформі **Railway**.

---

## ✨ Можливості

- ⚡ Робота через **webhook** (швидка реакція та економія ресурсів)
- ☁️ Просте налаштування і деплой на **Railway**
- 💬 Обробка повідомлень та `callback_query`
- 🔢 **CAPTCHA** із випадковими числами для підтвердження, що користувач — людина
- 🌍 Підтримка декількох мов: **англійська**, **українська**, **польська**, **російська**
- 📋 Збір інформації про користувача при взаємодії з ботом

---

## 🧩 Вимоги

- Python **3.11+**
- Залежності з `requirements.txt`  
  *(aiogram, aiohttp тощо)*

---

## 🚀 Швидкий старт

### 1️⃣ Клонування репозиторію
```bash
git clone https://github.com/Sergio-Maniani/my-telegram-bot.git
cd my-telegram-bot
```

### 2️⃣ Встановлення залежностей
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3️⃣ Налаштування змінних оточення

Можна використовувати `.env` файл локально або налаштувати змінні оточення безпосередньо в Railway.

| Змінна | Опис |
|--------|------|
| `BOT_TOKEN` | Токен вашого Telegram-бота |
| `RENDER_EXTERNAL_HOSTNAME` | Домен Railway, наприклад `my-telegram-bot.up.railway.app` |
| `PORT` | Порт для запуску застосунку (наприклад, `10000`) |

---

## 💻 Локальний запуск
```bash
python my_telegram_bot.py
```

---

## ☁️ Розгортання на Railway

1. Створіть новий **Python** сервіс у Railway.  
2. Укажіть команду запуску:
   ```bash
   python my_telegram_bot.py
   ```
3. Додайте змінні оточення: `BOT_TOKEN`, `RENDER_EXTERNAL_HOSTNAME`, `PORT`.  
4. Переконайтеся, що порт береться з:
   ```python
   web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
   ```
5. Згенеруйте публічний домен у розділі **Networking → Generate Domain**.  
6. Webhook встановиться автоматично при запуску, якщо в коді вказано правильний домен.

---

## 📂 Структура проєкту
```text
├── my_telegram_bot.py   # Основний скрипт бота
├── requirements.txt     # Список залежностей
├── README.md            # Цей файл
└── .env                 # Локальні змінні оточення (не включати в репозиторій)
```

---

## ⚠️ Важливі моменти

- Використовуйте змінну **RENDER_EXTERNAL_HOSTNAME** для коректного встановлення webhook.
- У функції `on_startup` використовуйте:
  ```python
  await bot.set_webhook(f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook")
  ```
- При зупинці застосунку можна видаляти webhook:
  ```python
  await bot.delete_webhook()
  ```

---

## 🧰 Корисні команди

Перевірити статус webhook:
```bash
curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

Встановити webhook вручну:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -d "url=https://yourdomain.com/webhook"
```

---

## 📫 Контакти

Якщо виникнуть питання —  
пишіть на **SergioManiani.dev@outlook.com**  
або створіть **Issue** у репозиторії.

---

# 🇬🇧 English Version

## 🤖 Telegram Bot in Python with Webhook (Deploy on Railway)

### 📝 Description

This repository contains the source code of a **Telegram bot** written in **Python** using the **aiogram** library.  
The bot uses a **webhook** to receive updates and is deployed on the **Railway** platform.

---

### ✨ Features

- ⚡ Works via **webhook** (fast and efficient)
- ☁️ Simple setup and deploy on **Railway**
- 💬 Handles messages and callback queries
- 🔢 **CAPTCHA** check with random numbers to verify users
- 🌍 Multi-language support: **English**, **Ukrainian**, **Polish**, **Russian**
- 📋 Collects key user info for developer messages

---

### 🧩 Requirements

- Python **3.11+**
- Dependencies from `requirements.txt`

---

### 🚀 Quick Start

#### 1️⃣ Clone the repository
```bash
git clone https://github.com/Sergio-Maniani/my-telegram-bot.git
cd my-telegram-bot
```

#### 2️⃣ Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### 3️⃣ Set environment variables

You can set them via `.env` or directly in Railway.

| Variable | Description |
|-----------|-------------|
| `BOT_TOKEN` | Your Telegram bot token |
| `RENDER_EXTERNAL_HOSTNAME` | Your Railway domain, e.g. `my-telegram-bot.up.railway.app` |
| `PORT` | App port, e.g. `10000` |

---

### 💻 Local Run
```bash
python my_telegram_bot.py
```

---

### ☁️ Deploy on Railway

1. Create a **Python** service on Railway  
2. Set startup command:
   ```bash
   python my_telegram_bot.py
   ```
3. Add environment variables: `BOT_TOKEN`, `RENDER_EXTERNAL_HOSTNAME`, `PORT`  
4. Ensure port binding:
   ```python
   web.run_app(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
   ```
5. Generate a public domain under **Networking → Generate Domain**  
6. Webhook auto-sets on startup if the domain is correct.

---

### 📂 Project Structure
```text
├── my_telegram_bot.py   # Main bot script
├── requirements.txt     # Dependencies list
├── README.md            # This file
└── .env                 # Environment variables (excluded from repo)
```

---

### ⚠️ Important Notes

- Always use **RENDER_EXTERNAL_HOSTNAME** when setting webhook  
- In `on_startup`, use:
  ```python
  await bot.set_webhook(f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook")
  ```
- On shutdown:
  ```python
  await bot.delete_webhook()
  ```

---

### 🧰 Useful Commands

Check webhook:
```bash
curl -X GET "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
```

Set webhook manually:
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -d "url=https://yourdomain.com/webhook"
```

---

### 📫 Contact

Questions?  
📧 **SergioManiani.dev@outlook.com**  
or open an **Issue** in the repository.

---

## 💖 Thanks for using this bot!


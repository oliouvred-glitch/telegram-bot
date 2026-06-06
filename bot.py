import os
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/oliouvred-glitch/telegrambot",
                "X-Title": "Telegram Bot"
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {"role": "user", "content": user_text}
                ],
                "max_tokens": 500
            },
            timeout=60
        )

        result = response.json()

        if response.status_code == 200 and "choices" in result:
            answer = result["choices"][0]["message"]["content"]
        else:
            answer = f"OpenRouter Error:\n{result}"

    except Exception as e:
        answer = f"Exception:\n{str(e)}"

    await update.message.reply_text(answer[:4000])

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing")
        return

    if not OPENROUTER_API_KEY:
        print("OPENROUTER_API_KEY missing")
        return

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply
        )
    )

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
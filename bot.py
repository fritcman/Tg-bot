import os

from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🤖\n\n"
        "Я подключён к OpenAI.\n"
        "Просто напиши мне сообщение."
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message or not update.message.text:
        return

    text = update.message.text

    try:
        await update.message.chat.send_action("typing")

        response = client.responses.create(
            model="gpt-5-mini",
            input=text
        )

        answer = response.output_text

        if not answer:
            answer = "Не удалось получить ответ."

        # Telegram ограничивает длину сообщения,
        # поэтому разбиваем слишком длинные ответы.
        for i in range(0, len(answer), 4000):
            await update.message.reply_text(
                answer[i:i + 4000]
            )

    except Exception as error:
        print("ERROR:", error)

        await update.message.reply_text(
            "Произошла ошибка при обращении к OpenAI."
        )


def main():
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot started")

    app.run_polling()


if __name__ == "__main__":
    main()

from config import CONFIG
import pathlib
import datetime
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text(f"Hi!\nUse /set to start tracking the event.\nUse /unset to stop tracking the event.\nUse /{CONFIG['COMMAND']} to reset the event.")


async def count_reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Resetting count :("
    )
    with open("./last_date.txt", "w", encoding="utf8") as file:
        file.write(datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d"))

    await send_days_message(context, update.effective_chat.id)


async def send_days_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int) -> None:
    with open("./last_date.txt", "r", encoding="utf8") as file:
        date_string = datetime.datetime.strptime(file.read(), "%Y-%m-%d").date()
    
    delta = abs(datetime.date.today() - date_string).days
    
    await context.bot.send_message(
        chat_id, text=f"It has been {delta} days since {CONFIG['EVENT_NAME']}."
    )


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""

    job = context.job

    await send_days_message(context, job.chat_id)


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""

    current_jobs = context.job_queue.get_jobs_by_name(name)

    if not current_jobs:
        return False

    for job in current_jobs:
        job.schedule_removal()

    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""

    chat_id = update.effective_message.chat_id

    try:
        job_removed = remove_job_if_exists(str(chat_id), context)

        context.job_queue.run_custom(
            alarm,
            job_kwargs=CONFIG["REMINDER"],
            chat_id=str(chat_id),
            name=str(chat_id)
        )

        text = "Event tracking successfully started!"

        if job_removed:
            text += " Old one was removed."

        await update.effective_message.reply_text(text)

        await send_days_message(context, update.effective_chat.id)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /start")


async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""

    chat_id = update.message.chat_id

    job_removed = remove_job_if_exists(str(chat_id), context)

    text = (
        "Event tracking successfully cancelled!" if job_removed else "You are no longer tracking the event."
    )

    await update.message.reply_text(text)


def main():
    if not pathlib.Path("./last_date.txt").exists():
        with open("./last_date.txt", "x", encoding="utf8") as file:
            file.write(datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d"))

    application = ApplicationBuilder().token(CONFIG["TOKEN"]).build()

    start_handler = CommandHandler(["start", "help"], start)
    set_handler = CommandHandler("set", set_timer)
    unset_handler = CommandHandler("unset", unset)
    count_reset_handler = CommandHandler(CONFIG["COMMAND"], count_reset)
    application.add_handler(start_handler)
    application.add_handler(set_handler)
    application.add_handler(unset_handler)
    application.add_handler(count_reset_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

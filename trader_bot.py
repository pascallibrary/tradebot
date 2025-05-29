# trade_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from market_checker import get_btc_price, generate_trade_signal
from news_filter import check_for_news
from config import BOT_TOKEN
import pytz


tz = pytz.timezone("Africa/Lagos")
        
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Trading Bot Active! Send /signal to get the latest call")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here is your trading signal!")
    

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.job_queue.scheduler.configure(timezone=tz)
     
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    app.run_polling()


if __name__ == "__main__":
    main()
    

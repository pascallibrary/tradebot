# trade_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
from market_checker import get_btc_price, generate_trade_signal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from news_filter import check_for_news
from config import BOT_TOKEN
import pytz


tz = pytz.timezone("Africa/Lagos")
        
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Trading Bot Active! Send /signal to get the latest call")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    signal = generate_trade_signal(get_btc_price())
    await update.message.reply_text("Here is your trading signal!")
    
# job function to run every minute
async def send_btc_signal(context: ContextTypes.DEFAULT_TYPE):
    price = get_btc_price()
    signal = generate_trade_signal(price)
    news = check_for_news()
    
    message = f'📈 BTC Price: ${price} \n 📊 Signal: {signal}\n📰 News: {news or 'No major news'}'


def main():
    # set the timezone using pytz
    tz = pytz.timezone('Africa/Lagos')
    app = ApplicationBuilder().token(BOT_TOKEN).build()
      
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    
    # schedule the btc job every 60 seconds
    
    app.job_queue.run_repeating(send_btc_signal, interval=60, first=5, timezone=pytz.timezone('Africa/Lagos'))

    app.run_polling()


if __name__ == "__main__":
    main()
    

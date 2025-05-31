# trade_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
from market_checker import get_btc_price, generate_trade_signal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from news_filter import check_for_news
from config import BOT_TOKEN
import pytz

# global variable to store the chat id for scheduled messages 

TARGET_CHAT_ID = None

tz = pytz.timezone("Africa/Lagos")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.message.chat_id
    await update.message.reply_text("Trading Bot Active! Send /signal to get the latest call. I will also send scheduled updates here.")
    print(f"Bot started in chat_id: {TARGET_CHAT_ID}")
    

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_btc_price()
    signal = generate_trade_signal(price)
    await update.message.reply_text("Here is your trading signal! \n Signal: {signal_text}")
    
# job function to run every minute
async def send_btc_signal(context: ContextTypes.DEFAULT_TYPE):
    if not TARGET_CHAT_ID:
        print("TARGET_CHAT_ID not set. Cannot send scheduled messages.")
        return
    
    price = get_btc_price
    signal_text = generate_trade_signal(price)
    news = check_for_news()
    
    message = f'📈 BTC Price: ${price} \n 📊 Signal: {signal_text}\n📰 News: {news or 'No major news'}'
    
    try:
       await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message)
       print(f"Sent Signal to {TARGET_CHAT_ID}")
    except Exception as e:
       print(f"Error sending message to {TARGET_CHAT_ID}: {e}")

def main():
    # set the timezone using pytz
    tz = pytz.timezone('Africa/Lagos')
    app = ApplicationBuilder().token(BOT_TOKEN).build()
      
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    
    # schedule the btc job every 60 seconds
    
    app.job_queue.run_repeating(send_btc_signal, interval=60, first=5)

    app.run_polling()


if __name__ == "__main__":
    main()
    

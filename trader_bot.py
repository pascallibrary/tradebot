# trade_bot.py

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue, Defaults
from market_checker import get_btc_price, generate_trade_signal
from news_filter import check_for_news
from config import BOT_TOKEN
import pytz
import logging


# ---configure logging---
# create a logger object

logger = logging.getLogger(__name__)
# set the logging level (eg, INFO, DEBUG, WARNING, ERROR)
logger.setLevel(logging.INFO)

# create a console handler and set its level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create a formatter and add it to the header
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# add the handler to the logger
if not logger.handlers:
  logger.addHandler(ch)

# ---end logging config---


# global variable to store the chat id for scheduled messages 

TARGET_CHAT_ID = None

tz = pytz.timezone("Africa/Lagos") # define globally


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = update.message.chat_id
    await update.message.reply_text("Trading Bot Active! Send /signal to get the latest call. I will also send scheduled updates here.")
    logger.info(f"Bot started in chat_id: {TARGET_CHAT_ID}") # user log info
    

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_price = get_btc_price()
    signal_text = generate_trade_signal(current_price)
    await update.message.reply_text(f"Here is your trading signal! \n Signal: {signal_text}")
    logger.info(f"User {update.effective_user.id} requested signal. Sent: {signal_text}")
    
# job function to run every minute
async def send_btc_signal(context: ContextTypes.DEFAULT_TYPE):
    if not TARGET_CHAT_ID:
        logger.warning("TARGET_CHAT_ID not set. Cannot send scheduled messages.")
        return
    
    current_price = get_btc_price()
    signal_text = generate_trade_signal(current_price)
    news = check_for_news()
    
     
    # Call check_for_news() and unpack its return values BEFORE using them
    has_relevant_news, top_headlines = check_for_news()
    
    # Adjust the message to reflect the new news output
    news_info = ""
    if has_relevant_news: # Check the boolean flag first
      news_info = "\n**Market Alert!** Relevant news detected:\n" + "\n".join([f"- {h}" for h in top_headlines])
    elif top_headlines: # If no relevant news, but headlines were still fetched
      news_info = "\n📰 Recent Headlines:\n" + "\n".join([f"- {h}" for h in top_headlines])
    else: # No headlines or error fetching news
      news_info = "\n📰 News: No major news (or error fetching headlines)."


    message = (
      f'📈 BTC Price: ${current_price:,.2f} \n'
      f'📊 Signal: {signal_text}'
      f'{news_info}' # Include the structured news info
    )
    
    try:
       await context.bot.send_message(chat_id=TARGET_CHAT_ID, text=message)
       logger.info(f"Sent Signal to {TARGET_CHAT_ID}. Message: {message.replace('\n', ' ')}")
    except Exception as e:
       logger.error(f"Error sending message to {TARGET_CHAT_ID}: {e}", exc_info=True)

def main():
    # set the timezone using pytz
    defaults = Defaults(tzinfo=tz)
    app = ApplicationBuilder().token(BOT_TOKEN).defaults(defaults).build()
      
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    
    # schedule the btc job every 60 seconds
    
    app.job_queue.run_repeating(send_btc_signal, interval=60, first=5)

    logger.info("Bot is polling and jobs are scheduled...")
    app.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
    

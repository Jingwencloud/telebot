import logging
from dotenv import load_dotenv
import telegram
from telegram import Update
from telegram.ext import Updater, Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from query import search
import geopy
import asyncio


load_dotenv()
TOKEN = os.getenv('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!")

async def search_bin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttonList =  [[telegram.KeyboardButton(text='Share your location!', request_location = True)]]
    markup = telegram.ReplyKeyboardMarkup(buttonList, one_time_keyboard = True)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Share your location with us to find out the nearest e-waste bin! "
                                        + "Remember to turn on location services :)",
                                   reply_markup=markup)


async def manage_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    long= update.message.location.longitude
    location = geolocator.reverse([lat, long])
    postal_code = location.raw['address']['postcode']
    messages = search(postal_code, db)
    for msg in messages:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text = msg)

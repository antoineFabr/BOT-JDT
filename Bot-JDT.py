import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import datetime
import pytz
import requests

load_dotenv()

TOKEN = os.get_env('TOKEN_BOT')
URL_SHEET = os.get_env('GOOGLE_SHEET_LINK')

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  chat_id = update.effective_chat.id

  await update.message.reply_text(f"Bot-JDT activé ! tous les vendredis tu recevra une visualisation du rendu de ton journal de travail de la semain")


  #on enleve le job s'il existe deja (pour le créer ensuite)
  current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
  for job in current_jobs:
    job.schedule_removal()

  #création du job
  context.job_queue.run_daily(
    callback=generate_JDT(context),
    time=datetime.time(hour=18, minute=30, tzinfo=pytz.timezone('Europe/Paris')), #on lance la fonction à 18h30
    days=(4,), #le vendredi
    chat_id=chat_id,
  )


async def generate_JDT(context: ContextTypes.DEFAULT_TYPE):
  chat_id = context.job.chat_id
  message = "Generation du mail du journal de travail"
  await context.bot.send_message(chat_id=chat_id, text=message)

  #TODO 1 récuperation des données dans le google sheet du jdt
  response = requests.get(URL_SHEET)

  #TODO 2 mise en forme d'un mail du journal de travail de la bonne semaine
  #TODO 3 Confirmation du mail par l'utilisateur
  #TODO 4 Envoit du mail aux formateurs / Profs (ETML)



if __name__ == '__main__':
  application = ApplicationBuilder().token(TOKEN).build()

  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)
  application.run_polling()

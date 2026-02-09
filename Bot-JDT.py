import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import datetime
import pytz
import requests
from generateJDT import generate_JDT
import markdown
from email.message import EmailMessage
import smtplib

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')
MAIL = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('EMAIL_PASSWORD')

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
  context.job_queue.run(

    callback=send_JDT,
    chat_id=chat_id

)

import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import datetime
import pytz
import requests
from generateJDT import generate_JDT
import markdown
from email.message import EmailMessage
import smtplib

load_dotenv()

TOKEN = os.getenv('TOKEN_BOT')
MAIL = os.getenv('EMAIL_ADDRESS')
PASSWORD = os.getenv('EMAIL_PASSWORD')

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
  context.job_queue.run_once(
    when=2,
    callback=send_JDT,
    chat_id=chat_id,
    user_id=update.effective_user.id
)


async def send_JDT(context: ContextTypes.DEFAULT_TYPE):
  chat_id = context.job.chat_id
  message = "Generation du mail du journal de travail..."
  await context.bot.send_message(chat_id=chat_id, text=message)


  body_mail_MD = await generate_JDT()
  context.user_data['pending_mail_body'] = body_mail_MD

  keyboard = [
        [
            InlineKeyboardButton("Envoyer le mail", callback_data="send_mail"),
            InlineKeyboardButton("Annuler", callback_data="cancel_mail")
        ]
    ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await context.bot.send_message(
    chat_id=chat_id,
    text=f"Voici la preview du mail :\n\n {body_mail_MD}",
    reply_markup=reply_markup,
    parse_mode="Markdown"
  )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query

    # Obligatoire : dire à Telegram qu'on a bien reçu le clic (arrête le sablier)
  await query.answer()

    # Récupérer le choix (callback_data)
  choice = query.data
  body_md = context.user_data.get('pending_mail_body')

  if choice == "send_mail":
    print("envoyer le mail !!")
    await send_mail(body_md)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Mail envoyé avec succes, à la semaine prochaine !")


  elif choice == "cancel_mail":
      print("❌ mail annulé")


async def send_mail(body_md):

  HTML_BODY = markdown.markdown(body_md, extensions=['tables'])
  css_style = """
    <html>
    <head>
    <style>
        body { font-family: Arial, sans-serif; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
    </head>
    <body>
    """

  full_html = css_style + HTML_BODY + "</body></html>"
  msg = EmailMessage()
  msg['Subject'] = 'Journal de travail'
  msg['From'] = MAIL
  msg['To'] = 'formateurs-fsd@groupes.epfl.ch, xavier.carrel@eduvaud.ch'
  msg.set_content(full_html,subtype='html')

  try:
    print(f"DEBUG: Connexion à smtp.gmail.com via {MAIL}")
    # Connexion au serveur Outlook
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls() # Sécurisation de la connexion
        print(MAIL)
        print(PASSWORD)
        smtp.login(MAIL, PASSWORD)
        smtp.send_message(msg)
    print("Email envoyé avec succès !")
  except Exception as e:
        print(f"❌ Autre erreur : {e}")
        raise e






if __name__ == '__main__':
  application = ApplicationBuilder().token(TOKEN).build()

  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)
  application.add_handler(CallbackQueryHandler(button_handler))
  application.run_polling()

async def send_JDT(context: ContextTypes.DEFAULT_TYPE):
  chat_id = context.job.chat_id
  message = "Generation du mail du journal de travail..."
  await context.bot.send_message(chat_id=chat_id, text=message)


  body_mail_MD = await generate_JDT()
  context.user_data['pending_mail_body'] = body_mail_MD

  keyboard = [
        [
            InlineKeyboardButton("Envoyer le mail", callback_data="send_mail"),
            InlineKeyboardButton("Annuler", callback_data="cancel_mail")
        ]
    ]
  reply_markup = InlineKeyboardMarkup(keyboard)
  await context.bot.send_message(
    chat_id=chat_id,
    text=f"Voici la preview du mail :\n\n {body_mail_MD}",
    reply_markup=reply_markup,
    parse_mode="Markdown"
  )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query

    # Obligatoire : dire à Telegram qu'on a bien reçu le clic (arrête le sablier)
  await query.answer()

    # Récupérer le choix (callback_data)
  choice = query.data
  body_md = context.user_data.get('pending_mail_body')

  if choice == "send_mail":
    print("envoyer le mail !!")
    await send_mail(body_md)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Mail envoyé avec succes, à la semaine prochaine !")


  elif choice == "cancel_mail":
      print("❌ mail annulé")


async def send_mail(body_md):

  HTML_BODY = markdown.markdown(body_md, extensions=['tables'])
  css_style = """
    <html>
    <head>
    <style>
        body { font-family: Arial, sans-serif; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
    </head>
    <body>
    """

  full_html = css_style + HTML_BODY + "</body></html>"
  msg = EmailMessage()
  msg['Subject'] = 'Journal de travail'
  msg['From'] = MAIL
  msg['To'] = 'formateurs-fsd@groupes.epfl.ch, xavier.carrel@eduvaud.ch'
  msg.set_content(full_html,subtype='html')

  try:
    print(f"DEBUG: Connexion à smtp.gmail.com via {MAIL}")
    # Connexion au serveur Outlook
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls() # Sécurisation de la connexion
        print(MAIL)
        print(PASSWORD)
        smtp.login(MAIL, PASSWORD)
        smtp.send_message(msg)
    print("Email envoyé avec succès !")
  except Exception as e:
        print(f"❌ Autre erreur : {e}")
        raise e






if __name__ == '__main__':
  application = ApplicationBuilder().token(TOKEN).build()

  start_handler = CommandHandler('start', start)
  application.add_handler(start_handler)
  application.add_handler(CallbackQueryHandler(button_handler))
  application.run_polling()

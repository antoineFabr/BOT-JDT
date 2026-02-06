import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import datetime
import pytz
import requests
import asyncio
import re
import json
from datetime import datetime



load_dotenv()

URL_SHEET = os.getenv('GOOGLE_SHEET_LINK')

async def generate_JDT():
  #chat_id = context.job.chat_id
  #message = "Generation du mail du journal de travail"
  #await context.bot.send_message(chat_id=chat_id, text=message)

  response = requests.get(URL_SHEET)

  if response.status_code == 200 :
    tableau = response.text
    pattern = r'google\.visualization\.Query\.setResponse\((.*)\);'
    match = re.search(pattern, tableau)

    if match:
        # On récupère le groupe capturé (le JSON pur)
        json_str = match.group(1)

        # 4. Convertir en objet Python (dict)
        data = json.loads(json_str)

        # Affichage pour vérifier
        print("Statut:", data['status'])
        #print("table:", data["table"])
    else:
       print("Impossible de récuperer le json")
       return False


  #TODO 1 récuperation de la bonne semaine dans ce qu'on récupère du jdt
  Last_week = []
  today = datetime.today().strftime('%d/%m/%y')

  rows = data['table']['rows']
  for i ,day in enumerate(rows):
    if today in day['c'][0].get('f',''):
      print(f"Aujourd'hui ! : ", day['c'][0].get('f',''))
      print(f"Donc la case numero : ", i)
      start_index = max(0, i - 5)

      end_index = i
      Last_week = rows[start_index : end_index]
      break
    else:
      continue

  print(Last_week)







  #TODO 2 mise en forme d'un mail du journal de travail de la bonne semaine
  #TODO 3 Confirmation du mail par l'utilisateur
  #TODO 4 Envoit du mail aux formateurs / Profs (ETML)

if __name__ == '__main__':
  asyncio.run(generate_JDT())
import os
from dotenv import load_dotenv
import datetime
import pytz
import requests
import asyncio
import re
import json
from datetime import datetime
import markdown




load_dotenv()

URL_SHEET = os.getenv('GOOGLE_SHEET_LINK')

def generate_day_content(day):
  date_jour = day['c'][0].get('f', 'Date inconnue')
  debut = day['c'][1].get('f', '-') if day['c'][1] else '-'
  pause_deb = day['c'][2].get('f', '-') if day['c'][2] else '-'
  pause_fin = day['c'][3].get('f', '-') if day['c'][3] else '-'
  fin = day['c'][4].get('f', '-') if day['c'][4] else '-'
  h_sup = day['c'][5].get('f', '-') if day['c'][5] else '-'
  h_journée = day['c'][6].get('f', '-') if day['c'][6] else '-'




  tache = day['c'][9].get('v', '')

  taches = tache.split(",")

  items = [f"- {t}" for t in taches if t]
  md_taches = "\n".join(items)


  problemes = day['c'][10].get('v', '')
  if problemes:
       md_problemes = f"Problèmes : {problemes}"
  else:
       md_problemes = ""

  #Markdown_problemes = [f"- {item}" for item in problemes]

  block_day = f"""
### {date_jour}

| Début de journée | Début de la pause | Fin de la pause | Fin de journée | Heures sup | Heure de la journée |
|----------|----------|----------|----------|----------|----------|
| {debut} | {pause_deb} | {pause_fin} | {fin} | {h_sup} | {h_journée} |

**Tâches effectuées :**
{md_taches}

{md_problemes}
---
"""



  return block_day




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


  #récuperation de la bonne semaine dans ce qu'on récupère du jdt
  Last_week = []
  today = datetime.today().strftime('%d/%m/%y')

  rows = data['table']['rows']
  for i ,day in enumerate(rows):
    if today in day['c'][0].get('f',''):
      print(f"Aujourd'hui ! : ", day)
      print(f"Donc la case numero : ", i)
      start_index = max(0, i - 5)

      end_index = i + 1
      Last_week = rows[start_index : end_index]
      break
    else:
      continue


  FINAL_BODY = f"""
# Journal de Travail
**Semaine du {Last_week[0]['c'][0].get('f')} au {Last_week[-1]['c'][0].get('f')}**

Bonjour,

Voici le récapitulatif de mes heures et activités pour cette semaine.
"""





  #TODO 2 mise en forme d'un mail du journal de travail de la bonne semaine
  #Lundi, Mardi, Mercredi, Jeudi, Vendredi = Last_week
  #Partie horaire
  MarkDown_Final = []
  print(Last_week[4]['c'][8].get('f',''))
  for i, day in enumerate(Last_week):
    FINAL_BODY += generate_day_content(day)

  FINAL_BODY += f"""
Temps effectué cette semaine : {Last_week[4]['c'][7].get('f','')}

Heures supp effectuées cette semaine : {Last_week[4]['c'][8].get('f','')}

Bilan de la semaine : {Last_week[4]['c'][11].get('f','')}

Je vous souhaite un excellent week-end.

Cordialement,

**Antoine Fabre**

ps: ce mail est généré automatiquement.
"""
  return FINAL_BODY



if __name__ == '__main__':
  asyncio.run(generate_JDT())





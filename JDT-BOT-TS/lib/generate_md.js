export function generateMD(filterJDT) {

  let FinalBody = `
# Journal de travail \n
**Semaine du ${filterJDT[0].c[0].f} au ${filterJDT[4].c[0].f}** \n

Bonjour, \n \n
Voici le récapitulatif de mes heures et activités pour cette semaine. \n
`
for (const day of filterJDT) {
  FinalBody += generateDayContent(day);
}

FinalBody += `
Temps effectué cette semaine : ${filterJDT[4].c[7].f}

Heures supp effectuées cette semaine : ${filterJDT[4].c[8].f}

Bilan de la semaine : ${filterJDT[4].c[11].v}

Je vous souhaite un excellent week-end.

Cordialement,

**Antoine Fabre**

ps: Ce mail est généré automatiquement.
`

return FinalBody;
}

function generateDayContent(day){
  const jour = day.c;
  const date_jour = jour[0].f ? jour[0].f : "Date inconnue"
  const debut = jour[1].f ? jour[1].f : "-"
  const pause_deb = jour[2].f ? jour[2].f : "-"
  const pause_fin = jour[3].f ? jour[3].f : "-"
  const fin = jour[4].f ? jour[4].f : "-"
  const h_sup = jour[5].f ? jour[5].f : "-"
  const h_journée = jour[6].f ? jour[6].f : "-"

  const blocTache = jour[9].v;

  const taches = blocTache.split(",");

  let items = [];

  for(const t of taches) {
    items.push(`- ${t} \n`)
  }

  const tachesMD = items.join("\n")
  const probleme = jour[10];
  const problemes = probleme ? probleme.v : "-"

  const dayMD = `
### ${date_jour} \n

| Début de journée | Début de la pause | Fin de la pause | Fin de journée | Heures sup | Heure de la journée |
|----------|----------|----------|----------|----------|----------|
| ${debut} | ${pause_deb} | ${pause_fin} | ${fin} | ${h_sup} | ${h_journée} |

**Tâches effectuées :**


${tachesMD}


**Problèmes :**

${problemes}

---

  `
return dayMD;
}
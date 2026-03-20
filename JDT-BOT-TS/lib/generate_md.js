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
Temps effectué cette semaine : ${filterJDT[4].c[7].f} \n
Heures supp effectuées cette semaine : ${filterJDT[2].c[7].f} \n
Heures supp total : ${filterJDT[3].c[7].f} \n

Bilan de la semaine : ${filterJDT[4].c[10].v} \n

Je vous souhaite un excellent week-end.

Cordialement,

**Jérémy Würsch**
`

  return FinalBody;
}

function generateDayContent(day) {
  const jour = day.c;
  const date_jour = jour[0]?.f ? jour[0].f : "Date inconnue"
  const debut = jour[1]?.v ? jour[1].v : "-"
  const pause_deb = jour[2]?.v ? jour[2].v : "-"
  const pause_fin = jour[3]?.v ? jour[3].v : "-"
  const fin = jour[4]?.v ? jour[4].v : "-"
  const h_dehors = jour[5]?.v ? jour[5].v : "-"
  const h_journée = jour[6]?.f ? jour[6].f : "-"

  const blocTache = jour[8]?.v ? jour[8]?.v : "-";

  const taches = blocTache.split(",");

  let items = [];

  for (const t of taches) {
    items.push(`- ${t} \n`)
  }

  const tachesMD = items.join("\n")
  const probleme = jour[9];
  const problemes = probleme ? probleme.v : "-"
  let dayMD = "";
  if (jour[1]?.v.toLowerCase() === "cours" || jour[1]?.v.toLowerCase() === "cie") {
    dayMD = `
### ${date_jour} \n
En ${jour[1]?.v.toLowerCase()}
---
  `
  } else {
    dayMD = `
### ${date_jour} \n

| Début de journée | Début de la pause | Fin de la pause | Fin de journée | Heures en dehors | Heure de la journée |
|----------|----------|----------|----------|----------|----------|
| ${debut} | ${pause_deb} | ${pause_fin} | ${fin} | ${h_dehors} | ${h_journée} |

**Tâches effectuées :**


${tachesMD}


**Problèmes :**

${problemes}

---

  `
  }
  return dayMD;
}
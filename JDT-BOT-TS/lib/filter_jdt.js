export function filterJDT(jdtJSON) {

  const date = new Date();
  const dayOfWeek = date.getDay();

  // Ajustement de la date si on a oublié de l'envoyer vendredi
  if (dayOfWeek === 6) {
    // Si on est samedi, on recule de 1 jour pour cibler vendredi
    date.setDate(date.getDate() - 1);
  } else if (dayOfWeek === 0) {
    // Si on est dimanche, on recule de 2 jours
    date.setDate(date.getDate() - 2);
  } else if (dayOfWeek === 1) {
    // Si on a complètement oublié et qu'on est lundi, on recule de 3 jours
    date.setDate(date.getDate() - 3);
  } else if (dayOfWeek === 4) {
    date.setDate(date.getDate() + 1)
  }

  const today = date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit'
  });
  let Last_week = [];

  const rows = jdtJSON.table.rows
  for (const[i, day] of rows.entries()) {
    if (day.c && day.c[0]) {

      const cellValue = day.c[0].f

      if(cellValue.includes(today)) {

        Last_week = rows.slice(i - 4, i+ 1)
      }
    }
  }
  return Last_week;
}
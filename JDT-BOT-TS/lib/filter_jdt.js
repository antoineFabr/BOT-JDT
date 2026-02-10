export function filterJDT(jdtJSON) {

  const date = new Date();
  const today = "06/02/26"

  /*date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: '2-digit'
  });*/

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
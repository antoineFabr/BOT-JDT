import showdown  from "showdown";


export function generateHTML(mailMD) {
  const converter = new showdown.Converter({
    tables: true,
    strikethrough: true,
  });

  const css = `
    <style>
        body { font-family: Arial, sans-serif; color: #333; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        h3 { color: #0056b3; border-bottom: 1px solid #eee; padding-bottom: 5px; }
    </style>
  `;

  const bodyHtml = converter.makeHtml(mailMD);

  const finalHtml = `<html><head>${css}</head><body>${bodyHtml}</body></html>`;

  return finalHtml;
}
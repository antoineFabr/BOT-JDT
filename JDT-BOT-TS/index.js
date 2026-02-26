import { getJDT } from "./lib/get_jdt";
import { filterJDT } from "./lib/filter_jdt";
import { generateMD } from "./lib/generate_md";
import { generateHTML } from "./lib/generate_html";
import { Telegraf } from "telegraf";
import cron  from "node-cron"
import { sendMail } from "./lib/send_mail";

const bot = new Telegraf(process.env.BOT_TOKEN)



const url = process.env.GOOGLE_SHEET_LINK

bot.action('yes', async ctx => {
  ctx.editMessageReplyMarkup();
  const html = await Bun.file('mail.html').text();
  await sendMail(process.env.MAIL_TO, process.env.MAIL_SUBJECT, process.env.MAIL_CC, html);
  console.log("Envoi du mail a été fait ✅");

  bot.telegram.sendMessage(process.env.CHAT_ID, `Le mail a bien été envoyé à ${process.env.MAIL_TO}`);
})

bot.action('no', async ctx => {
    ctx.editMessageReplyMarkup();
    console.log("Envoi du mail annulé ❌");
    bot.telegram.sendMessage(ctx.chat.id, 'Oke, aucun mail ne sera envoyé pour ce JDT');
    })

async function job_bot(ChatId) {
  try {
    const jdtJSON = await getJDT(url);
    console.log("Journal de travail récuperé avec succès ✅")

    const jdtFilter = filterJDT(jdtJSON);
    console.log("Journal de travail filtré ✅")

    const mailMD = generateMD(jdtFilter);
    console.log("Le markdown du mail a bien été généré ✅")

    const mailHTML = generateHTML(mailMD);
    console.log("Le Html du mail a bien été généré ✅")

    Bun.write('mail.html', mailHTML);
    await bot.telegram.sendMessage(ChatId, mailMD, {
            parse_mode: 'Markdown',
            reply_markup: {
                inline_keyboard: [
                    [{ text: `Envoyer le mail à ${process.env.MAIL_TO}`, callback_data: "yes" }],
                    [{ text: "Ne pas envoyer le mail", callback_data: "no" }]
                ]
            }
        });
  } catch (error) {
        console.error("Erreur durant le job:", error);
    }
}


bot.start((ctx) => {
  // il faut lancer un cron tous les vendredis a 18h30
  // 30 18 * * 5 pour vendredi 18h30
  cron.schedule('30 18 * * 5', () => {
    console.log("Lancement du job ⚙️")
    job_bot(ctx.chat.id)
  })
  ctx.reply("Vous avez activé le Bot-JDT, cela veut dire que tous les vendredis à 18h30 une confirmation de mail vous sera envoyé pour confirmer l'envoi de votre journal de travail à vos formateurs")
})

bot.launch();



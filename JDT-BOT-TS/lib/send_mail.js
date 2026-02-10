import nodemailer from "nodemailer";

export async function sendMail(receiver, subject, copy, html) {
  const transporter = nodemailer.createTransport({
    host: "mail.epfl.ch",
    port: 587,
    secure: false,
    auth: {
      user: process.env.AUTH_USER,
      pass: process.env.AUTH_PASSWORD
    },
  });

  return transporter.sendMail({
    from: process.env.MAIL_ADDRESS,
    to: receiver,
    subject: subject,
    html: html,
    replyTo: process.env.MAIL_REPLY_TO,
    cc: copy
  })
}
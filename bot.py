from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread
import datetime

TOKEN = "8625718826:AAERffGtA6sl20MPqajLVRXhOvrnH4Ej5vA"

users = {}

# Partie Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in users:
        users[user_id] = {"premium": False}
    await update.message.reply_text(
        "👋 Bienvenue !\n\n"
        "Je t’envoie des opportunités IA & business.\n\n"
        "🆓 Gratuit : 1 alerte / jour\n"
        "💎 Premium : toutes les alertes\n\n"
        "Commande : /alerte"
    )

async def alerte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    today = datetime.date.today()
    if user_id not in users:
        users[user_id] = {"premium": False, "last": None}
    if not users[user_id]["premium"]:
        if users[user_id].get("last") == today:
            await update.message.reply_text("⏳ Alerte gratuite déjà utilisée aujourd’hui.")
            return
        users[user_id]["last"] = today
    await update.message.reply_text(
        "🚀 Opportunité IA du jour :\nUn outil IA B2B sous-exploité.\n💡 Plus d’alertes en premium."
    )

app_telegram = ApplicationBuilder().token(TOKEN).build()
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(CommandHandler("alerte", alerte))

# Partie Flask pour Render
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot en ligne !"

def run_flask():
    app_flask.run(host='0.0.0.0', port=10000)

Thread(target=run_flask).start()
app_telegram.run_polling()
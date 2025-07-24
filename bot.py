import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration - Set these in Render.com environment variables
BOT_TOKEN = os.getenv('8440264312:AAGgPJ8wfy5WCtF7RPG1jCE6nHZwCEpizWc')
CHANNEL_LINK = "https://t.me/eaexperts"
CHANNEL_USERNAME = "@eaexperts"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = (
        f"👋 Hello {user.username or 'there'}!\n\n"
        "🌟 Welcome to Forex Experts – your gateway to automated trading solutions!\n\n"
        "📈 Access our Copy Trade service featuring advanced EAs and trading robots "
        "designed for efficient market participation.\n\n"
        "👉 Join our channel for real-time updates and performance tracking:\n"
    )

    keyboard = [
        [InlineKeyboardButton("✨ Join Official Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="joined")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def handle_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    success_message = (
        "🚀 Well done! You're on the right path.\n\n"
        "Important next steps:\n"
        "1. Stay active in our channel for daily updates\n"
        "2. Explore pinned messages for key resources\n"
        "3. Contact support @[your_support] for assistance\n\n"
        "*Note: Trading involves risk. Past performance doesn't guarantee future results.*"
    )
    
    await query.edit_message_text(
        success_message,
        reply_markup=None
    )

def main():
    # Create Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_joined, pattern="joined"))
    
    # Start Bot
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()

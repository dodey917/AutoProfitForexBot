import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - Direct token assignment for testing (remove in production)
BOT_TOKEN = "8440264312:AAGgPJ8wfy5WCtF7RPG1jCE6nHZwCEpizWc"  # TEMPORARY - REPLACE WITH ENV VAR
CHANNEL_LINK = "https://t.me/eaexperts"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = (
        f"👋 Hello {user.username or 'trader'}!\n\n"
        "🌟 Welcome to Forex Experts - automated trading solutions.\n\n"
        "📈 Access our Copy Trade service with advanced EAs.\n\n"
        "👉 Join our channel for updates:"
    )

    keyboard = [
        [InlineKeyboardButton("✨ Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Verify Join", callback_data="joined")]
    ]
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
    )

async def handle_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🚀 Well done! You're all set.\n\n"
        "*Note: Trading involves risk. Past performance ≠ future results.*",
        parse_mode="Markdown"
    )

def main():
    try:
        # Validate token format
        if ":" not in BOT_TOKEN:
            raise ValueError("Invalid token format. Should be 'numbers:letters'")
        
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_join, pattern="^joined$"))
        
        logger.info("Bot is running...")
        app.run_polling()
        
    except Exception as e:
        logger.critical(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()

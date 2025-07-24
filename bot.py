#!/usr/bin/env python3
"""
Forex Channel Access Bot
- Robust error handling
- Deployment-ready configuration
- Comprehensive logging
- Telegram policy compliant
"""

import os
import sys
import logging
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ----------------------
# Configuration
# ----------------------
class Config:
    # Get environment variables with validation
    @staticmethod
    def get_env_var(name: str, optional: bool = False) -> str:
        value = os.getenv(name)
        if not value and not optional:
            logging.critical(f"Environment variable '{name}' not set!")
            sys.exit(1)
        return value or ""

    # Bot settings
    TOKEN = get_env_var("8440264312:AAGgPJ8wfy5WCtF7RPG1jCE6nHZwCEpizWc")
    CHANNEL_LINK = "https://t.me/eaexperts"
    ADMIN_ID = get_env_var("ADMIN_ID", optional=True)
    
    # Messages
    START_MSG = """
👋 Hello {username}!

🌟 Welcome to Forex Experts - automated trading solutions.

📈 Access our Copy Trade service with advanced EAs and trading robots.

👉 Join our channel for updates:
"""
    JOINED_MSG = """
✅ Success! You've joined our channel.

Next steps:
1. Check pinned messages
2. Review daily insights
3. Contact support if needed

*Note: Trading involves risk. Past performance ≠ future results.*
"""

# ----------------------
# Logging Setup
# ----------------------
def setup_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    # Suppress noisy library logs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

# ----------------------
# Bot Handlers
# ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    try:
        user = update.effective_user
        username = user.username or "trader"
        
        keyboard = [
            [InlineKeyboardButton("✨ Join Channel", url=Config.CHANNEL_LINK)],
            [InlineKeyboardButton("✅ Verify Join", callback_data="joined")]
        ]
        
        await update.message.reply_text(
            Config.START_MSG.format(username=username),
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True,
        )
        logging.info(f"Sent welcome message to {username}")
        
    except Exception as e:
        logging.error(f"Error in start handler: {e}", exc_info=True)
        await notify_admin(f"⚠️ Start handler error: {e}")

async def handle_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle join verification"""
    try:
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            Config.JOINED_MSG,
            parse_mode="Markdown",
            reply_markup=None,
        )
        logging.info(f"User {query.from_user.username} verified join")
        
    except Exception as e:
        logging.error(f"Error in join handler: {e}", exc_info=True)
        await notify_admin(f"⚠️ Join handler error: {e}")

async def notify_admin(message: str):
    """Notify admin about errors"""
    if Config.ADMIN_ID:
        try:
            app = Application.builder().token(Config.TOKEN).build()
            await app.bot.send_message(
                chat_id=Config.ADMIN_ID,
                text=message,
            )
        except Exception as e:
            logging.error(f"Failed to notify admin: {e}")

# ----------------------
# Application Setup
# ----------------------
def create_application() -> Application:
    """Create and configure bot application"""
    try:
        # Validate token format before creating application
        if ":" not in Config.TOKEN:
            raise ValueError("Invalid token format. Should be '1234567890:ABCdef...'")
        
        app = Application.builder().token(Config.TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_join, pattern="^joined$"))
        
        return app
        
    except Exception as e:
        logging.critical(f"Failed to create application: {e}")
        sys.exit(1)

# ----------------------
# Main Execution
# ----------------------
def main():
    setup_logging()
    
    try:
        logging.info("🚀 Starting Forex Experts Bot")
        app = create_application()
        
        # Start polling
        logging.info("🔄 Starting polling...")
        app.run_polling()
        
    except Exception as e:
        logging.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

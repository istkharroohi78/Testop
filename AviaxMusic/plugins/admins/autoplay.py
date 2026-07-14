from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

# AviaxMusic ke standard imports (apne fork ke hisaab se folder name adjust kar lena)
from config import BANNED_USERS
from AviaxMusic import app
from AviaxMusic.utils.database import is_active_chat
# Agar aapke DB me get/set autoplay functions alag naam se hain, toh unhe yahan import karein
from AviaxMusic.utils.database import get_autoplay, set_autoplay 
from AviaxMusic.utils.decorators import AdminRightsCheck, AdminRightsCheckCB

# --- Inline Keyboard Generator ---
def autoplay_markup(state: bool):
    text = "Autoplay: ON | ✅" if state else "Autoplay: OFF | ❌"
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=text, callback_data="autoplay_toggle")
            ]
        ]
    )

# --- Autoplay Command Handler ---
@app.on_message(filters.command(["autoplay"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def autoplay_command(client, message: Message, _, chat_id):
    # Check karna ki bot abhi VC me play kar raha hai ya nahi
    if not await is_active_chat(chat_id):
        return await message.reply_text("Bot is not streaming in the video chat.")

    # Database se current state nikalna
    state = await get_autoplay(chat_id)
    
    text = "**Autoplay Control**\n\nWhen autoplay is enabled, the bot will automatically play recommended songs from YouTube when the queue is empty."
    button = autoplay_markup(state)

    await message.reply_text(text, reply_markup=button)


# --- Autoplay Callback (Button Click) Handler ---
@app.on_callback_query(filters.regex("^autoplay_toggle$") & ~BANNED_USERS)
@AdminRightsCheckCB
async def autoplay_callback(client, CallbackQuery: CallbackQuery, _, chat_id):
    # Check karna ki bot abhi VC me play kar raha hai ya nahi
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("Bot is not streaming in the video chat.", show_alert=True)

    # State fetch karke usko reverse (toggle) karna
    state = await get_autoplay(chat_id)
    new_state = not state
    
    # Nayi state ko database me save karna
    if new_state:
        await set_autoplay(chat_id, True)
        status = "enabled"
    else:
        await set_autoplay(chat_id, False)
        status = "disabled"

    text = "**Autoplay Control**\n\nWhen autoplay is enabled, the bot will automatically play recommended songs from YouTube when the queue is empty."
    button = autoplay_markup(new_state)

    # Message update karna aur popup alert dena
    try:
        await CallbackQuery.edit_message_text(text, reply_markup=button)
    except Exception as e:
        print(f"Failed to edit autoplay message: {e}")
        
    await CallbackQuery.answer(f"Autoplay has been {status}.", show_alert=False)
  

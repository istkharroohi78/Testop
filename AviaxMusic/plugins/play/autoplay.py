from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch
from config import BOT_USERNAME
from AnieXMusic.core.call import Anie
from AnieXMusic.utils.database import get_assistant
from AnieXMusic.utils.stream.stream import stream

AUTO_PLAY = {}

@Client.on_message(filters.command("autoplay"))
async def autoplay(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/autoplay on\n/autoplay off"
        )

    state = message.command[1].lower()

    if state == "on":
        AUTO_PLAY[message.chat.id] = True
        await message.reply_text("✅ Autoplay Enabled")
    elif state == "off":
        AUTO_PLAY[message.chat.id] = False
        await message.reply_text("❌ Autoplay Disabled")


@Client.on_message(filters.audio | filters.video)
async def auto_music(_, message: Message):
    chat_id = message.chat.id

    if not AUTO_PLAY.get(chat_id):
        return

    query = message.audio.title if message.audio else message.video.file_name

    try:
        results = VideosSearch(query, limit=1)
        data = await results.next()

        if not data["result"]:
            return

        url = data["result"][0]["link"]
        title = data["result"][0]["title"]

        await stream(
            client=_,
            message=message,
            videoid=url,
            title=title,
            streamtype="audio",
        )

        await message.reply_text(
            f"🎵 Autoplaying:\n{title}"
        )

    except Exception as e:
        await message.reply_text(f"Error:\n{e}")
